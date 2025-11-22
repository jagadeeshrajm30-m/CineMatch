from typing import List, Set
import numpy as np

def precision_at_k(recommended: List[int], relevant: Set[int], k: int = 10) -> float:
    if k == 0:
        return 0.0
    rec_k = recommended[:k]
    hits = len(set(rec_k) & relevant)
    return hits / k

def recall_at_k(recommended: List[int], relevant: Set[int], k: int = 10) -> float:
    if not relevant:
        return 0.0
    rec_k = recommended[:k]
    hits = len(set(rec_k) & relevant)
    return hits / len(relevant)

def ndcg_at_k(recommended: List[int], relevant: Set[int], k: int = 10) -> float:
    rec_k = recommended[:k]
    gains = [1.0 if item in relevant else 0.0 for item in rec_k]
    discounts = [1.0 / np.log2(i + 2) for i in range(len(gains))]
    dcg = sum(g * d for g, d in zip(gains, discounts))
    ideal_gains = sorted(gains, reverse=True)
    idcg = sum(g * d for g, d in zip(ideal_gains, discounts))
    if idcg == 0:
        return 0.0
    return dcg / idcg
