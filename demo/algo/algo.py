import dagma
import numpy as np
import pandas as pd
import torch
from dagma.nonlinear import DagmaMLP, DagmaNonlinear
import lingam
from lingam.utils import make_prior_knowledge
from collections import defaultdict
from typing import Callable, Iterable, List, Sequence, Tuple, Optional

# Local utilities
from utils import adjacency_to_edge_set

def main():
    raise NotImplementedError("This is a placeholder for the main algorithm module.")

def linear_causal_discovery(data: pd.DataFrame) -> np.ndarray:
    """Run DirectLiNGAM and return adjacency with our convention B[i,j] = i -> j.

    Note: In the lingam package, adjacency_matrix_[i, j] is the coefficient of X_j in the equation for X_i,
    i.e., it encodes j -> i. Our visualizers (adjacency_to_dot) assume B[i, j] means i -> j.
    Therefore we transpose before returning.
    """
    model = lingam.DirectLiNGAM()
    model.fit(data)

    # lingam uses (row i, col j) = j -> i; transpose to get i -> j
    return model.adjacency_matrix_.T

def nonlinear_causal_discovery(data: pd.DataFrame) -> np.ndarray:
    eq_model = DagmaMLP(dims=[data.shape[1], 10, 1], bias=True, dtype=torch.double) # create the model for the structural equations, in this case MLPs
    model = DagmaNonlinear(eq_model, dtype=torch.double) # create the model for DAG learning
    W_est = model.fit(data.values, lambda1=0.02, lambda2=0.005) # fit the model with L1 reg. (coeff. 0.02) and L2 reg. (coeff. 0.005)

    return W_est # return the estimated weighted adjacency matrix


def stability_subsampling(
    df: pd.DataFrame,
    candidate_edges: Sequence[Tuple[str, str]],
    *,
    B: int = 50,
    subsample_frac: float = 0.67,
    disc_thresh: float = 0.3,
    seed: int = 7,
    pi_threshold: Optional[float] = None,
    discovery_fn: Optional[Callable[[pd.DataFrame], np.ndarray]] = None,
) -> Tuple[pd.DataFrame, List[Tuple[str, str]], List[Tuple[str, str]]]:
    """
    Run stability subsampling by repeatedly subsampling rows, running causal discovery,
    and counting how often each candidate edge appears.

    Args:
        df: DataFrame of shape (n_samples, n_vars).
        candidate_edges: iterable of (u, v) edges to score.
        B: number of repetitions.
        subsample_frac: fraction of rows per repetition (without replacement).
        disc_thresh: threshold to convert weighted adjacency to edge set.
        seed: base random seed; iteration uses seed + b.
        pi_threshold: if provided, also partition results into (freq > pi) and (freq <= pi).
        discovery_fn: function mapping DataFrame -> weighted adjacency (numpy array) where W[i, j] denotes i -> j.

    Returns:
        (df_results, false_positive_edges, recommended_removals)
        - df_results: DataFrame with columns [u, v, frequency] sorted descending by frequency.
        - false_positive_edges: list of (u, v) with freq > pi_threshold (empty if pi_threshold is None).
        - recommended_removals: list of (u, v) with freq <= pi_threshold (empty if pi_threshold is None).
    """
    if discovery_fn is None:
        discovery_fn = linear_causal_discovery

    labels: List[str] = list(df.columns)
    n = df.shape[0]
    m = max(1, int(subsample_frac * n))

    # Normalize candidate edges to strings
    cand_edges: List[Tuple[str, str]] = [(str(u), str(v)) for (u, v) in candidate_edges]

    counts = defaultdict(int)

    for b in range(int(B)):
        df_b = df.sample(n=m, replace=False, random_state=int(seed + b))
        try:
            W_b = discovery_fn(df_b)
            edges_b = adjacency_to_edge_set(W_b, labels=labels, threshold=float(disc_thresh))
        except Exception:
            edges_b = set()

        edges_b = {(str(u), str(v)) for (u, v) in edges_b}
        for (u, v) in cand_edges:
            if (u, v) in edges_b:
                counts[(u, v)] += 1

    # Aggregate
    results = []
    for (u, v) in cand_edges:
        freq = counts[(u, v)] / float(B)
        results.append({"u": u, "v": v, "frequency": freq})

    df_results = pd.DataFrame(results).sort_values(by="frequency", ascending=False, ignore_index=True)

    false_pos: List[Tuple[str, str]] = []
    keep_remove: List[Tuple[str, str]] = []
    if pi_threshold is not None:
        false_pos = [(r["u"], r["v"]) for _, r in df_results.iterrows() if r["frequency"] > float(pi_threshold)]
        keep_remove = [(r["u"], r["v"]) for _, r in df_results.iterrows() if r["frequency"] <= float(pi_threshold)]

    return df_results, false_pos, keep_remove