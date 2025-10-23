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
st.markdown(r"""
    Một mệnh đề phân tách có hướng là biểu diễn trực quan của mệnh đề độ lập có điều kiện giữa hai biến trong 
    dữ liệu trên một đồ thị nhân quả Markov. Dựa trên một loại cấu trúc đặc biệt của đồ thị có hướng là **đối** (collider còn được gọi là immorality hay v-structure)
    một mệnh đề phân tách có hướng giữa hai nút $$i$$ và $$j$$ được định nghĩa như sau 
    """
)
st.markdown(r"""
    Xét một đường đi $$\gamma = \langle \gamma_1 = i, \gamma_2, \dots, \gamma_M = j \rangle$$, nút $$\gamma_m$$ trên đường đi này được gọi là **đối** nếu các cạnh trên đường đi hội tụ vào nút $$\gamma_m$$, tức là $$\gamma_{m-1} \rightarrow \gamma_m \leftarrow \gamma_{m+1}$$.
    Xét tập nút điều kiện $$C \subseteq \mathbf{X} \setminus \{X_i, X_j\}$$. Đường đi $$\gamma$$ **chặn quan hệ** giữa hai nút $$i$$ và $$j$$ nếu một trong hai điều kiện sau được thoả mãn
    - Một nút bất kỳ thuộc $$\gamma$$ không phải là đối và thuộc tập điều kiện $$C$$.
    - Không có nút đối và con cháu của nút đối thuộc tập điều kiện $$C$$.
    """
)
st.markdown(r"""
    Hai nút $$i$$ và $$j$$ được gọi là **phân tách có hướng** (d-separated) bởi tập nút điều kiện $$C$$ nếu mọi đường đi giữa $$i$$ và $$j$$ đều bị chặn quan hệ bởi $$C$$.
    Tập mệnh đề phân tách có hướng của đồ thị $$\mathcal{G}$$ được định nghĩa
    """)
st.latex(r"\mathcal{I}_{\perp\!\!\!\perp}(\mathcal{G}) = \{(i, j, C) \mid i, j \in [p], C \subseteq [p]\setminus\{i, j\}, i \perp\kern-2.7pt\perp_G j \mid C\}")

st.subheader("Independence Map")
st.markdown(
    r"""
    Một đồ thị nhân quả Markov $$\mathcal{G}$$ được gọi là **Independence Map** (I-MAP) của phân phối dữ liệu quan sát $$\mathbb{P}_X$$ nếu tập mệnh đề phân tách có hướng trong đồ thị là tập con của tập mệnh đề độc lập có điều kiện trong phân phối dữ liệu.
    Ở chiều ngược lại ta nói phân phối dữ liệu $$\mathbb{P}_X$$ thoả **tính chất Markov toàn cục** với đồ thị nhân quả Markov $$\mathcal{G}$$.
    """
)
st.latex(r"\mathcal{I}({\mathcal{G}}) \subseteq \mathcal{I}({\mathbb{P}_X})")

st.markdown(r"""
    Hệ quả của tính chấy Markov toàn cục là phân phối $$P_X$$ có thể có nhiều đồ thị I-MAP khác nhau. Nếu các I-MAP này có cùng một tập mệnh đề phân tách có hướng thì chúng thuộc cùng một **lớp tương đương Markov** (Markov Equivalence Class - MEC).
""")

with st.expander("Ví dụ: Hai DAG thuộc cùng lớp tương đương Markov"):
    st.markdown(
        """
        Cả hai đồ thị dưới đây có cùng skeleton (X1—X2—X3) và không có cấu trúc đối (v-structure),
        nên chúng thuộc cùng một lớp tương đương Markov.
        """
    )

    col_a, col_b = st.columns(2)

    # Use Streamlit Graphviz for auto-scaling within columns
    dot_a = """
    digraph G {
        graph [rankdir=LR, nodesep=0.3, ranksep=0.4, margin=0.02];
        node [shape=ellipse];
        X1 -> X2; X2 -> X3;
    }
    """
    dot_b = """
    digraph G {
        graph [rankdir=LR, nodesep=0.3, ranksep=0.4, margin=0.02];
        node [shape=ellipse];
        X2 -> X1; X2 -> X3;
    }
    """

    with col_a:
            st.caption("DAG A: X1 → X2 → X3")
            st.graphviz_chart(dot_a, use_container_width=True)

    with col_b:
            st.caption("DAG B: X1 ← X2 → X3")
            st.graphviz_chart(dot_b, use_container_width=True)

    # Shared d-separation statement for both DAGs
    st.markdown("Phát biểu phân tách có hướng chung (d-separation):")
    st.latex(r"X_1 \, \perp\!\!\!\perp \, X_3 \mid X_2")
