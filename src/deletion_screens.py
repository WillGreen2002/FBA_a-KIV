from __future__ import annotations
import itertools
import pandas as pd
import cobra

def screen_single_reaction_deletions(model: cobra.Model, candidates: list[str], product_rxn: str) -> pd.DataFrame:
    rows=[]
    for rid in candidates:
        with model:
            if rid not in model.reactions:
                continue
            model.reactions.get_by_id(rid).knock_out()
            model.objective = product_rxn
            sol = model.optimize()
            rows.append({'ko': rid, 'status': sol.status, 'product_flux': sol.objective_value})
    return pd.DataFrame(rows).sort_values('product_flux', ascending=False)

def screen_combinatorial_reaction_deletions(model: cobra.Model, candidates: list[str], k: int, product_rxn: str, max_sets: int = 200) -> pd.DataFrame:
    rows=[]
    for combo in itertools.islice(itertools.combinations(candidates, k), max_sets):
        with model:
            for rid in combo:
                if rid in model.reactions:
                    model.reactions.get_by_id(rid).knock_out()
            model.objective = product_rxn
            sol = model.optimize()
            rows.append({'ko_set': ';'.join(combo), 'status': sol.status, 'product_flux': sol.objective_value})
    return pd.DataFrame(rows).sort_values('product_flux', ascending=False)
