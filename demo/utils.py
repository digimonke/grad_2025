from causallearn.utils.GraphUtils import GraphUtils
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
from causallearn.graph.GraphClass import CausalGraph
from networkx.drawing.nx_pydot import to_pydot
import matplotlib.pyplot as plt
from io import BytesIO

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

def draw_graph(cg: CausalGraph, labels, algo_name, width_px: int | None = None):
    g = cg.G if algo_name == "PC" else cg['G']
    try:
        pyd = GraphUtils.to_pydot(g, labels=labels)
        png_bytes = pyd.create_png()   # returns PNG bytes
        if width_px is not None:
            st.image(png_bytes, caption="Causal graph (pydot)", width=width_px)
        else:
            st.image(png_bytes, caption="Causal graph (pydot)", use_container_width=True)
    except Exception as e:
        # Fallback: draw with NetworkX
        st.warning(f"Không thể render bằng Graphviz/pydot ({e}). Dùng NetworkX thay thế.")
        H = nx.DiGraph()
        # causal-learn Graph has nodes as indices 0..n-1
        for i, lab in enumerate(labels):
            H.add_node(lab)
        # edges: try to get from pydot conversion; fallback to adjacency matrix
        try:
            # Attempt to extract adjacency from cg directly
            for i in range(len(labels)):
                for j in range(len(labels)):
                    if g.graph[i][j] == 1:
                        H.add_edge(labels[i], labels[j])
        except Exception:
            pass
        pos = nx.spring_layout(H, seed=0)
        fig = plt.figure(figsize=(6, 4))
        nx.draw(H, pos, with_labels=True, node_color="#87cefa", node_size=1200, arrows=True)
        from io import BytesIO
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        plt.close(fig)
        img = buf.getvalue()
        if width_px is not None:
            st.image(img, caption="Causal graph (NetworkX)", width=width_px)
        else:
            st.image(img, caption="Causal graph (NetworkX)", use_container_width=True)


# ----------------------------
# Synthetic 5-node BN utilities
# ----------------------------

def get_true_bn():
    """Return a 5-node ground-truth DAG used for toy sampling."""
    G = nx.DiGraph()
    G.add_nodes_from(["X1", "X2", "X3", "X4", "X5"]) 
    # Structure: X1->X3, X2->X3, X2->X4, X3->X5, X4->X5
    G.add_edges_from([
        ("X1", "X3"),
        ("X2", "X3"),
        ("X2", "X4"),
        ("X3", "X5"),
        ("X4", "X5"),
    ])
    return G


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def sample_from_true_bn(n_samples: int = 1000, seed: int | None = 0) -> pd.DataFrame:
    """Sample binary data from the predefined 5-node BN using ancestral sampling.

    Nodes: X1, X2 (roots); X3 = f(X1, X2); X4 = f(X2); X5 = f(X3, X4)
    """
    rng = np.random.default_rng(seed)
    X1 = rng.binomial(1, 0.5, size=n_samples)
    X2 = rng.binomial(1, 0.5, size=n_samples)
    # Logistic CPDs produce probabilities in (0,1)
    p_X3 = _sigmoid(-1.0 + 1.2 * X1 + 1.2 * X2)
    X3 = rng.binomial(1, p_X3)
    p_X4 = _sigmoid(-1.0 + 1.1 * X2)
    X4 = rng.binomial(1, p_X4)
    p_X5 = _sigmoid(-1.5 + 1.2 * X3 + 1.2 * X4)
    X5 = rng.binomial(1, p_X5)
    df = pd.DataFrame({"X1": X1, "X2": X2, "X3": X3, "X4": X4, "X5": X5})
    return df


def draw_true_bn_graph(G: nx.DiGraph, width_px: int | None = None):
    """Render the ground-truth DAG using pydot and display in Streamlit."""
    try:
        pyd = to_pydot(G)
        png_bytes = pyd.create_png()
        if width_px is not None:
            st.image(png_bytes, caption="Ground-truth DAG (5-node BN)", width=width_px)
        else:
            st.image(png_bytes, caption="Ground-truth DAG (5-node BN)", use_container_width=True)
    except Exception as e:
        st.warning(f"Không thể render bằng Graphviz/pydot ({e}). Dùng NetworkX thay thế.")
        pos = nx.spring_layout(G, seed=0)
        fig = plt.figure(figsize=(6, 4))
        nx.draw(G, pos, with_labels=True, node_color="#ffcc00", node_size=1200, arrows=True)
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        plt.close(fig)
        img = buf.getvalue()
        if width_px is not None:
            st.image(img, caption="Ground-truth DAG (5-node BN)", width=width_px)
        else:
            st.image(img, caption="Ground-truth DAG (5-node BN)", use_container_width=True)