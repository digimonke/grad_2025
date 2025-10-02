import streamlit as st
from sections import kg_introduction

def tab_ontology():
    st.header("Bản thể học")
    st.write("""
    Bản thể học (Ontology) trong ngữ cảnh của đồ thị tri thức đề cập đến một tập hợp các khái niệm và mối quan hệ giữa chúng trong một lĩnh vực cụ thể.
    Nó cung cấp một khung cấu trúc để tổ chức và phân loại thông tin, giúp định nghĩa rõ ràng các thực thể và cách chúng tương tác với nhau.
    """)

def tab_incompleteness():
    st.header("Tính không đầy đủ")
    st.write("""
    Tính không đầy đủ của đồ thị tri thức đề cập đến thực tế rằng không phải tất cả các mối quan hệ và thực thể trong thế giới thực đều được biểu diễn trong đồ thị.
    Điều này có thể do nhiều nguyên nhân, bao gồm hạn chế trong việc thu thập dữ liệu, sai sót trong quá trình trích xuất thông tin, hoặc sự phức tạp vốn có của các mối quan hệ ngữ nghĩa.
    """)
    st.write("""
    Ví dụ, trong một đồ thị tri thức về y học, có thể thiếu các mối quan hệ quan trọng giữa các triệu chứng và bệnh tật do dữ liệu không đầy đủ hoặc lỗi trong quá trình trích xuất thông tin từ văn bản y khoa.
    Tính không đầy đủ này có thể ảnh hưởng đến hiệu quả của các ứng dụng dựa trên đồ thị tri thức, như hệ thống gợi ý hoặc trợ lý ảo, khi chúng không thể truy xuất thông tin cần thiết để đưa ra quyết định chính xác.
    """)

st.title("Đồ thị tri thức")
tab = st.tabs(["Định nghĩa", "Bản thể học", "Vấn đề"])

with tab[0]:
    kg_introduction.tab_introduction()
with tab[1]:
    tab_ontology()
with tab[2]:
    tab_incompleteness()