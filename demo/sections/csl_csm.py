import streamlit as st

def directional_separation():
    st.subheader("Phân tách có hướng (Directional Separation)")
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
    st.latex(r"\mathcal{I}_{\perp\!\!\!\perp}(\mathcal{G}) = \{(i, j, C) \mid i, j \in [p], C \subseteq [p]\setminus\{i, j\}, i \perp\perp_G j \mid C\}")

def imap_example():
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

def imap():
    st.subheader("Mạng độc lập (Independence Map)")
    st.markdown(
        r"""
        Một đồ thị nhân quả Markov $$\mathcal{G}$$ được gọi là **Independence Map** (I-MAP) của phân phối dữ liệu quan sát $$\mathbb{P}_X$$ nếu tập mệnh đề phân tách có hướng trong đồ thị là tập con của tập mệnh đề độc lập có điều kiện trong phân phối dữ liệu.
        Ở chiều ngược lại ta nói phân phối dữ liệu $$\mathbb{P}_X$$ thoả **tính chất Markov toàn cục** với đồ thị nhân quả Markov $$\mathcal{G}$$.
        """
    )
    st.latex(r"\mathcal{I}({\mathcal{G}}) \subseteq \mathcal{I}({\mathbb{P}_X})")

    st.markdown(r"""
        Hệ quả của tính chất Markov toàn cục là phân phối $$P_X$$ có thể có nhiều I-MAP khác nhau.
        Một tập các I-MAP có cùng tập mệnh đề phân tách có hướng được gọi là một **lớp tương đương Markov** (Markov Equivalence Class - MEC).
    """)

    imap_example()

    st.info(r"""
        **Hệ quả của quan sát trên là các thuật toán xây dựng cấu trúc nhân quả chỉ có thể khôi phục được đến lớp tương đương Markov của đồ thị nhân quả Markov mục tiêu thông qua phân tích dữ liệu quan sát.**
    """)

    st.markdown(r"""Các thuật toán xây dựng cấu trúc nhân quả sẽ cố gắng vượt qua giới hạn này bằng cách sử dụng thêm các giả định bổ sung (như giả định phi chu trình, tuyến tính, không có biến ẩn…),
                sử dụng dữ liệu can thiệp (interventional data) hoặc sử dụng một nền tảng (prior) để xác định hướng của các cạnh trong đồ thị nhân quả Markov.""")


def render():
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

    st.markdown("Hàm cấu trúc với giả định giá trị của biến $$X_i$$ được xác định bởi một hàm số của các biến cha và biến ngoại sinh tương ứng với nó. Đa phần các thuật toán đều hoạt động dựa trên giả định về hàm cấu trúc của SCM như tuyến tính hay phi tuyến tính.")
    col1, col2 = st.columns(2)
    with col1:
        st.latex("{\{f_i\}}^p_{i=1}")
    with col2:
        st.latex(r"X_i = f_i(X_{pa_{\mathcal{G}}(i)}, \epsilon_i)")

    st.markdown("Phân phối có điều kiện của một biến nội sinh thuộc SCM có dạng")
    st.latex(r"P(X_i \mid X_{pa_{\mathcal{G}}(i)}) = \mathbb{E}[\mathbf{1}_{X_i = f_i(X_{\text{pa}_{\mathcal{G}}(i)}, \epsilon_i)} \mid X_{\text{pa}_{\mathcal{G}}(i)}]")

    st.markdown("Theo tính chất Markov, phân phối của biến nội sinh được phân tích nhân tử như sau")
    st.latex(r"\mathbb{P}_X(X) = \prod_{i=1}^p \mathbb{P}_X(X_i \mid X_{\text{pa}_{\mathcal{G}}(i)})")

    st.markdown(r"""**Phân tích nhân tử trên đảm bảo một biến nội sinh $$X_i$$ độc lập khỏi các biến không phải con cháu của nó khi đã biết giá trị của các biến cha của nó.**""")

    # directional separation
    directional_separation()

    # independence map
    imap()