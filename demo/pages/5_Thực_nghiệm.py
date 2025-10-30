import streamlit as st
from utils import bnlearn_dag_to_dot, simulate_nonlinear_sem_from_pgmpy, add_random_edges_acyclic
import requests
import gzip
from io import BytesIO
try:
	from pgmpy.readwrite import BIFReader
except Exception:
	BIFReader = None
	
st.title("Thực nghiệm")
st.markdown("""
    Sau đây là một thực nghiệm nhỏ của nghiên cứu dựa trên thuật toán được đề xuất. Nghiên cứu sử dụng đồ thị với mã nguồn mở
	từ thư viện bnlearn với 27 nút và 52 cạnh, mô tả chuỗi nhân quả giữa các thực thể trong lĩnh vực bảo hiểm tài sản và tai nạn.
""")

# 1. import example
st.subheader("Đồ thị tri thức")

# Use session state to load on demand without writing anything to disk
if 'dag' not in st.session_state:
	st.session_state.dag = None
if 'negative_dag' not in st.session_state:
	st.session_state.negative_dag = None

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

# 2. dữ liệu mô phỏng
st.subheader("Dữ liệu mô phỏng từ DAG")
st.markdown("""
    Xem đồ thị tri thức trên như một mạng nhân Bayes biểu diễn chuỗi nhân quả hoàn chỉnh giữa các biến trong dữ liệu.
	Nghiên cứu mô phỏng dữ liệu từ mạng Bayes này bằng các hàm phi tuyến tính với nhiễu ngẫu nhiên theo phân phối chuẩn để tạo ra tập dữ liệu mô phỏng.
	Dữ liệu được tạo ra tuần theo các giả định sau:
	- **Giả định hoàn thiện nhân quả (Causal Sufficiency)**: Giả định rằng tất cả các biến trong hệ thống (causal variables) đều đã được quan sát và không có biến ẩn (latent confounding) nằm ngoài tập dữ liệu.
    - **Giả định Markov (Causal Markov Assumption)**: Mỗi biến trong mạng nhân quả là độc lập có điều kiện với các biến không phải là hậu duệ của nó, khi biết giá trị của các biến cha.
""")

if st.session_state.dag is not None:
	with st.form(key="simulate_form"):
		c1, c2, c3 = st.columns([1.6, 1, 1])
		with c1:
			sem_choice = st.selectbox(
				"Cấu tạo hàm (functional form)",
				options=[
					"Multilayer Perceptron",
					"Gaussian Process",
				],
				index=0,
			)
		with c2:
			n_samples = st.number_input("Số mẫu", min_value=10, max_value=20000, value=1000, step=100)
		with c3:
			noise_scale = st.number_input("Độ lệch nhiễu (σ)", min_value=0.0, value=1.0, step=0.1)

		submitted = st.form_submit_button("Tạo dữ liệu")

	if submitted:
		with st.spinner("Đang mô phỏng dữ liệu..."):
			try:
				df_sim = simulate_nonlinear_sem_from_pgmpy(
					st.session_state.dag, n=int(n_samples), sem_type=sem_choice, noise_scale=float(noise_scale)
				)
				st.session_state["simulated_df"] = df_sim
				st.success(f"Đã tạo dữ liệu: {df_sim.shape[0]}x{df_sim.shape[1]}. 20 dòng đầu tiên hiển thị bên dưới.")
			except Exception as e:
				st.error(f"Không thể mô phỏng dữ liệu: {e}")

	df_sim = st.session_state.get("simulated_df")
	if df_sim is not None:
		st.dataframe(df_sim.head(20), use_container_width=True)

else:
	st.info("Chưa có DAG để mô phỏng. Hãy tải DAG trước.")

# 3. Perturb structure: add random edges without cycles
st.subheader("Gây nhiễu cấu trúc")
if st.session_state.dag is not None:
	st.markdown("""
       Nhằm mô phỏng lại những cạnh nhiễu thường thấy trong đồ thị tri thức thực tế, ta tiến hành thêm ngẫu nhiên một số cạnh vào DAG hiện tại
       trong khi vẫn giữ tính chất không chu trình (acyclic). Nhiệm vụ của thuật toán là phát hiện và loại bỏ các cạnh nhiễu này.
	""")
	c1, c2 = st.columns([1, 1])
	with c1:
		k_add = st.number_input("Số cạnh nhiễu", min_value=3, max_value=26, value=12, step=1)
	with c2:
		seed = st.number_input("Random seed", min_value=0, max_value=10, value=1, step=1)

	do_perturb = st.button("Thêm nhiễu")
	if do_perturb:
		with st.spinner("Đang thêm cạnh ngẫu nhiên và kiểm tra chu trình..."):
			new_model, added_edges = add_random_edges_acyclic(st.session_state.dag, n_add=int(k_add), seed=int(seed))
			st.caption("DAG sau khi thêm cạnh (cạnh mới tô đỏ):")
			dot_new = bnlearn_dag_to_dot({"model": new_model}, highlight_edges=added_edges)
			st.graphviz_chart(dot_new, use_container_width=True)
			st.session_state.negative_dag = new_model
