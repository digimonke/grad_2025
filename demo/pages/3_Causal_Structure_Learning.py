from causallearn.search.ConstraintBased.PC import pc
from causallearn.search.ScoreBased.GES import ges
import utils
import streamlit as st

st.title("Xây dựng mạng quan hệ nhân quả từ dữ liệu")

st.info(
    """
    Quan hệ nhân quả giữa các biến thuộc dữ liệu thô chứa đựng nhiều thông tin hữu ích cho việc phân tích và dự đoán cho nhiều lĩnh vực khác nhau.
    Các nghiên cứu về xây dựng mạng quan hệ nhân quả từ dữ liệu nhắm đến việc trích xuất cấu trúc nhân quả Markov (Markovian Structural Causal Model) thể hiện các mẫu hình phụ thuộc
    có điều kiện giữa các biến trong dữ liệu.
    """
)

st.divider()
st.markdown(
    r"""
    Một **mạng quan hệ nhân quả Markov** (SCM) là một đồ thị có hướng vô chu trình (Directed Acyclic Graph - DAG) $$\mathcal{G}$$ trong đó các nút đại diện cho các biến ngẫu nhiên
    $${\{X_i\}}^p_{i=1}$$. Với mỗi nút $$i \in \mathcal{G}$$ ta có tập cha $${pa}_{\mathcal{G}}(i)={\{j \mid (j \rightarrow i) \in \mathcal{G}\}}$$.
    """
)
st.markdown(r"Một SCM với đồ thị $$\mathcal{G}$$ bao gồm các thành phần")

st.markdown("Tập biến nội sinh và tập biến ngoại sinh")
col1, col2 = st.columns(2)
with col1:
    st.latex("{\{X_i\}}^p_{i=1}")
with col2:
    st.latex("{\{\epsilon_i\}}^p_{i=1}")

st.markdown("Phân phối của biến nội sinh và phân phối của biến ngoại sinh")
col1, col2 = st.columns(2)
with col1:
    st.latex("P_X")
with col2:
    st.latex("P_{\epsilon}")

st.markdown("Tập hàm cấu trúc với giả định giá trị của biến $$X_i$$ được xác định bởi một hàm số của các biến cha và biến ngoại sinh tương ứng với nó")
col1, col2 = st.columns(2)
with col1:
    st.latex("{\{f_i\}}^p_{i=1}")
with col2:
    st.latex(r"X_i = f_i(pa_{\mathcal{G}}(X_i), \epsilon_i)")

st.markdown("Phân phối có điều kiện của một biến nội sinh thuộc SCM có dạng")
st.latex(r"P(X_i \mid pa_{\mathcal{G}}(X_i)) = \mathbb{E}[\mathbf{1}_{X_i = f_i(X_{\text{pa}_{\mathcal{G}}(i)}, \epsilon_i)} \mid X_{\text{pa}_{\mathcal{G}}(i)}]")

st.markdown("Theo tính chất Markov, phân phối của biến nội sinh được phân tích nhân tử như sau")
st.latex(r"\mathbb{P}_X(X) = \prod_{i=1}^p \mathbb{P}_X(X_i \mid X_{\text{pa}_{\mathcal{G}}(i)})")