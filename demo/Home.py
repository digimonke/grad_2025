import streamlit as st
from config import AUTHOR, SUPERVISOR, CONTACT_EMAIL

# --- Sidebar
with st.sidebar:
	st.subheader("Đại học Quốc gia Thành phố Hồ Chí Minh")
	st.subheader("Trường Đại học Khoa Học Tự Nhiên")
	st.markdown(f"**Giảng viên hướng dẫn:** {SUPERVISOR}")
	st.markdown(f"**Học viên thực hiện:** {AUTHOR}")
	if CONTACT_EMAIL:
		st.caption(f"Email: {CONTACT_EMAIL}")

st.title("Hoàn thiện đồ thị tri thức thông qua khai thác cấu trúc nhân quả từ dữ liệu")
st.markdown(":green-badge[Knowledge Graph] :green-badge[Knowledge Graph Completion] :green-badge[Causal Structure Learning]")