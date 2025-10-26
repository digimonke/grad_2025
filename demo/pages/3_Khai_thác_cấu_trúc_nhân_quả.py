import streamlit as st
from sections import csl_ci, csl_csm, csl_algorithms

st.title("Khai thác cấu trúc quan hệ nhân quả từ dữ liệu")

st.info(
    """
    Quan hệ nhân quả giữa các biến thuộc dữ liệu thô chứa đựng nhiều thông tin hữu ích cho việc phân tích và dự đoán cho nhiều lĩnh vực khác nhau.
    Các nghiên cứu về khai thác cấu trúc quan hệ nhân quả từ dữ liệu nhắm đến việc trích xuất cấu trúc nhân quả Markov (Markovian Structural Causal Model) thể hiện các mẫu hình phụ thuộc
    có điều kiện giữa các biến trong dữ liệu.
    """
)

# conditional independence
csl_ci.render()

# causal structure model
csl_csm.render()

# algorithms
csl_algorithms.render()