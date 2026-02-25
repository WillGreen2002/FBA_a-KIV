from __future__ import annotations
import itertools
import cobra
import pandas as pd

def fseof_like_scan(model: cobra.Model, product_rxn: str, levels: list[float], candidate_rxns: list[str]) -> pd.DataFrame:
    rows=[]
    biomass = next(iter(model.objective.keys())).id
    max_growth = model.optimize().objective_value
    for lvl in levels:
        with model:
            model.reactions.get_by_id(biomass).lower_bound = max_growth * (1-lvl)
            model.objective = product_rxn
            sol = model.optimize()
            for r in candidate_rxns:
                if r in sol.fluxes.index:
                    rows.append({'forcing_level': lvl, 'rxn_id': r, 'flux': sol.fluxes[r], 'product_flux': sol.objective_value})
    return pd.DataFrame(rows)

def apply_overexpression_proxy(model: cobra.Model, rxn_ids: list[str], factor: float = 2.0) -> None:
    for rid in rxn_ids:
        if rid in model.reactions:
            rxn = model.reactions.get_by_id(rid)
            rxn.upper_bound *= factor
