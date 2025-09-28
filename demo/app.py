import streamlit as st
import pandas as pd
from causallearn.search.ConstraintBased.PC import pc
from causallearn.search.ScoreBased.GES import ges
from causallearn.search.FCMBased import lingam
from causallearn.utils.GraphUtils import GraphUtils
import matplotlib.pyplot as plt

st.title("Causal Discovery App")
st.write("Upload an Excel file to run a causal inference algorithm and view the resulting graph.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Preview of data:", data.head())

    algo = st.selectbox(
        "Select Causal Discovery Algorithm",
        ["PC", "GES", "LiNGAM"]
    )

    if st.button("Run Causal Discovery"):
        # Convert to numpy
        data_np = data.to_numpy()

        if algo == "PC":
            cg = pc(data_np, alpha=0.05)  # alpha is significance level
        elif algo == "GES":
            cg = ges(data_np)
        elif algo == "LiNGAM":
            cg = lingam(data_np)

        st.success("Causal graph generated!")

        # Using causal-learn built-in graph plotting
        fig = plt.figure(figsize=(8,6))
        GraphUtils.plot_graph(cg.G, labels=data.columns)
        st.pyplot(fig)
