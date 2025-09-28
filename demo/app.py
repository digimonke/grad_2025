import streamlit as st
import pandas as pd
import networkx as nx
from causallearn.graph.GraphClass import CausalGraph
from causallearn.search.ConstraintBased.PC import pc
from causallearn.search.ScoreBased.GES import ges
from causallearn.search.FCMBased import lingam
from causallearn.utils.GraphUtils import GraphUtils
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

def read_file(file):
    df = None
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.xlsx') or file.name.endswith('.xls'):
        df = pd.read_excel(file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None
    
    return df
    
def normalize_data(df):
    df = df.dropna()  # Drop missing values for simplicity

    # find all string columns and convert to categorical codes
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns
    encoder = LabelEncoder()
    for col in categorical_columns:
        df[col] = encoder.fit_transform(df[col].astype(str))

    return df

def draw_graph(cg: CausalGraph, labels):
    G_nx = cg.to_nx_graph()   # convert to networkx graph
    pos = nx.spring_layout(G_nx, seed=42)

    plt.figure(figsize=(8,6))
    nx.draw(G_nx, pos, with_labels=True, labels=labels, arrows=True)
    plt.axis('off')

    st.pyplot(plt.gcf())
    plt.clf()

st.title("Causal Discovery App")
st.write("Upload an Excel file to run a causal inference algorithm and view the resulting graph.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    data = read_file(uploaded_file)
    st.write("Preview of data:", data.head())

    algo = st.selectbox(
        "Select Causal Discovery Algorithm",
        ["PC", "GES", "LiNGAM"]
    )

    if st.button("Run Causal Discovery"):
        # Convert to numpy
        data = normalize_data(data)
        data_np = data.to_numpy()

        if algo == "PC":
            cg = pc(data_np)  # alpha is significance level
        elif algo == "GES":
            cg = ges(data_np)
        elif algo == "LiNGAM":
            cg = lingam(data_np)

        pyd = GraphUtils.to_pydot(cg.G, labels=data.columns)
        png_bytes = pyd.create_png()   # returns PNG bytes
        st.image(png_bytes, caption="Causal graph (pydot)", use_column_width=True)