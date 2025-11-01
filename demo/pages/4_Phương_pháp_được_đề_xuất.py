import streamlit as st
import utils

st.title("Phương pháp được đề xuất")
st.info(r"""
    Mục tiêu của phương pháp được nghiên cứu là sử dụng dữ liệu ngoại vi phản ánh quan hệ của các thực thể được ghi nhận từ các nguồn khác nhau thay vì
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

st.markdown("""
    Các nghiên cứu về khai thác cấu trúc nhân quả từ dữ liệu thường dựa trên hai giả định cơ bản sau:
    - **Giả định hoàn thiện nhân quả (Causal Sufficiency)**: Giả định rằng tất cả các biến trong hệ thống (causal variables) đều đã được quan sát và không có biến ẩn (latent confounding) nằm ngoài tập dữ liệu.
    - **Giả định Markov (Causal Markov Assumption)**: Mỗi biến trong mạng nhân quả là độc lập có điều kiện với các biến không phải là hậu duệ của nó, khi biết giá trị của các biến cha.
    - **Giả định trung thực (Faithfulness Assumption)**: Mọi độc lập có điều kiện trong phân phối dữ liệu đều phản ánh cấu trúc đồ thị nhân quả, tức là không có sự phụ thuộc ngẫu nhiên nào xảy ra.
""")

st.divider()
st.header("Hoàn thiện đồ thị tri thức")

st.subheader("Tập cạnh lỗi tiềm năng")
st.markdown(r"""
    Xét đồ thị tri thức $$\mathcal{K}$$ có tập nút và tập cạnh:
""")
col1, col2 = st.columns(2)
with col1:
    st.latex(r"V_{\mathcal{K}} = \{x^K_1, x^K_2, \ldots, x^K_n\}")
with col2:
    st.latex(r"E_{\mathcal{K}} = \{(x^K_i, x^K_j) | x^K_i, x^K_j \in V_{\mathcal{K}}\}")

st.markdown(r"""và mạng nhân quả $$\mathcal{G^*}$$ với bộ tham số và tập cạnh:""")
col1, col2 = st.columns(2)
with col1:
    st.latex(r"X = \{x^G_1, x^G_2, \ldots, x^G_n\} ")
with col2:
    st.latex(r"E_{\mathcal{G^*}} = \{(x^G_i, x^G_j) | x^G_i, x^G_j \in X\}")

st.markdown("Tập cạnh thuộc đồ thị tri thức nhưng không thuộc mạng nhân quả mục tiêu được định nghĩa là tập cạnh lỗi tiềm năng:")
st.latex(r"{E`}_{\mathcal{K}} = \{(x^K_i, x^K_j) \mid (x^K_i, x^K_j) \in E_{\mathcal{K}} \land (x^G_i, x^G_j) \notin E_{\mathcal{G^*}}\}")

st.markdown(r"""
    Một tập cạnh tồn tại trong đồ thị tri thức nhưng dữ liệu được ghi nhận thực tế về sự tương tác giữa các thực thể này không ủng hộ mối quan hệ nhân quả đó có thể được coi là cạnh lỗi.
    Tuy nhiên, không phải tất cả các cạnh trong tập cạnh lỗi tiềm năng $$E`_{\mathcal{K}}$$ đều thực sự là cạnh lỗi bởi chính mạng nhân quả có thể thiếu hoàn thiện
    do được xây dựng từ tập dữ liệu hữu hạn hoặc bị ảnh hưởng bởi nhiễu. VD: $$x_i = 0.001x_j + \mathcal{N}(0,1)$$.
""")
st.markdown(r"""
    Tuy nhiên, đây là một tập cạnh lỗi tiềm năng và là dự đoán tốt nhất trên toàn bộ tập dữ liệu có sẵn. Phương pháp được đề xuất sẽ
    tiếp tục đánh giá chất lượng của tập cạnh này thông qua lọc mẫu ổn định ngẫu nhiên.
""")

st.subheader("Lọc mẫu ổn định ngẫu nhiên (Stability Selection)")
st.markdown(r"""
    [**Lọc mẫu ổn định ngẫu nhiên (Stability Selection)**](https://arxiv.org/pdf/0809.2932) là một kỹ thuật lọc phổ biến trong thống kê và học máy, giúp cải thiện độ tin cậy của việc lấy mẫu bằng cách lặp lại quá trình lựa chọn trên các tập con khác nhau của dữ liệu.
    Thuật toán khai thác cấu trúc nhân quả từ dữ liệu sẽ được chạy nhiều lần trên các tập con ngẫu nhiên của bộ dữ liệu gốc. Mỗi lần chạy sẽ tạo ra một đồ thị nhân quả riêng biệt.
    Tần suất xuất hiện của mỗi cạnh trong số các đồ thị này sẽ được ghi nhận lại. Cuối cùng, các cạnh có tần suất xuất hiện vượt ngưỡng định sẵn sẽ được giữ lại như là các cạnh đáng tin cậy trong mạng nhân quả cuối cùng.
""")

st.markdown(r"""
    Nghiên cứu đặt tên cho module này là **Stable Edge Selection (SES)**. Kết quả của SES là một vector tần suất xuất hiện của một cạnh $$(x_i, x_j) \in {E`}_{\mathcal{K}}$$ trong số các đồ thị nhân quả được khai thác từ các tập con dữ liệu khác nhau:
""")
st.latex(r"\pi_{ij} = \frac{1}{B} \sum_{b=1}^{B} \mathbb{I}\{(x_i, x_j) \in E_{\hat{\mathcal{G}}_b}\} \quad \forall (x_i, x_j) \in {E`}_{\mathcal{K}}")

st.markdown(r"""
    SES sẽ hoạt động dựa trên một tập siêu tham số sau:
    - $$B$$: số lượng tập con và cũng là số lần chạy thuật toán khai thác cấu trúc nhân quả.
    - $$\alpha \in (0, 1)$$: tỷ lệ dữ liệu được chọn trong mỗi tập con so với bộ dữ liệu gốc.
    - $$\pi \in (0, 1)$$: ngưỡng tần suất xuất hiện để xác định cạnh đáng tin cậy.
""")

st.markdown(r"""
    Quá trình hoạt động của SES được mô tả như sau:
    1. Tạo $$B$$ tập con dữ liệu $$\mathcal{D}_b$$ bằng cách chọn ngẫu nhiên $$\alpha \times M$$ dòng từ bộ dữ liệu gốc $$\mathcal{D}$$.
    2. Trên mỗi tập con $$\mathcal{D}_b$$, chạy thuật toán khai thác cấu trúc nhân quả (ví dụ: PC, GES, LiNGAM) để thu được đồ thị nhân quả $$\hat{\mathcal{G}}_b$$.
    3. Ghi nhận tần suất xuất hiện $$\pi_{ij}$$ của mỗi cạnh $$(x_i, x_j) \in {E`}_{\mathcal{K}}$$ trong số các đồ thị $$\hat{\mathcal{G}}_b$$.
    4. Chọn lọc các cạnh đáng tin cậy dựa trên ngưỡng $$\pi$$:
       - Giữ lại cạnh $$(x_i, x_j)$$ nếu $$\pi_{ij} < \pi$$.
       - Loại bỏ cạnh $$(x_i, x_j)$$ nếu $$\pi_{ij} \geq \pi$$.
""")

st.markdown(r"""
    Kết quả cuối cùng của SES là một tập cạnh nhiễu đã được lọc, chỉ bao gồm các cạnh có tần suất xuất hiện thấp hơn ngưỡng định sẵn,
    từ đó giúp cải thiện độ tin cậy của tập cạnh lỗi được đề xuất loại bỏ khỏi đồ thị tri thức ban đầu.
""")
st.latex(r"E_{SES} = \{(x_i, x_j) \in {E`}_{\mathcal{K}} \mid \pi_{ij} < \pi\}")

st.subheader("Đồ thị tri thức hoàn thiện")
st.markdown(r"""
    Cuối cùng, đồ thị tri thức được hoàn thiện $$\mathcal{K*}$$ sẽ được xây dựng bằng cách loại bỏ các cạnh trong tập cạnh nhiễu $$E_{SES}$$ khỏi đồ thị tri thức ban đầu $$\mathcal{K}$$:
""")
st.latex(r"\mathcal{K*} = (V_{\mathcal{K}}, E_{\mathcal{K}} \setminus E_{SES})")