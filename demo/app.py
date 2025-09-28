import streamlit as st
import pandas as pd
import networkx as nx
from cdt.causality.graph import GES, LiNGAM, CAM, PC, GS
from pyvis.network import Network

st.title("Causal Discovery Demo")

uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:", data.head())

    if st.button("Run Causal Discovery"):
        # 1. Fit a graph model
        obj = PC()  # You can swap in GES, LiNGAM, etc.
        output_graph = obj.predict(data)

        # 2. Display as an interactive graph
        net = Network(notebook=False, directed=True)
        net.from_nx(output_graph)

        net.save_graph("graph.html")
        st.success("Graph generated!")
        st.components.v1.html(open("graph.html", 'r').read(), height=500)
