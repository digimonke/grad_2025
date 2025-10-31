from causallearn.utils.GraphUtils import GraphUtils
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
from networkx.drawing.nx_pydot import to_pydot
import matplotlib.pyplot as plt
from io import BytesIO
from typing import Optional, Union, List, Tuple, Iterable, Set
from sklearn.gaussian_process import GaussianProcessRegressor
from pgmpy.models import BayesianModel

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
        # edges: extract from networkx DiGraph if available
        try:
            if isinstance(cg, nx.DiGraph):
                for u, v in cg.edges():
                    # If nodes are indices, map via labels
                    if isinstance(u, int) and 0 <= u < len(labels) and isinstance(v, int) and 0 <= v < len(labels):
                        H.add_edge(labels[u], labels[v])
                    else:
                        H.add_edge(str(u), str(v))
        except Exception:
            pass
        pos = nx.spring_layout(H, seed=0)
        fig = plt.figure(figsize=(6, 4))
        nx.draw(H, pos, with_labels=True, node_color="#87cefa", node_size=1200, arrows=True)
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

def _dot_header(rankdir: str) -> List[str]:
    """Return a standard DOT header ensuring consistent styling across graphs."""
    return [
        "digraph G {",
        f"  rankdir={rankdir};",
        "  graph [splines=true, overlap=false, nodesep=0.4, ranksep=0.6, pad=0.2, margin=0.02];",
        "  node [shape=box, style=rounded, color=gray30, fontname=Helvetica, fontsize=12, penwidth=1.2];",
    ]

def pgmpy_model_to_dot(
    model,
    rankdir: str = "LR",
    title: str | None = None,
    highlight_edges: Optional[Iterable[Tuple[str, str]]] = None,
) -> str:
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

    # Normalize highlight set to strings for easy matching
    hset: Set[Tuple[str, str]] = set()
    if highlight_edges is not None:
        for u, v in highlight_edges:
            hset.add((str(u), str(v)))

    lines = _dot_header(rankdir)
    if title:
        lines.append(f"  labelloc=\"t\"; label=\"{title}\";")

    for n in nodes:
        safe = str(n).replace("\"", "\\\"")
        lines.append(f"  \"{safe}\";")

    for u, v in edges:
        su_raw, sv_raw = str(u), str(v)
        su = su_raw.replace("\"", "\\\"")
        sv = sv_raw.replace("\"", "\\\"")
        if (su_raw, sv_raw) in hset:
            lines.append(f"  \"{su}\" -> \"{sv}\" [color=\"#d62728\", penwidth=2.5];")
        else:
            lines.append(f"  \"{su}\" -> \"{sv}\" [penwidth=1.3];")

    lines.append("}")
    return "\n".join(lines)


def bnlearn_dag_to_dot(
    dag,
    highlight_edges: Optional[Iterable[Tuple[str, str]]] = None,
) -> str:
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
        return pgmpy_model_to_dot(model, rankdir="LR", highlight_edges=highlight_edges)

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
            lines = _dot_header("LR")
            for n in nodes:
                safe = str(n).replace("\"", "\\\"")
                lines.append(f"  \"{safe}\";")
            # Normalize highlight set
            hset: Set[Tuple[str, str]] = set()
            if highlight_edges is not None:
                for uu, vv in highlight_edges:
                    hset.add((str(uu), str(vv)))

            for u, v in edges:
                su_raw, sv_raw = str(u), str(v)
                su = su_raw.replace("\"", "\\\"")
                sv = sv_raw.replace("\"", "\\\"")
                if (su_raw, sv_raw) in hset:
                    lines.append(f"  \"{su}\" -> \"{sv}\" [color=\"#d62728\", penwidth=2.5];")
                else:
                    lines.append(f"  \"{su}\" -> \"{sv}\" [penwidth=1.3];")
            lines.append("}")
            return "\n".join(lines)
        except Exception:
            pass

    return "digraph G { rankdir=LR; }"


# ----------------------------
# Nonlinear SEM simulation
# ----------------------------

def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def simulate_nonlinear_sem(
    B: np.ndarray,
    n: int,
    sem_type: str,
    noise_scale: Optional[Union[float, List[float]]] = None,
) -> np.ndarray:
    """Simulate samples from a nonlinear SEM defined by adjacency B.

    Parameters
    ----------
    B : np.ndarray
        [d, d] binary adj matrix of DAG (1 indicates edge i->j).
    n : int
        Number of samples.
    sem_type : str
        'mlp', 'mim', 'gp', or 'gp-add'.
    noise_scale : float | list[float] | None
        Scale parameter(s) of additive Gaussian noises. If None, all ones.

    Returns
    -------
    np.ndarray
        [n, d] sample matrix.
    """
    
    d = B.shape[0]
    if noise_scale is None:
        scale_vec = np.ones(d)
    elif isinstance(noise_scale, (int, float)):
        scale_vec = np.ones(d) * float(noise_scale)
    else:
        scale_vec = np.asarray(noise_scale, dtype=float)
        assert scale_vec.shape[0] == d, "noise_scale length must equal number of variables"

    # Build graph and obtain topological order
    G = nx.DiGraph()
    G.add_nodes_from(range(d))
    srcs, dsts = np.where(B != 0)
    G.add_edges_from(zip(srcs.tolist(), dsts.tolist()))
    ordered_vertices = list(nx.topological_sort(G))
    assert len(ordered_vertices) == d, "Topological sorting failed to include all nodes"

    def _simulate_single_equation(X: np.ndarray, scale: float) -> np.ndarray:
        # X: [n, num_parents]
        z = np.random.normal(scale=scale, size=n)
        pa_size = X.shape[1]
        if pa_size == 0:
            return z
        if sem_type == 'Multilayer Perceptron':
            hidden = 100
            W1 = np.random.uniform(low=0.5, high=2.0, size=[pa_size, hidden])
            W1[np.random.rand(*W1.shape) < 0.5] *= -1
            W2 = np.random.uniform(low=0.5, high=2.0, size=hidden)
            W2[np.random.rand(hidden) < 0.5] *= -1
            x = sigmoid(X @ W1) @ W2 + z
        elif sem_type == 'Gaussian Process':
            gp = GaussianProcessRegressor()
            x = gp.sample_y(X, random_state=None).flatten() + z
        else:
            raise ValueError('unknown sem type')
        return x

    X = np.zeros([n, d], dtype=float)
    for j in ordered_vertices:
        parents = list(G.predecessors(j))
        X_pa = X[:, parents] if len(parents) > 0 else np.zeros((n, 0))
        X[:, j] = _simulate_single_equation(X_pa, float(scale_vec[j]))
    return X


def pgmpy_to_adjacency(model) -> Tuple[np.ndarray, List[str]]:
    """Convert a pgmpy BayesianModel to adjacency matrix and a topological node order."""
    # Use networkx for a stable topological order
    G = nx.DiGraph()
    nodes = list(model.nodes())
    G.add_nodes_from(nodes)
    G.add_edges_from(model.edges())
    topo_nodes = list(nx.topological_sort(G))
    idx = {n: i for i, n in enumerate(topo_nodes)}
    d = len(topo_nodes)
    B = np.zeros((d, d), dtype=int)
    for u, v in model.edges():
        B[idx[u], idx[v]] = 1
    return B, topo_nodes


def simulate_nonlinear_sem_from_pgmpy(
    model: BayesianModel,
    n: int,
    sem_type: str,
    noise_scale: Optional[Union[float, List[float]]] = None,
    as_dataframe: bool = True,
):
    """Simulate data from a pgmpy BayesianModel using a nonlinear SEM.

    Returns a pandas DataFrame with columns ordered topologically (or a numpy array if as_dataframe=False).
    """
    B, node_order = pgmpy_to_adjacency(model)
    X = simulate_nonlinear_sem(B, n=n, sem_type=sem_type, noise_scale=noise_scale)
    if as_dataframe:
        return pd.DataFrame(X, columns=node_order)
    return X, node_order

# ----------------------------
# LiNGAM (linear, non-Gaussian) simulation
# ----------------------------
def simulate_lingam(
    B: np.ndarray,
    n: int,
    coef_range: Tuple[float, float] = (0.5, 2.0),
    noise: str = "laplace",
    noise_scale: float = 1.0,
    seed: int | None = None,
) -> np.ndarray:
    """Simulate data from a linear, non-Gaussian acyclic model (LiNGAM).

    X_j = sum_{i in Pa(j)} w_{ij} X_i + e_j, where e_j are independent non-Gaussian noises.

    Parameters
    ----------
    B : np.ndarray
        [d, d] binary adj matrix of DAG (1 indicates edge i->j).
    n : int
        Number of samples.
    coef_range : (float, float)
        Uniform range for absolute edge coefficients. Signs are assigned randomly.
    noise : str
        One of {'laplace','exponential','mixture'}.
    noise_scale : float
        Scale for noise distribution (interpreted per distribution).
    seed : int | None
        Random seed for reproducibility.
    """

    d = B.shape[0]
    rng = np.random.default_rng(seed)

    # Build DAG and topological order
    G = nx.DiGraph()
    G.add_nodes_from(range(d))
    srcs, dsts = np.where(B != 0)
    G.add_edges_from(zip(srcs.tolist(), dsts.tolist()))
    ordered_vertices = list(nx.topological_sort(G))
    assert len(ordered_vertices) == d, "Topological sorting failed to include all nodes"

    # Random edge weights with random signs
    low, high = coef_range
    W = np.zeros_like(B, dtype=float)
    for i, j in zip(srcs.tolist(), dsts.tolist()):
        c = rng.uniform(low, high)
        s = rng.choice([-1.0, 1.0])
        W[i, j] = s * c

    def sample_noise(size: int) -> np.ndarray:
        if noise == "laplace":
            return rng.laplace(loc=0.0, scale=noise_scale, size=size)
        elif noise == "exponential":
            # shift to mean-zero
            return rng.exponential(scale=noise_scale, size=size) - noise_scale
        elif noise == "mixture":
            # mixture of Laplace and Gaussian (still non-Gaussian)
            return 0.5 * rng.laplace(0.0, noise_scale, size=size) + 0.5 * rng.normal(0.0, noise_scale, size=size)
        else:
            raise ValueError("unknown noise distribution for LiNGAM")

    X = np.zeros((n, d), dtype=float)
    for j in ordered_vertices:
        parents = list(G.predecessors(j))
        if parents:
            X[:, j] = X[:, parents] @ W[parents, j] + sample_noise(n)
        else:
            X[:, j] = sample_noise(n)
    return X

def simulate_lingam_from_pgmpy(
    model,
    n: int,
    coef_range: Tuple[float, float] = (0.5, 2.0),
    noise: str = "laplace",
    noise_scale: float = 1.0,
    seed: int | None = None
):
    """Wrapper to simulate LiNGAM data from a pgmpy BayesianModel.

    Returns a pandas DataFrame (topological order) by default.
    """
    B, node_order = pgmpy_to_adjacency(model)
    X = simulate_lingam(B, n=n, coef_range=coef_range, noise=noise, noise_scale=noise_scale, seed=seed)
    return pd.DataFrame(X, columns=node_order)


# ----------------------------
# DAG perturbation utilities
# ----------------------------
def add_random_edges_acyclic(
    model,
    n_add: int,
    seed: Optional[int] = None,
) -> Tuple[object, List[Tuple[str, str]]]:
    """Return a new pgmpy BayesianModel with up to n_add random edges added without creating cycles.

    - Does NOT modify the input model.
    - Preserves nodes; ignores/does not preserve CPDs (structure-only).
    - If fewer than n_add edges can be added without cycles, adds as many as possible.
    """

    nodes = list(model.nodes())
    existing = set(model.edges())

    # Build candidate edges (u->v) not present and u!=v
    candidates: List[Tuple[str, str]] = []
    for u in nodes:
        for v in nodes:
            if u == v:
                continue
            if (u, v) in existing:
                continue
            candidates.append((u, v))

    rng = np.random.default_rng(seed)
    rng.shuffle(candidates)

    # Maintain a working NX graph to check reachability efficiently
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(existing)

    added: List[Tuple[str, str]] = []
    for u, v in candidates:
        # Adding u->v would create a cycle iff there's already a path v->u
        if nx.has_path(G, v, u):
            continue
        G.add_edge(u, v)
        added.append((u, v))
        if len(added) >= n_add:
            break

    # Build a fresh BayesianModel with new edges
    if BayesianModel is not None:
        new_model = BayesianModel()
        new_model.add_nodes_from(nodes)
        new_model.add_edges_from(G.edges())
    else:
        # Fallback: return the edges via networkx graph and caller can wrap
        new_model = None  # type: ignore

    return new_model if new_model is not None else G, added


# ----------------------------
# Draw from adjacency with directed (1) and undirected (-1)
# ----------------------------

def adjacency_to_dot(
    W: np.ndarray,
    labels: Optional[List[str]] = None,
    rankdir: str = "LR",
    threshold: Optional[float] = None,
    tol: float = 1e-8,
) -> str:
    """Build DOT from an adjacency matrix with entries {0, 1, -1}.

    - 1 means directed edge i->j
    - -1 means undirected edge between i and j (we draw once with dir="none").
    - 0 means no edge.
    If both a directed and undirected indicator are present between i and j, directed takes precedence.

    Also supports weighted adjacency matrices by using a threshold or tolerance:
    - If threshold is None, any abs(W[i,j]) > tol is considered non-zero.
    - If both directions i->j and j->i are non-zero within tolerance, the edge is rendered undirected
      unless one direction has strictly larger absolute weight (then we pick that direction).
    """
    if W.ndim != 2 or W.shape[0] != W.shape[1]:
        raise ValueError("W must be a square matrix")
    d = W.shape[0]
    if labels is None:
        labels = [f"X{i+1}" for i in range(d)]
    if len(labels) != d:
        raise ValueError("labels length must match W dimension")

    def nonzero(x: float) -> bool:
        thr = tol if threshold is None else float(threshold)
        return abs(float(x)) > thr

    directed: List[Tuple[int, int]] = []
    undirected_pairs: Set[Tuple[int, int]] = set()

    for i in range(d):
        for j in range(i + 1, d):
            a = float(W[i, j])
            b = float(W[j, i])
            ai = nonzero(a)
            bj = nonzero(b)
            if ai and bj:
                # both directions present -> pick stronger direction if clearly stronger, else undirected
                if abs(a) > abs(b) + tol:
                    directed.append((i, j))
                elif abs(b) > abs(a) + tol:
                    directed.append((j, i))
                else:
                    undirected_pairs.add((i, j))
            elif ai:
                directed.append((i, j))
            elif bj:
                directed.append((j, i))

    lines = _dot_header(rankdir)

    for n in labels:
        safe = str(n).replace("\"", "\\\"")
        lines.append(f"  \"{safe}\";")

    for i, j in directed:
        su = str(labels[i]).replace("\"", "\\\"")
        sv = str(labels[j]).replace("\"", "\\\"")
        lines.append(f"  \"{su}\" -> \"{sv}\" [penwidth=1.3];")

    for i, j in undirected_pairs:
        su = str(labels[i]).replace("\"", "\\\"")
        sv = str(labels[j]).replace("\"", "\\\"")
        lines.append(f"  \"{su}\" -> \"{sv}\" [dir=none, penwidth=1.3];")

    lines.append("}")
    return "\n".join(lines)


def adjacency_to_edge_set(
    W: np.ndarray,
    labels: Optional[List[str]] = None,
    threshold: Optional[float] = None,
    tol: float = 1e-8,
) -> Set[Tuple[str, str]]:
    """Return a set of directed edges (u, v) from an adjacency/weight matrix.

    - Uses same threshold logic as adjacency_to_dot.
    - If both directions i<->j are present above threshold, the stronger direction is chosen;
      if nearly equal within tol, returns neither direction to avoid ambiguity.
    """
    if W.ndim != 2 or W.shape[0] != W.shape[1]:
        raise ValueError("W must be a square matrix")
    d = W.shape[0]
    if labels is None:
        labels = [f"X{i+1}" for i in range(d)]
    if len(labels) != d:
        raise ValueError("labels length must match W dimension")

    def nonzero(x: float) -> bool:
        thr = tol if threshold is None else float(threshold)
        return abs(float(x)) > thr

    edges: Set[Tuple[str, str]] = set()
    for i in range(d):
        for j in range(i + 1, d):
            a = float(W[i, j])
            b = float(W[j, i])
            ai = nonzero(a)
            bj = nonzero(b)
            if ai and bj:
                if abs(a) > abs(b) + tol:
                    edges.add((str(labels[i]), str(labels[j])))
                elif abs(b) > abs(a) + tol:
                    edges.add((str(labels[j]), str(labels[i])))
                else:
                    # ambiguous; skip adding either direction
                    pass
            elif ai:
                edges.add((str(labels[i]), str(labels[j])))
            elif bj:
                edges.add((str(labels[j]), str(labels[i])))
    return edges