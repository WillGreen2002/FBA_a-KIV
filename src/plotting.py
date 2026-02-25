from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

def line_plot(df: pd.DataFrame, x: str, y: str, hue: str | None, out_png: str, title: str) -> None:
    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6,4))
    if hue and hue in df.columns:
        for k, sub in df.groupby(hue):
            plt.plot(sub[x], sub[y], marker='o', label=str(k))
        plt.legend()
    else:
        plt.plot(df[x], df[y], marker='o')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_png, dpi=180)
    plt.close()

def bar_plot(df: pd.DataFrame, x: str, y: str, out_png: str, title: str) -> None:
    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7,4))
    plt.bar(df[x], df[y])
    plt.xticks(rotation=45, ha='right')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_png, dpi=180)
    plt.close()
