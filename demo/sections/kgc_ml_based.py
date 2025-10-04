import streamlit as st

def render():
    st.header("Phương pháp dựa trên học máy")
    st.info("**Phương pháp học máy (Machine Learning-based)** sử dụng các thuật toán học máy với nhúng (embedding) để học từ chính cấu trúc đồ thị và dự đoán các thành phần thiếu.")
    st.markdown(
        """
        - [TransE: Translating Embeddings for Modeling Multi-relational Data](https://papers.nips.cc/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf)
        - [RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space](https://arxiv.org/abs/1902.10197)
        """
    )
    st.write("""
         Với sự phát triển của các mô hình ngôn ngữ lớn và lượng tri thức mà các mô hình này học được trong quá trình huấn luyện, có một số nghiên cứu gần đây đã thử áp dụng các mô hình ngôn ngữ lớn để thực hiện tác vụ hoàn thiện đồ thị tri thức.
            - (Survey) [Exploring large language models for knowledge graph completion](https://ieeexplore.ieee.org/abstract/document/10889242)
        """)