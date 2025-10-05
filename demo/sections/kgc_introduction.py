import streamlit as st

def render():
    st.info("**Tác vụ hoàn thiện đồ thị tri thức (Knowledge Graph Completion)** với mục tiêu bổ sung các thực thể, quan hệ hoặc thuộc tính còn thiếu trong đồ thị hiện có, làm giàu kho tri thức của đồ thị.")
    st.write("""
            Về mặt tác vụ, KGC nhắm đến dự đoán thành phần còn thiếu trong một bộ ba (chủ thể, quan hệ, đối tượng) dựa trên các thành phần đã biết:
            - **Dự đoán quan hệ (Relation Prediction)**: xác định **quan hệ** giữa hai thực thể đã biết.
            - **Dự đoán thực thể (Entity Prediction)**: xác định **chủ thể** hoặc **đối tượng** còn thiếu trong bộ ba.
            """)

    st.divider()
    st.write("""
            Về mặt kỹ thuật, KGC truyền thống dựa trên 2 hướng chính:
            - **Phương pháp dựa trên quy tắc (Rule-based)**: khai thác các mẫu quy tắc từ bản thể đồ thị hiện có để suy luận các bộ ba mới.
                - [AMIE: association rule mining under incomplete evidence in ontological knowledge bases](https://archives.iw3c2.org/www2013/proceedings/p413.pdf)
                - [Reinforced anytime bottom up rule learning for knowledge graph completion](https://arxiv.org/abs/2004.04412)
            - **Phương pháp học máy (Machine Learning-based)**: sử dụng các thuật toán học máy với nhúng (embedding) để học từ chính cấu trúc đồ thị và dự đoán các thành phần thiếu.
                - [TransE: Translating Embeddings for Modeling Multi-relational Data](https://papers.nips.cc/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf)
                - [RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space](https://arxiv.org/abs/1902.10197)
            """)
    st.write("""
            Với sự phát triển của các mô hình ngôn ngữ lớn và lượng tri thức mà các mô hình này học được trong quá trình huấn luyện, có một số nghiên cứu gần đây đã thử áp dụng các mô hình ngôn ngữ lớn để thực hiện tác vụ hoàn thiện đồ thị tri thức.
                - (Survey) [Exploring large language models for knowledge graph completion](https://ieeexplore.ieee.org/abstract/document/10889242)
            """)