import streamlit as st
from causallearn.search.ConstraintBased.PC import pc
from causallearn.search.ScoreBased.GES import ges
import utils

# ----------------------------
# Ví dụ nhỏ: Học cấu trúc nhân quả từ dữ liệu mô phỏng (moved from page 4)
# ----------------------------

def render():
    st.header("Ví dụ nhỏ: Khai thác cấu trúc nhân quả từ dữ liệu mô phỏng")

    st.write(
        """
        Ta tạo dữ liệu nhị phân từ một mạng Bayes 5 nút (X1→X3, X2→X3, X2→X4, X3→X5, X4→X5),
        sau đó áp dụng thuật toán khám phá quan hệ nhân quả để khôi phục cấu trúc.
        """
    )

    # Thiết lập dữ liệu (đưa vào nội dung thay vì sidebar)
    with st.form(key="toy_form"):
        st.subheader("Thiết lập dữ liệu (Toy Example)")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            n_samples = st.slider("Số mẫu", min_value=200, max_value=5000, value=1000, step=100, key="toy_n_samples")
        with col2:
            seed = st.number_input("Seed", min_value=0, value=0, step=1, key="toy_seed")
        with col3:
            algo = st.selectbox("Thuật toán", ["PC", "GES"], index=0, key="toy_algo")

        run = st.form_submit_button("Chạy", use_container_width=True)

    if run:
        # 1) Tạo dữ liệu từ BN thật
        G_true = utils.get_true_bn()
        df = utils.sample_from_true_bn(n_samples=int(n_samples), seed=int(seed))

        # 2) Chạy thuật toán học cấu trúc
        data_np = df.to_numpy()
        if algo == "PC":
            cg = pc(data_np)
        else:
            cg = ges(data_np)

        labels = list(df.columns)

        # Bảng dữ liệu ở trên
        st.subheader("Dữ liệu (5 dòng đầu)")
        st.dataframe(df.head(), use_container_width=True)

        # Hai đồ thị song song bên dưới: Đồ thị thật (trái) và Đồ thị học được (phải)
        st.subheader("Đồ thị")
        col_left, col_right = st.columns(2)
        with col_left:
            st.caption("Đồ thị thật")
            utils.draw_true_bn_graph(G_true, width_px=300)
        with col_right:
            st.caption(f"Đồ thị học được ({algo})")
            utils.draw_graph(cg, labels=labels, algo_name=algo, width_px=300)
    else:
        st.info("Trong phần Ví dụ nhỏ: Chọn tham số và bấm 'Chạy' để tạo dữ liệu và học đồ thị.")