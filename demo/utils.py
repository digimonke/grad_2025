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

def draw_graph(cg: nx.DiGraph, labels, width_px: int | None = None):
    try:
        pyd = GraphUtils.to_pydot(cg, labels=labels)
        png_bytes = pyd.create_png()   # returns PNG bytes
        if width_px is not None:
            st.image(png_bytes, width=width_px)
        else:
            st.image(png_bytes, use_container_width=True)
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

def get_example_bn():
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

def get_example_cpdag():
    """Return a 5-node CPDAG using a single NetworkX DiGraph for rendering.

    We encode the undirected edge X2—X4 as a single edge with Graphviz
    attribute dir="none" so it draws without arrowheads, while keeping other
    edges directed. This avoids the undesirable double-arrows for that pair.
    """
    G = nx.DiGraph()
    G.add_nodes_from(["X1", "X2", "X3", "X4", "X5"]) 

    # Directed edges
    G.add_edges_from([
        ("X1", "X3"),
        ("X2", "X3"),
        ("X3", "X5"),
        ("X4", "X5"),
    ])

    # Undirected visually: one edge with no arrowheads in Graphviz
    # NetworkX -> pydot will pass the 'dir' attribute through to Graphviz (dot)
    G.add_edge("X2", "X4", dir="none")
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


def draw_dag(G: nx.DiGraph, width_px: int | None = None):
    """Render the ground-truth DAG using pydot and display in Streamlit."""
    try:
        pyd = to_pydot(G)
        png_bytes = pyd.create_png()
        if width_px is not None:
            st.image(png_bytes, width=width_px)
        else:
            st.image(png_bytes, use_container_width=True)
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


# ----------------------------
# bnlearn / pgmpy helpers
# ----------------------------

def pgmpy_model_to_dot(model, rankdir: str = "LR", title: str | None = None) -> str:
    """Build a Graphviz DOT string from a pgmpy BayesianModel without requiring graphviz/pydot.

    Parameters
    - model: pgmpy.models.BayesianModel or any object exposing .nodes() and .edges()
    - rankdir: 'LR' (left-to-right) or 'TB' (top-to-bottom)
    - title: optional graph label
    """
    # Gather nodes and edges defensively
    try:
        nodes = list(model.nodes())
    except Exception:
        nodes = []
    try:
        edges = list(model.edges())
    except Exception:
        edges = []

    lines = ["digraph G {"]
    lines.append(f"  rankdir={rankdir};")
    lines.append("  node [shape=box, style=rounded, color=gray30, fontname=Helvetica];")
    if title:
        lines.append(f"  labelloc=\"t\"; label=\"{title}\";")

    for n in nodes:
        safe = str(n).replace("\"", "\\\"")
        lines.append(f"  \"{safe}\";")

    for u, v in edges:
        su = str(u).replace("\"", "\\\"")
        sv = str(v).replace("\"", "\\\"")
        lines.append(f"  \"{su}\" -> \"{sv}\";")

    lines.append("}")
    return "\n".join(lines)


def bnlearn_dag_to_dot(dag) -> str:
    """Accept a bnlearn DAG object and return a DOT string.

    bnlearn.import_DAG(...) typically returns a dict with keys like 'model' and 'adjmat'.
    This function tries 'model' first, then falls back to adjacency matrix if present.
    """
    model = None
    adj = None
    if isinstance(dag, dict):
        model = dag.get("model")
        adj = dag.get("adjmat")
    else:
        model = getattr(dag, "model", None)
        adj = getattr(dag, "adjmat", None)

    if model is not None:
        return pgmpy_model_to_dot(model, rankdir="LR")

    if adj is not None:
        try:
            nodes = list(adj.columns)
            edges = []
            for i, src in enumerate(nodes):
                for j, dst in enumerate(nodes):
                    try:
                        val = adj.iloc[i, j]
                    except Exception:
                        continue
                    if isinstance(val, (int, float)) and val != 0:
                        edges.append((src, dst))
            lines = [
                "digraph G {",
                "  rankdir=LR;",
                "  node [shape=box, style=rounded, color=gray30, fontname=Helvetica];",
            ]
            for n in nodes:
                safe = str(n).replace("\"", "\\\"")
                lines.append(f"  \"{safe}\";")
            for u, v in edges:
                su = str(u).replace("\"", "\\\"")
                sv = str(v).replace("\"", "\\\"")
                lines.append(f"  \"{su}\" -> \"{sv}\";")
            lines.append("}")
            return "\n".join(lines)
        except Exception:
            pass

    return "digraph G { rankdir=LR; }"