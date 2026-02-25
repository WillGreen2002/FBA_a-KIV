from __future__ import annotations
import pandas as pd
import cobra

def optimize_growth(model: cobra.Model):
    return model.optimize()

def flux_table(solution, rxn_ids: list[str]) -> pd.DataFrame:
    rows=[]
    for r in rxn_ids:
        if r in solution.fluxes.index:
            rows.append({'rxn_id': r, 'flux': solution.fluxes[r]})
    return pd.DataFrame(rows)

def scan_bound(model: cobra.Model, rxn_id: str, values: list[float], objective='biomass') -> pd.DataFrame:
    rows=[]
    target = next(iter(model.objective.keys()))
    for v in values:
        with model:
            if rxn_id in model.reactions:
                model.reactions.get_by_id(rxn_id).lower_bound = v
            sol = model.optimize()
            rows.append({'rxn_id': rxn_id, 'lb': v, 'growth': sol.objective_value, 'status': sol.status, 'objective_rxn': target.id})
    return pd.DataFrame(rows)
