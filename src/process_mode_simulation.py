from __future__ import annotations
import cobra
from .medium_builder import set_oxygen_bound

def run_constant_mode(model: cobra.Model, oxygen_lb: float, min_growth: float, product_rxn: str) -> dict:
    with model:
        set_oxygen_bound(model, oxygen_lb)
        biomass = next(iter(model.objective.keys())).id
        model.reactions.get_by_id(biomass).lower_bound = min_growth
        model.objective = product_rxn
        sol = model.optimize()
        return {'status': sol.status, 'product_flux': sol.objective_value, 'growth': sol.fluxes.get(biomass, 0.0)}

def run_two_stage(model: cobra.Model, stage1_o2: float, stage2_o2: float, product_rxn: str) -> dict:
    biomass = next(iter(model.objective.keys())).id
    with model:
        set_oxygen_bound(model, stage1_o2)
        sol1 = model.optimize()
        mu = max(sol1.objective_value, 0.0)
    with model:
        set_oxygen_bound(model, stage2_o2)
        model.reactions.get_by_id(biomass).lower_bound = 0.05 * mu
        model.objective = product_rxn
        sol2 = model.optimize()
        return {'stage1_growth': mu, 'stage2_status': sol2.status, 'stage2_product_flux': sol2.objective_value, 'stage2_growth': sol2.fluxes.get(biomass, 0.0)}
