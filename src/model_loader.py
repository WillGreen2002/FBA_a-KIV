from __future__ import annotations
from pathlib import Path
from typing import Any
import cobra
from cobra.io import load_model, read_sbml_model, write_sbml_model
from .utils import dump_json, utc_now

def detect_solvers() -> dict[str, bool]:
    available = {}
    for s in ['glpk', 'gurobi', 'cplex']:
        try:
            m = cobra.Model('tmp')
            m.solver = s
            available[s] = True
        except Exception:
            available[s] = False
    return available

def load_bigg_model(model_id: str, cache_dir: str | Path = 'data/raw/bigg') -> cobra.Model:
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f'{model_id}.xml'
    if cache_path.exists():
        return read_sbml_model(str(cache_path))
    model = load_model(model_id)
    write_sbml_model(model, str(cache_path))
    return model

def model_qc_summary(model: cobra.Model) -> dict[str, Any]:
    exchanges = [r.id for r in model.exchanges]
    return {
        'model_id': model.id,
        'timestamp': utc_now(),
        'metabolites': len(model.metabolites),
        'reactions': len(model.reactions),
        'genes': len(model.genes),
        'exchanges': len(exchanges),
        'objective': str(model.objective.expression),
    }

def save_exchange_inventory(model: cobra.Model, out_csv: str | Path) -> None:
    import pandas as pd
    rows = [{'reaction_id': r.id, 'name': r.name, 'lb': r.lower_bound, 'ub': r.upper_bound} for r in model.exchanges]
    pd.DataFrame(rows).to_csv(out_csv, index=False)
