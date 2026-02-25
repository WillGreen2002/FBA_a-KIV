from __future__ import annotations
import cobra
import pandas as pd

def list_prod_cons_reactions(model: cobra.Model, met_id: str) -> pd.DataFrame:
    met = model.metabolites.get_by_id(met_id)
    rows=[]
    for r in met.reactions:
        coeff = r.metabolites[met]
        rows.append({'rxn_id': r.id, 'name': r.name, 'stoich_coeff': coeff, 'equation': r.reaction, 'gene_rule': r.gene_reaction_rule})
    return pd.DataFrame(rows)

def ensure_export_or_demand(model: cobra.Model, met_id: str, ex_id='EX_3mob_e', dm_id='DM_3mob_c') -> list[str]:
    notes=[]
    met = model.metabolites.get_by_id(met_id)
    if ex_id not in model.reactions:
        if met.compartment == 'e':
            ex = cobra.Reaction(ex_id)
            ex.lower_bound = 0.0
            ex.upper_bound = 1000.0
            ex.add_metabolites({met: -1.0})
            model.add_reactions([ex])
            notes.append(f'Added exchange proxy {ex_id} for {met_id}.')
    if dm_id not in model.reactions:
        dm = cobra.Reaction(dm_id)
        dm.lower_bound = 0.0
        dm.upper_bound = 1000.0
        dm.add_metabolites({met: -1.0})
        model.add_reactions([dm])
        notes.append(f'Added demand proxy {dm_id} for {met_id}.')
    return notes
