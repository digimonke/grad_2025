import streamlit as st
import utils

def draw_example_bn():
    G_true = utils.get_example_bn()
    G_mec = utils.get_example_cpdag()
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.caption("Đồ thị thật")
        utils.draw_dag(G_true, width_px=300)
    with col_right:
        st.caption(f"Lớp tương đương Markov của đồ thị thật")
        utils.draw_dag(G_mec, width_px=300)

st.title("Phương pháp được đề xuất")
st.info("""
    Mục tiêu của phương pháp được nghiên cứu là sử dụng dữ liệu ngoại vi phản ánh quan hệ của các thực thể được ghi nhân từ các nguồn khác nhau thay vì
    chỉ dựa vào cấu trúc đồ thị có sẵn như các phương pháp truyền thống. Mạng nhân quả mục tiêu $$\mathcal{G^*}$$ có thể được khai thác từ tập dữ
    liệu ngoại vi này có thể dùng để kiểm tra độ tin cậy của các cạnh mang quan hệ nhân quả thuộc đồ thị tri thức.
""")

st.header("Khai thác cấu trúc nhân quả từ dữ liệu")
st.markdown(r"""
    Xét bộ dữ liệu $$\mathcal{D}=X_{M \times N}$$ với $$M$$ dòng và $$N$$ cột. Mỗi cột trong bộ dữ liệu đại diện cho một biến $$D_i$$, tương ứng với
    một thực thể thuộc đồ thị tri thức $$x_i$$. Gọi $$\mathcal{G^*}$$ là mạng nhân quả mục tiêu cần khai thác từ bộ dữ liệu $$\mathcal{D}$$.
    Đa phần các phương pháp khai thác cấu trúc nhân quả từ dữ liệu chỉ có thể khôi phục được một lớp tương đương Markov $$\text{MEC}(\mathcal{G^*})$$ của mạng nhân quả mục tiêu
    nếu chỉ dựa trên phân phối của dữ liệu mà không có thêm giả định hoặc thông tin bổ sung nào khác.
""")

draw_example_bn()

st.markdown(r"""
    Ta có thể dùng thông tin có sẵn từ đồ thị tri thức, cụ thể là tập nút nguồn và nút lá của đồ thị tri thức.
    Ví dụ với tham số $$X_2$$ và $$X_4$$ trong lớp tương đương Markov ở trên, nếu từ đồ thị tri thức ta biết được
    rằng $$X_2$$ là nút nguồn (không có cạnh hướng vào), ta có thể sử dụng thông tin bổ sung này để khôi phục mạng
    mục tiêu từ lớp tương đương Markov.
""")

st.markdown(r"""
    Các thuật toán học cấu trúc nhân quả phổ biến như PC, GES hoặc LiNGAM đều hỗ trợ xử lý thông tin bổ sung dưới dạng ràng buộc phả hệ (ancestral constraints),
    bắt một tập nút phải được sắp xếp theo thứ tự trong chuỗi nhân quả. Ở ví dụ hiện tại, ta có thể cung cấp ràng buộc phả hệ rằng $$X_2$$ phải là
    tổ tiên (ancestor) của tất cả các nút khác trong đồ thị, từ đó giúp thu hẹp không gian tìm kiếm cấu trúc đồ thị nhân quả, cho ra kết quả chính xác hơn.
""")

st.divider()
st.header("Hoàn thiện đồ thị tri thức")

st.markdown(r"""
    Xét đồ thị tri thức $$\mathcal{K}$$ có tập nút $$V_{\mathcal{K}} = \{x^k_1, x^k_2, \ldots, x^k_n\}$$, tập cạnh $$E_{\mathcal{K}} = {(x^k_i, x^k_j) | x^k_i, x^k_j \in V_{\mathcal{K}}}$$
    và mạng nhân quả $$\mathcal{G^*}$$ với bộ tham số $$X = \{x^G_1, x^G_2, \ldots, x^G_n\}$$ và tập cạnh $$E_{\mathcal{G^*}} = {(x^G_i, x^G_j) | x^G_i, x^G_j \in X}$$.
    So khớp tập cạnh giữa hai đồ thị này, ta có tập cạnh lỗi tiềm năng
""")
st.latex(r"{E`}_{\mathcal{K}} = \{(x^k_i, x^k_j) \mid (x^k_i, x^k_j) \in E_{\mathcal{K}} \land (x^G_i, x^G_j) \notin E_{\mathcal{G^*}}\}")

st.markdown(r"""
    Một tập cạnh tồn tại trong đồ thị tri thức nhưng dữ liệu được ghi nhận thực tế về sự tương tác giữa các thực thể này không ủng hộ mối quan hệ nhân quả đó có thể được coi là cạnh lỗi.
    Tuy nhiên, không phải tất cả các cạnh trong tập cạnh lỗi tiềm năng $$E`_{\mathcal{K}}$$ đều thực sự là cạnh lỗi bởi chính mạng nhân quả có thể thiếu hoàn thiện
    do được xây dựng từ tập dữ liệu hữu hạn hoặc bị ảnh hưởng bởi nhiễu. VD: $$x_i = 0.001x_j + \mathcal{N}(0,1)$$
""")

st.markdown(r"""
    
""")