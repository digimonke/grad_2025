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

st.header("Độc lập có điều kiện")
st.markdown(
    """
    Việc xây dựng mạng nhân quả từ dữ liệu bắt đầu từ trích xuất tập mệnh đề phụ thuộc có điều kiện.
    **Kiểm thử độc lập có điều kiện** (Conditional Independence Test - CI Test) là nhóm phương pháp 
    kiểm định liệu giá trị của hai biến ngẫu nhiên có độc lập khi biết biến thứ ba hay không.
    """)
st.markdown(r"Xét biến ngẫu nhiên $$X$$ độc lập có điều kiện với biến ngẫu nhiên $$Y$$ khi biết biến ngẫu nhiên $$Z$$ thuộc phân phối chung $$\mathbb{P}_X$$ nếu và chỉ nếu")
st.latex(r"X \perp\!\!\!\perp Y \mid Z")
st.latex(r"\mathbb{P}(X \mid Y, Z) = \mathbb{P}(X \mid Z)")
st.latex(r"\mathbb{P}(X, Y \mid Z) = \mathbb{P}(X \mid Z) \mathbb{P}(Y \mid Z)")

st.markdown(r"Tuỳ thuộc vào tính chất của dự liệu, ta có thể lựa chọn các phương pháp kiểm định như $$\chi^2$$-test, G-test, Fisher's Z-test, hoặc phương pháp dựa trên thông tin như Mutual Information để thực hiện kiểm định độc lập có điều kiện.")
st.markdown(
    """
    Kết quả của thuật toán kiểm định độc lập có điều kiện là tập các mệnh đề độc lập có điều kiện giữa các biến trong dữ liệu.
    Tập mệnh đề này sẽ được sử dụng để kiểm tra tính tương thích của các cấu trúc mạng nhân quả với dữ liệu quan sát.
    """
)
st.latex(r"\mathcal{I}({\mathbb{P}_X}) = \{(X_i \perp\!\!\!\perp X_j \mid C) \mid X_i, X_j \in \mathbf{X}, C \subseteq \mathbf{X} \setminus \{X_i, X_j\}\}")

st.header("Mạng quan hệ nhân quả Markov")
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
    st.latex(r"X_i = f_i(X_{pa_{\mathcal{G}}(i)}, \epsilon_i)")

st.markdown("Phân phối có điều kiện của một biến nội sinh thuộc SCM có dạng")
st.latex(r"P(X_i \mid X_{pa_{\mathcal{G}}(i)}) = \mathbb{E}[\mathbf{1}_{X_i = f_i(X_{\text{pa}_{\mathcal{G}}(i)}, \epsilon_i)} \mid X_{\text{pa}_{\mathcal{G}}(i)}]")

st.markdown("Theo tính chất Markov, phân phối của biến nội sinh được phân tích nhân tử như sau")
st.latex(r"\mathbb{P}_X(X) = \prod_{i=1}^p \mathbb{P}_X(X_i \mid X_{\text{pa}_{\mathcal{G}}(i)})")

st.subheader("Phân tách có hướng")
st.markdown(
    """
    Một mạng nhân quả Markov tương thích với phân phối của dữ liệu -- và là một I-map của $$\mathbb{P}_X$$ -- nếu tất cả các mệnh đề phân tách có hướng (d-separation) được biểu diễn trong đồ thị là tập con của tập mệnh đề độc lập có điều kiện trong phân phối dữ liệu quan sát.
    """
)
st.latex(r"\mathcal{I}({\mathcal{G}}) \subseteq \mathcal{I}({\mathbb{P}_X})")

st.markdown(r"""
    Một mệnh đề phân tách có hướng là biểu diễn trực quan của mệnh đề độ lập có điều kiện giữa hai biến trong 
    dữ liệu trên một đồ thị nhân quả Markov. Dựa trên một loại cấu trúc đặc biệt của đồ thị có hướng là **đối** (collider còn được gọi là immorality hay v-structure)
    một mệnh đề phân tách có hướng giữa hai nút $$i$$ và $$j$$ được định nghĩa như sau 
    """
)
st.markdown(r"""
    Xét một đường đi $$\gamma = \langle \gamma_1 = i, \gamma_2, \dots, \gamma_M = j \rangle$$, nút $$\gamma_m$$ trên đường đi này được gọi là **đối** nếu các cạnh trên đường đi hội tụ vào nút $$\gamma_m$$, tức là $$\gamma_{m-1} \rightarrow \gamma_m \leftarrow \gamma_{m+1}$$.
    Xét tập nút điều kiện $$C \subseteq \mathbf{X} \setminus \{X_i, X_j\}$$. Đường đi $$\gamma$$ chặn quan hệ giữa hai nút $$i$$ và $$j$$ nếu một trong hai điều kiện sau được thoả mãn
    - Một nút bất kỳ thuộc $$\gamma$$ không phải là đối và thuộc tập điều kiện $$C$$.
    - Không có nút đối và con cháu của nút đối thuộc tập điều kiện $$C$$.
    """
)