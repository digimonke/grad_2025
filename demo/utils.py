from causallearn.utils.GraphUtils import GraphUtils
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import pandas as pd
from causallearn.graph.GraphClass import CausalGraph

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

def draw_graph(cg: CausalGraph, labels, algo_name):
    g = cg.G if algo_name == "PC" else cg['G']

    pyd = GraphUtils.to_pydot(g, labels=labels)
    png_bytes = pyd.create_png()   # returns PNG bytes
    st.image(png_bytes, caption="Causal graph (pydot)", use_container_width=True)