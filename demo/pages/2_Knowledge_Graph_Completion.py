import streamlit as st
from sections import kgc_rule_based, kgc_ml_based, kgc_introduction

st.title("Hoàn thiện đồ thị tri thức")
tab = st.tabs(["Tổng quan","Phương pháp dựa trên quy tắc", "Phương pháp dựa trên học máy"])

with tab[0]:
    kgc_introduction.render()
with tab[1]:
    kgc_rule_based.render()
with tab[2]:
    kgc_ml_based.render()