from __future__ import annotations
import pandas as pd

def simple_grid(top_design_df: pd.DataFrame, oxygen_bounds: list[float], growth_fracs: list[float]) -> pd.DataFrame:
    rows=[]
    for _, row in top_design_df.iterrows():
        for o2 in oxygen_bounds:
            for g in growth_fracs:
                rows.append({'design': row.get('ko_set', row.get('ko','WT')), 'oxygen_lb': o2, 'min_growth_frac': g})
    return pd.DataFrame(rows)
