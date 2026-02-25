from __future__ import annotations
import pandas as pd

def optknock_or_fallback(model, candidate_rxns: list[str], product_rxn: str, max_k: int = 2) -> pd.DataFrame:
    """GLPK-first placeholder: uses enumerative fallback if cameo/advanced MILP unavailable."""
    from .deletion_screens import screen_combinatorial_reaction_deletions
    rows=[]
    for k in range(1, max_k+1):
        df = screen_combinatorial_reaction_deletions(model, candidate_rxns, k=k, product_rxn=product_rxn, max_sets=120)
        df['method'] = 'fallback_enumerative'
        df['k'] = k
        rows.append(df.head(20))
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
