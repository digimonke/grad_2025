from causallearn.search.ConstraintBased.PC import pc
from causallearn.search.ScoreBased.GES import ges
import utils
import streamlit as st

st.title("Causal Inference")
st.write("Upload an Excel file to run a causal inference algorithm and view the resulting graph.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    data = utils.read_file(uploaded_file)
    st.write("Preview of data:", data.head())

    algo = st.selectbox(
        "Select Causal Discovery Algorithm",
        ["PC", "GES"]
    )

    if st.button("Run Causal Discovery"):
        # Convert to numpy
        data = utils.normalize_data(data)
        data_np = data.to_numpy()

        if algo == "PC":
            cg = pc(data_np)  # alpha is significance level
        elif algo == "GES":
            cg = ges(data_np)

        utils.draw_graph(cg, labels=list(data.columns), algo_name=algo)