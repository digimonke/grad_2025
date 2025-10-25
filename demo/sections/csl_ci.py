import streamlit as st

def render():
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