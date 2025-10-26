import streamlit as st
from config import AUTHOR, SUPERVISOR, CONTACT_EMAIL

# --- Page title and tags ---
st.title("Hoàn thiện đồ thị tri thức với cấu trúc nhân quả được khai thác từ dữ liệu")
st.markdown(":green-badge[Knowledge Graph] :green-badge[Knowledge Graph Completion] :green-badge[Causal Structure Learning]")

with st.container(border=True):
    st.subheader("Đại học Quốc gia Thành phố Hồ Chí Minh")
    st.subheader("Trường Đại học Khoa Học Tự Nhiên")
    st.markdown(f"**Giảng viên hướng dẫn:** {SUPERVISOR}")
    st.markdown(f"**Học viên thực hiện:** {AUTHOR}")
    if CONTACT_EMAIL:
        st.caption(f"Email: {CONTACT_EMAIL}")

st.header("Giới thiệu nội dung luận văn")
st.write(
    """
    Đồ thị tri thức (Knowledge Graph - KG) được ứng dụng rộng rãi trong nhiều lĩnh vực và hỗ trợ nhiều tác vụ khác nhau.
    Tuy nhiên, đa phần nội dung của các đồ thị tri thức này đều tồn tại sự thiếu chính xác, thiếu nhất quán và thiếu toàn vẹn về mặt tri thức.
    Các phương pháp truyền thống để sửa lỗi và hoàn thiện các đồ thị tri thức này thường dựa vào các thao tác thủ công hoặc các kỹ thuật học máy.
    Cả hai hướng tiếp cận này đều có những hạn chế riêng về tính chủ quan của chuyên gia hoặc nhiễu từ dữ liệu huấn luyện.
    Với sự bùng nổ của các mô hình ngôn ngữ lớn, một số nghiên cứu gần đây đã thử sức trong việc khai thác thông tin bổ trợ từ văn bản nhằm ứng dụng cho việc hoàn thiện đồ thị tri thức.
    Dữ liệu là một dạng tài nguyên khác phản ánh sự tương tác của các sự vật hiện tượng trong thế giới thực và có tiềm năng ứng dụng để hỗ trợ việc hoàn thiện đồ thị tri thức.
    Tuy đa dạng và dư thừa trong thời đại dữ liệu lớn, việc khai thác những tương tác và quan hệ giữa các biến trong dữ liệu vẫn là một thách thức với giới nghiên cứu.
    Nội dung của nghiên cứu này thử sức với việc việc khai thác quan hệ nhân quả giữa các tham số thuộc dữ liệu để hỗ trợ việc hoàn thiện đồ thị tri thức.
    Phương pháp được đề xuất từ nghiên cứu đầu tiên sử dụng nội dung của đồ thị tri thức như một nguồn thông tin bổ sung để cải thiện chất lượng cho tác vụ khai thác cấu trúc nhân quả của dữ liệu.
    Cấu trúc này sau đó sẽ được sử dụng để cải thiện độ chính xác và tính toàn vẹn của đồ thị tri thức, loại bỏ các cạnh không chính xác khỏi đồ thị.
    """
)

st.info("""
    Trang web này được chia thành các đề mục như ở thanh điều hướng bên trái:
    - **Đồ thị tri thức**: Giới thiệu tổng quan về đồ thị tri thức, các thành phần cấu thành, vấn đề thiếu toàn vẹn trong đồ thị tri thức.
    - **Hoàn thiện đồ thị tri thức**: Trình bày các phương pháp hoàn thiện đồ thị tri thức kinh điển được phân loại thành hai nhóm chính: phương pháp dựa trên quy tắc và phương pháp dựa trên học máy.
    - **Khai thác mạng quan hệ nhân quả từ dữ liệu**: Giới thiệu tổng quan về khai thác mạng quan hệ nhân quả từ dữ liệu, các khái niệm nền tảng và các thuật toán phổ biến.
""")