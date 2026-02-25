from __future__ import annotations
from typing import Iterable
import pandas as pd
import cobra

def find_metabolites_by_synonyms(model: cobra.Model, synonyms: Iterable[str]) -> pd.DataFrame:
    syns = [s.lower() for s in synonyms]
    rows = []
    for m in model.metabolites:
        blob = f"{m.id} {m.name}".lower()
        if any(s in blob for s in syns):
            rows.append({'met_id': m.id, 'name': m.name, 'compartment': m.compartment})
    return pd.DataFrame(rows)

def reaction_candidates(model: cobra.Model, terms: Iterable[str]) -> pd.DataFrame:
    t = [x.lower() for x in terms]
    rows = []
    for r in model.reactions:
        blob = f"{r.id} {r.name} {r.reaction}".lower()
        if any(k in blob for k in t):
            rows.append({'rxn_id': r.id, 'name': r.name, 'equation': r.reaction, 'gene_rule': r.gene_reaction_rule})
    return pd.DataFrame(rows)
