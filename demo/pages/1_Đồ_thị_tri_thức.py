import streamlit as st
from sections import kg_introduction, kg_ontology, kg_incompleteness

st.title("Đồ thị tri thức")
tab = st.tabs(["Định nghĩa", "Bản thể học", "Vấn đề"])

with tab[0]:
    kg_introduction.render()
with tab[1]:
    kg_ontology.render()
with tab[2]:
    kg_incompleteness.render()