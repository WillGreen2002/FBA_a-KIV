from __future__ import annotations
from pathlib import Path


def build_final_report(out_path: str, sections: dict[str, str]) -> None:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('# α-KIV FBA Project Report\n\n')
        for title, text in sections.items():
            f.write(f'## {title}\n\n{text}\n\n')
