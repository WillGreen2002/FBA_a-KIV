from __future__ import annotations
from typing import Dict
import cobra

def apply_medium(model: cobra.Model, medium_cfg: Dict[str, float]) -> None:
    for rxn_id, lb in medium_cfg.items():
        if rxn_id in model.reactions:
            rxn = model.reactions.get_by_id(rxn_id)
            rxn.lower_bound = lb

def set_lactate_scenario(model: cobra.Model, scenario_bounds: Dict[str, float]) -> None:
    for rxn_id, lb in scenario_bounds.items():
        if rxn_id in model.reactions:
            model.reactions.get_by_id(rxn_id).lower_bound = lb

def set_oxygen_bound(model: cobra.Model, oxygen_lb: float) -> None:
    if 'EX_o2_e' in model.reactions:
        model.reactions.get_by_id('EX_o2_e').lower_bound = oxygen_lb
