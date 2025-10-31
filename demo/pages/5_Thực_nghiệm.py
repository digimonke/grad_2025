import streamlit as st
import pandas as pd
from utils import bnlearn_dag_to_dot, simulate_nonlinear_sem_from_pgmpy, add_random_edges_acyclic, adjacency_to_dot, simulate_lingam_from_pgmpy, adjacency_to_edge_set, diff_pgmpy_models_to_dot
from algo.algo import linear_causal_discovery, stability_subsampling

import requests
import gzip
from io import BytesIO
from pgmpy.readwrite import BIFReader
	
# Use session state to load on demand without writing anything to disk
if 'dag' not in st.session_state:
	st.session_state.dag = None
if 'negative_dag' not in st.session_state:
	st.session_state.negative_dag = None
if 'perturbed_edges' not in st.session_state:
    st.session_state.perturbed_edges = []
if 'candidate_edges' not in st.session_state:
    st.session_state.candidate_edges = []
if 'simulated_df' not in st.session_state:
	st.session_state.simulated_df = None
if 'causal_dag' not in st.session_state:
    st.session_state.causal_dag = None
if 'W_est' not in st.session_state:
    st.session_state.W_est = None
if 'stability_results' not in st.session_state:
    st.session_state.stability_results = None
if 'false_positive_edges' not in st.session_state:
    st.session_state.false_positive_edges = []
if 'recommended_removals' not in st.session_state:
    st.session_state.recommended_removals = []

def original_graph():
    # 1. import example
    st.subheader("Đồ thị tri thức")

    if st.session_state.dag is None:
        # Download BIF.gz on demand and parse fully in-memory
        BIF_URL = "https://www.bnlearn.com/bnrepository/insurance/insurance.bif.gz"
        try:
            with st.spinner("Đang tải Insurance.bif từ bnlearn repository..."):
                resp = requests.get(BIF_URL, timeout=20)
                resp.raise_for_status()
                compressed = BytesIO(resp.content)
                with gzip.GzipFile(fileobj=compressed, mode='rb') as gz:
                    bif_text = gz.read().decode('utf-8')
            
                # Some pgmpy versions accept 'string' kw, others offer from_string
                model = None
                try:
                    reader = BIFReader(string=bif_text)  # type: ignore[arg-type]
                    model = reader.get_model()
                except Exception:
                    try:
                        reader = BIFReader.from_string(bif_text)  # type: ignore[attr-defined]
                        model = reader.get_model()
                    except Exception as e:
                        st.error(f"Không thể parse BIF trong bộ nhớ: {e}")

                if model is not None:
                    st.session_state.dag = model
        except Exception as e:
            st.error(f"Lỗi tải DAG: {e}")
        
    # Show basic info
    try:
        n_nodes = len(st.session_state.dag.nodes())
        n_edges = len(st.session_state.dag.edges())
        st.caption(f"DAG 'insurance': {n_nodes} nút, {n_edges} cạnh")
    except Exception:
        st.caption("Không đọc được thông tin nút/cạnh từ DAG.")

    # Render with Graphviz in Streamlit (no system Graphviz required)
    dot = bnlearn_dag_to_dot({"model": st.session_state.dag})
    st.graphviz_chart(dot, use_container_width=True)

def perturbed_graph():
    # 2. Perturb structure: add random edges without cycles
    st.subheader("Gây nhiễu cấu trúc")
    st.markdown("""
        Nhằm mô phỏng lại những cạnh nhiễu thường thấy trong đồ thị tri thức thực tế, ta tiến hành thêm ngẫu nhiên một số cạnh vào DAG hiện tại
        trong khi vẫn giữ tính chất không chu trình (acyclic). Nhiệm vụ của thuật toán là phát hiện và loại bỏ các cạnh nhiễu này.
        """)
    
    if st.session_state.dag is not None:
        c1, c2 = st.columns([1, 1])
        with c1:
            k_add = st.number_input("Số cạnh nhiễu", min_value=3, max_value=26, value=12, step=1)
        with c2:
            seed = st.number_input("Random seed", min_value=0, max_value=10, value=5, step=1)

        do_perturb = st.button("Thêm nhiễu")
        if do_perturb:
            with st.spinner("Đang thêm cạnh ngẫu nhiên và kiểm tra chu trình..."):
                st.session_state.negative_dag, st.session_state.perturbed_edges = add_random_edges_acyclic(st.session_state.dag, n_add=int(k_add), seed=int(seed))

    if st.session_state.negative_dag is not None:
        st.caption("DAG sau khi thêm quan hệ nhiễu (cạnh mới tô đỏ):")
        dot_new = bnlearn_dag_to_dot({"model": st.session_state.negative_dag}, highlight_edges=st.session_state.perturbed_edges)
        st.graphviz_chart(dot_new, use_container_width=True)

def synthetic_data():
    if st.session_state.dag is None or st.session_state.negative_dag is None:
        return
    
    # 3. dữ liệu mô phỏng
    st.subheader("Dữ liệu mô phỏng từ DAG")
    st.markdown("""
        Xem đồ thị tri thức trên như một mạng nhân Bayes biểu diễn chuỗi nhân quả hoàn chỉnh giữa các biến trong dữ liệu.
        Nghiên cứu mô phỏng dữ liệu từ mạng Bayes này bằng các hàm phi tuyến tính với nhiễu ngẫu nhiên theo phân phối chuẩn để tạo ra tập dữ liệu mô phỏng.
    Dữ liệu được tạo ra tuân theo các giả định sau:
        - **Giả định hoàn thiện nhân quả (Causal Sufficiency)**: Giả định rằng tất cả các biến trong hệ thống (causal variables) đều đã được quan sát và không có biến ẩn (latent confounding) nằm ngoài tập dữ liệu.
        - **Giả định Markov (Causal Markov Assumption)**: Mỗi biến trong mạng nhân quả là độc lập có điều kiện với các biến không phải là hậu duệ của nó, khi biết giá trị của các biến cha.
    """)

    with st.form(key="simulate_form"):
        c1, c2, c3 = st.columns([1.6, 1, 1])
        with c1:
            sem_choice = st.selectbox(
                "Cấu tạo hàm (functional form)",
                # "Multilayer Perceptron",
                # "Gaussian Process",
                options=[
                    "LiNGAM (linear, non-Gaussian)",
                ],
                index=0,
            )
        with c2:
            n_samples = st.number_input("Số mẫu", min_value=250, max_value=750, value=300, step=50)
        with c3:
            noise_scale = st.number_input("Độ lệch nhiễu (σ)", min_value=0.0, value=1.2, step=0.1)

        submitted = st.form_submit_button("Tạo dữ liệu")

    if submitted:
        with st.spinner("Đang mô phỏng dữ liệu..."):
            try:
                if sem_choice.startswith("LiNGAM"):
                    df_sim = simulate_lingam_from_pgmpy(
                        st.session_state.dag,
                        n=int(n_samples),
                        noise="laplace",
                        noise_scale=float(noise_scale),
                    )
                else:
                    df_sim = simulate_nonlinear_sem_from_pgmpy(
                        st.session_state.dag, n=int(n_samples), sem_type=sem_choice, noise_scale=float(noise_scale)
                    )
                st.session_state.simulated_df = df_sim
                st.success(f"Đã tạo dữ liệu: {df_sim.shape[0]}x{df_sim.shape[1]}. 20 dòng đầu tiên hiển thị bên dưới.")
            except Exception as e:
                st.error(f"Không thể mô phỏng dữ liệu: {e}")

    if st.session_state.simulated_df is not None:
        st.dataframe(st.session_state.simulated_df.head(20), use_container_width=True)

def causal_discovery():
    if st.session_state.simulated_df is None:
        return

    # 4. Run causal discovery to try to recover true structure from data
    st.subheader("Khai thác cấu trúc nhân quả từ dữ liệu")
    run_discovery = st.button("Khai thác cấu trúc nhân quả")
    if run_discovery:
        with st.spinner("Đang khai thác cấu trúc nhân quả..."):
            try:
                W_est = linear_causal_discovery(st.session_state.simulated_df)
                st.session_state.W_est = W_est
                
            except Exception as e:
                st.error(f"Exception was raised: {e}")
    
    if st.session_state.W_est is not None:
        # node names from simulated data
        default_labels_list = list(st.session_state.simulated_df.columns)
        dot_W = adjacency_to_dot(st.session_state.W_est, labels=default_labels_list, rankdir='LR')
        st.graphviz_chart(dot_W, use_container_width=True)
        st.success("Khai thác cấu trúc nhân quả thành công.")

        if st.session_state.negative_dag is not None:
            st.subheader("So sánh với DAG gây nhiễu")
            discovered = adjacency_to_edge_set(st.session_state.W_est, labels=default_labels_list, threshold=float(0.5))
            perturbed = {(str(u), str(v)) for (u, v) in st.session_state.negative_dag.edges()}
            st.session_state.candidate_edges = sorted(list(perturbed - discovered))
            st.caption(f"Số cạnh tồn tại trong đồ thị nhiễu nhưng không có trong cấu trúc nhân quả: {len(st.session_state.candidate_edges)}")
            if st.session_state.candidate_edges:
                st.dataframe(pd.DataFrame(st.session_state.candidate_edges, columns=["u", "v"]))
                dot_neg = bnlearn_dag_to_dot({"model": st.session_state.negative_dag}, highlight_edges=st.session_state.candidate_edges)
                st.graphviz_chart(dot_neg, use_container_width=True)

def edge_stability():
    if st.session_state.W_est is None:
        return

    st.subheader("Kiểm tra độ ổn định của quan hệ nhân quả")
    st.markdown(
        """
        Tập cạnh được đề xuất ở trên chưa hẳn là tập cạnh nhiễu chính xác. Khai thác cấu trúc nhân quả từ đồ thị là một mảng
        nghiên cứu đang phát triển với nhiều thách thức, đặc biệt khi tập dữ liệu bị ảnh hưởng bởi nhiễu, ảnh hưởng của các quan hệ
        trừ khử lẫn nhau, và các yếu tố khác. Do đó, ta cần kiểm tra độ ổn định của các cạnh được phát hiện nhằm đánh giá độ tin cậy của chúng.
        Phương pháp stability subsampling được sử dụng để đánh giá độ ổn định của các cạnh trong đồ thị nhân quả được khai thác.
        """
    )
    with st.form(key="stability_form"):
        c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
        with c1:
            subsample_frac = st.slider("Tỉ lệ lấy mẫu", min_value=0.4, max_value=0.75, value=0.65, step=0.01)
        with c2:
            B = st.number_input("Số lần lặp", min_value=10, max_value=50, value=20, step=1)
        with c3:
            pi_threshold = st.slider("Ngưỡng π", min_value=0.1, max_value=0.9, value=0.75, step=0.05)
        with c4:
            base_seed = st.number_input("Seed", min_value=0, max_value=9999, value=7, step=1)
        run_btn = st.form_submit_button("Chạy stability subsampling")

    if run_btn:
        if not st.session_state.candidate_edges:
            st.info("Không có candidate_edges để kiểm tra. Hãy chạy các bước trước (gây nhiễu, tạo dữ liệu, khai thác cấu trúc).")
            return

        with st.spinner("Đang chạy stability subsampling..."):
            df_results, false_pos, keep_remove = stability_subsampling(
                st.session_state.simulated_df,
                st.session_state.candidate_edges,
                B=int(B),
                subsample_frac=float(subsample_frac),
                seed=int(base_seed),
                pi_threshold=float(pi_threshold),
                discovery_fn=linear_causal_discovery,
            )

        st.session_state.stability_results = df_results
        st.session_state.false_positive_edges = false_pos
        st.session_state.recommended_removals = keep_remove

    # Hiển thị kết quả nếu có
    if st.session_state.stability_results is not None:
        st.markdown("### Kết quả tần suất xuất hiện cạnh trong các mẫu")
        st.dataframe(st.session_state.stability_results, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Cạnh xuất hiện thường xuyên (freq > π) — false positive trong đề xuất")
            st.caption("Các cạnh này nên loại khỏi danh sách cạnh nhiễu.")
            if st.session_state.false_positive_edges:
                st.dataframe(pd.DataFrame(st.session_state.false_positive_edges, columns=["u", "v"]))
            else:
                st.info("Không có cạnh nào vượt ngưỡng π.")

        with c2:
            st.markdown("#### Cạnh ít xuất hiện (freq ≤ π) — đề xuất xoá")
            if st.session_state.recommended_removals:
                st.dataframe(pd.DataFrame(st.session_state.recommended_removals, columns=["u", "v"]))
            else:
                st.info("Mọi cạnh đều vượt ngưỡng π, không còn cạnh đề xuất xoá.")

def show_diff_against_ground_truth():
    if st.session_state.stability_results is None:
        return

    st.subheader("So sánh với đồ thị gốc sau khi xoá cạnh")

    # Chỉ xoá những cạnh thực sự tồn tại trong DAG hiện tại
    existing = set((str(u), str(v)) for (u, v) in st.session_state.negative_dag.edges())
    to_remove = [(u, v) for (u, v) in st.session_state.recommended_removals if (u, v) in existing]
    try:
        # remove in batch
        final_graph = st.session_state.negative_dag.copy()
        final_graph.remove_edges_from(to_remove)
    except Exception:
        # fallback remove one by one for safety
        for (u, v) in to_remove:
            try:
                st.session_state.negative_dag.remove_edge(u, v)
            except Exception:
                pass
    
    gt_edges = {(str(u), str(v)) for (u, v) in st.session_state.dag.edges()}
    curr_edges = {(str(u), str(v)) for (u, v) in final_graph.edges()}

    extra_edges = sorted(list(curr_edges - gt_edges))  # vẫn thừa so với ground truth (chưa xoá hết)
    missing_edges = sorted(list(gt_edges - curr_edges))  # thiếu so với ground truth (đã xoá nhầm cạnh đúng)

    # Tích hợp với kết quả xoá: thống kê bao nhiêu cạnh đề xuất đã xoá là đúng/nhầm
    rr = set((str(u), str(v)) for (u, v) in st.session_state.get("recommended_removals", []))
    removed_correct = sorted(list(rr & set(missing_edges)))  # false positive removals
    removed_noise = sorted(list(rr - set(missing_edges)))    # đã đề xuất xoá và không còn trong DAG, nhưng không thuộc GT

    if not extra_edges and not missing_edges:
        st.success("Đồ thị gây nhiễu sau khi xoá đã trùng khớp với đồ thị gốc.")
        # Hiển thị đồ thị chung để xác nhận
        dot_ok = bnlearn_dag_to_dot({"model": final_graph})
        st.graphviz_chart(dot_ok, use_container_width=True)
        return

    # Bảng tổng quan
    st.caption(
        f"Tổng quan: còn thừa {len(extra_edges)} cạnh; xoá nhầm {len(removed_correct)} cạnh thuộc ground truth; xoá đúng {len(removed_noise)} cạnh nhiễu."
    )

    # Bảng chi tiết
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Cạnh thừa (so với ground truth)")
        st.caption(f"Còn lại: {len(extra_edges)} cạnh")
        if extra_edges:
            st.dataframe(pd.DataFrame(extra_edges, columns=["u", "v"]))
        else:
            st.info("Không còn cạnh thừa.")

    with c2:
        st.markdown("#### Cạnh thiếu (so với ground truth) — false positive (xoá cạnh đúng)")
        st.caption(f"Thiếu: {len(missing_edges)} cạnh; Trong đó xoá nhầm theo đề xuất: {len(removed_correct)} cạnh")
        if missing_edges:
            st.dataframe(pd.DataFrame(missing_edges, columns=["u", "v"]))
        else:
            st.info("Không có cạnh thiếu.")

    # Hiển thị một đồ thị duy nhất thể hiện cả hai loại khác biệt
    dot_diff = diff_pgmpy_models_to_dot(
        st.session_state.dag,
        final_graph,
        rankdir="LR",
        title="Đỏ đặc: cạnh thừa | Đỏ nét đứt: cạnh thiếu",
    )
    st.graphviz_chart(dot_diff, use_container_width=True)

st.title("Thực nghiệm")
st.markdown("""
    Sau đây là một thực nghiệm nhỏ của nghiên cứu dựa trên thuật toán được đề xuất. Nghiên cứu sử dụng đồ thị với mã nguồn mở
	từ thư viện bnlearn với 27 nút và 52 cạnh, mô tả chuỗi nhân quả giữa các thực thể trong lĩnh vực bảo hiểm tài sản và tai nạn.
    Mục tiêu của thực nghiệm là phát hiện và đề xuất một tập cạnh nhiễu nhằm xoá khỏi đồ thị tri thức, cải thiện chất lượng tri thức
    thuộc đồ thị.
""")

# Bắt đầu với một đồ thị tri thức
original_graph()
# Gây nhiễu đồ thị tri thức
perturbed_graph()
# Tạo dữ liệu mô phỏng cho đồ thị tri thức thật
synthetic_data()
# Khôi phục cấu trúc nhân quả từ dữ liệu mô phỏng
causal_discovery()
# Sử dụng statbility subsampling và causal inference để kiểm tra độ ổn định của cạnh
edge_stability()
# show final graph
show_diff_against_ground_truth()