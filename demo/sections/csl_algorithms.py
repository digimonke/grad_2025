import streamlit as st

def constraint_based_methods():
    st.subheader("Nhóm phương pháp sử dụng ràng buộc")
    st.markdown(r"""
        Nhóm phương pháp sử dụng ràng buộc hoạt động dựa trên việc kiểm định các mệnh đề độc lập có điều kiện trong dữ liệu quan sát để xây dựng đồ thị nhân quả Markov.
        Thuật toán PC (Peter-Clark) là một ví dụ kinh điển của nhóm phương pháp này và được sử dụng như một baseline để kiểm định các phương pháp mới.
        PC bắt đầu với một đồ thị đầy đủ (fully-connected graph) và lược bỏ các cạnh tuần tự dựa trên tập các mệnh đề độc lập có điều kiện được kiểm định từ dữ liệu.
    """)
    st.markdown(r"""
        Lợi thế của nhóm phương pháp này là hiệu quả trong tính toán và tính khả diễn dựa trên tập mệnh đề độc lập có điều kiện.
        Tuy nhiên, kết quả của các thuật toán phụ thuộc vào chất lượng của khâu kiểm định độc lập có điều kiện, vốn có thể bị ảnh hưởng bởi kích thước mẫu và các giả định về phân phối dữ liệu.
    """)

def score_based_methods():
    st.subheader("Nhóm phương pháp sử dụng điểm đánh giá")
    st.markdown(r"""
        Nhóm phương pháp sử dụng điểm đánh giá xây dựng cấu trúc nhân quả sử dụng một hàm tính điểm để đánh giá cấu trúc nhân quả, nhắm đến việc tìm ra cấu trúc nhân quả với điểm tối ưu nhất.
        Hàm tính điểm được chọn dựa trên loại dữ liệu và các giả định về mô hình ví dụ như BDeu cho dữ liệu rời rạc, BIC/MDL cho dữ liệu liên tục.
        Các thuật toán thuộc nhóm này như GES (Greedy Equivalence Search) hoặc GOBNILP (Greedy Optimization for Bayesian Network structure learning using Integer Linear Programming) 
        sử dụng chiến thuật tìm kiếm với cực trị cục bộ (greedy search) để tìm ra cấu trúc nhân quả với điểm số tối ưu.
    """)
    st.latex(r"\text{Score}(G;D) = \log(P(D \mid G)) - \text{ComplexityPenalty}(G)")
    st.markdown(r"""
        Trong đó:
        - $$(G)$$ là cấu trúc đồ thị nhân quả.
        - $$(D)$$ là dữ liệu quan sát.
        - $$(\text{ComplexityPenalty}(G))$$ là độ phức tạp của cấu trúc đồ thị \(G\).
    """)

    st.markdown(r"""
        Ưu điểm của nhóm phương pháp này là khả năng tìm kiếm toàn cục và tính linh hoạt trong việc lựa chọn hàm điểm đánh giá phù hợp với đặc tính dữ liệu.
        Tuy nhiên, quá trình tối ưu hóa có thể tốn kém về mặt tính toán và dễ bị mắc kẹt trong các cực trị cục bộ.
    """)

def render():
    st.header("Thuật toán")

    st.write("Các thuật toán xấy dựng cấu trúc nhân quả từ dữ liệu có thể được phân loại thành 3 nhóm chính là **nhóm phương pháp sử dụng ràng buộc**, " \
    "**nhóm phương pháp sử dụng điểm đánh giá** và **nhóm phương pháp tổng hợp** (constraint based, score based, hybrid methods).")

    st.markdown(
        r"""
        Thông thường, các phương pháp này hoạt động dựa trên ít nhất 1 trong 2 giả định sau về phân phối dữ liệu:
        - **Giả định trung thực** (Faithfulness Assumption): Mọi mệnh đề độc lập có điều kiện trong phân phối dữ liệu đều được phản ánh trong đồ thị nhân quả Markov. Giả định này ràng buộc đồ thị nhân quả Markov mục tiêu phải mô hình hoá toàn bộ tập mệnh đề độc lập có điều kiện trong phân phối dữ liệu.
        """
    )
    st.latex(r"\mathcal{I}(\mathbb{P}_X) \subseteq \mathcal{I}(\mathcal{G})")
    st.markdown(r"""- **Giả định phân phối hoàn thiện về mặt nhân quả** (Causal Sufficiency Assumption): Không tồn tại biến ẩn (latent variable) nào là nguyên nhân chung của hai hoặc nhiều biến quan sát trong phân phối dữ liệu.
                Giả định này loại bỏ khả năng xuất hiện các cạnh vô hướng (bi-directed edge) trong đồ thị nhân quả Markov mục tiêu do ảnh hưởng của biến ẩn.""")
    
    constraint_based_methods()

    score_based_methods()
