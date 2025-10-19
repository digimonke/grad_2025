import streamlit as st
import pandas as pd
from causallearn.search.ConstraintBased.PC import pc
from causallearn.search.ScoreBased.GES import ges
import utils

st.set_page_config(page_title="Causal Toy Example", page_icon="🧪", layout="wide")
st.title("Ví dụ nhỏ: Học cấu trúc nhân quả từ dữ liệu mô phỏng")

st.write(
    """
    Ta tạo dữ liệu nhị phân từ một mạng Bayes 5 nút (X1→X3, X2→X3, X2→X4, X3→X5, X4→X5),
    sau đó áp dụng thuật toán khám phá quan hệ nhân quả để khôi phục cấu trúc.
    """
)

with st.sidebar:
    st.header("Thiết lập dữ liệu")
    n_samples = st.slider("Số mẫu", min_value=200, max_value=5000, value=1000, step=100)
    seed = st.number_input("Seed", min_value=0, value=0, step=1)
    algo = st.selectbox("Thuật toán", ["PC", "GES"], index=0)
    run = st.button("Chạy")

col_true, col_learned = st.columns(2)

if run:
    # 1) Tạo dữ liệu từ BN thật
    G_true = utils.get_true_bn()
    df = utils.sample_from_true_bn(n_samples=n_samples, seed=int(seed))

    # 2) Chạy thuật toán học cấu trúc
    data_np = df.to_numpy()
    if algo == "PC":
        cg = pc(data_np)
    else:
        cg = ges(data_np)

    labels = list(df.columns)

    with col_true:
        st.subheader("Đồ thị thật")
        utils.draw_true_bn_graph(G_true)
        st.dataframe(df.head(), use_container_width=True)

    with col_learned:
        st.subheader("Đồ thị học được")
        utils.draw_graph(cg, labels=labels, algo_name=algo)

else:
    st.info("Chọn tham số ở thanh bên và bấm 'Chạy' để tạo dữ liệu và học đồ thị.")
