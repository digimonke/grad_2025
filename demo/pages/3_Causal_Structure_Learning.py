from causallearn.search.ConstraintBased.PC import pc
from causallearn.search.ScoreBased.GES import ges
import utils
import streamlit as st

st.title("Xây dựng cấu trúc quan hệ nhân quả từ dữ liệu")

def example():
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls", "csv"])

    if uploaded_file is not None:
        data = utils.read_file(uploaded_file)
        st.write("Preview of data:", data.head())

        algo = st.selectbox(
            "Select Causal Discovery Algorithm",
            ["PC", "GES"]
        )

        if st.button("Run Causal Discovery"):
            # Convert to numpy
            data = utils.normalize_data(data)
            data_np = data.to_numpy()

            if algo == "PC":
                cg = pc(data_np)  # alpha is significance level
            elif algo == "GES":
                cg = ges(data_np)

            utils.draw_graph(cg, labels=list(data.columns), algo_name=algo)

st.info(
    """
    Quan hệ nhân quả giữa các biến thuộc dữ liệu thô chứa đựng nhiều thông tin hữu ích cho việc phân tích và dự đoán cho nhiều lĩnh vực khác nhau.
    Các nghiên cứu về **xây dựng cấu trúc quan hệ nhân quả từ dữ liệu** nhắm đến việc trích xuất một mạng Bayes thể hiện các mẫu hình phụ thuộc
    có điều kiện giữa các biến trong dữ liệu.
    """
)

st.expander("Ví dụ minh hoạ")
with st.expander("Ví dụ minh hoạ"):
    example()