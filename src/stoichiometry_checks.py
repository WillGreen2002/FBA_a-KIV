from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import cobra

@dataclass
class StoichSummary:
    reaction_id: str
    equation: str

def summarize_route(model: cobra.Model, route_rxns: Iterable[str]) -> list[StoichSummary]:
    out=[]
    for rid in route_rxns:
        if rid in model.reactions:
            r=model.reactions.get_by_id(rid)
            out.append(StoichSummary(rid, r.reaction))
    return out

def compute_yield(solution_fluxes, product_flux: float, lactate_fluxes: list[float]) -> dict:
    total_lac = sum(abs(v) for v in lactate_fluxes if v < 0)
    mol_mol = product_flux / total_lac if total_lac else 0.0
    mw_lac = 90.08
    mw_kiv = 116.11
    gg = (product_flux * mw_kiv) / (total_lac * mw_lac) if total_lac else 0.0
    return {'yield_mol_per_mol_lac': mol_mol, 'yield_g_per_g_lac': gg}
