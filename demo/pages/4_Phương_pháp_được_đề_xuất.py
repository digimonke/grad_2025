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
st.markdown("""
    Mục tiêu của phương pháp được nghiên cứu là sử dụng dữ liệu ngoại vi phản ánh quan hệ của các thực thể được ghi nhân từ các nguồn khác nhau thay vì
    chỉ dựa vào cấu trúc đồ thị có sẵn như các phương pháp truyền thống.
    """)

st.markdown(r"""
    Xét bộ dữ liệu $$\mathcal{D}=X_{M \times N}$$ với $$M$$ dòng và $$N$$ cột. Mỗi cột trong bộ dữ liệu đại diện cho một biến $$D_i$$, tương ứng với
    một thực thể thuộc đồ thị tri thức $$X_i$$. Gọi $$\mathcal{G^*}$$ là đồ thị nhân quả Markov mục tiêu cần khai thác từ bộ dữ liệu $$\mathcal{D}$$.
    Đa phần các phương pháp khai thác cấu trúc nhân quả từ dữ liệu chỉ có thể khôi phục được một lớp tương đương Markov $$\text{MEC}(\mathcal{G^*})$$ của đồ thị nhân quả Markov mục tiêu
    nếu chỉ dựa trên phân phối của dữ liệu mà không có thêm giả định hoặc thông tin bổ sung nào khác.
""")

draw_example_bn()

st.markdown(r"""

""")