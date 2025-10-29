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
    một thực thể thuộc đồ thị tri thức $$X_i$$. Gọi $$\mathcal{G^*}$$ là mạng nhân quả mục tiêu cần khai thác từ bộ dữ liệu $$\mathcal{D}$$.
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
    
""")

st.divider()
