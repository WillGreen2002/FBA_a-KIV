from __future__ import annotations
from pathlib import Path
import pandas as pd


def parse_review_to_claims(pdf_path: str | Path) -> pd.DataFrame:
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        return pd.DataFrame([
            {
                'claim': 'Attached review file not found; all literature-derived claims marked uncertain.',
                'classification': 'not_directly_modelable',
                'confidence': 'low',
                'traceability': str(pdf_path),
            }
        ])
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(pdf_path))
        txt = '\n'.join(page.extract_text() or '' for page in reader.pages)
    except Exception as e:
        txt = f'PDF parse failed: {e}'
    claims = []
    for keyword, cls in [
        ('alss', 'proxy_modelable'),
        ('ilve', 'directly_modelable'),
        ('leua', 'directly_modelable'),
        ('panb', 'directly_modelable'),
        ('microaerobic', 'proxy_modelable'),
        ('nadph', 'proxy_modelable'),
    ]:
        if keyword in txt.lower():
            claims.append(
                {
                    'claim': f'Keyword found: {keyword}',
                    'classification': cls,
                    'confidence': 'medium',
                    'traceability': 'auto-keyword',
                }
            )
    if not claims:
        claims.append(
            {
                'claim': 'No machine-extracted specific engineering claims; manual curation required.',
                'classification': 'not_directly_modelable',
                'confidence': 'low',
                'traceability': 'auto-keyword',
            }
        )
    return pd.DataFrame(claims)


def build_alignment_markdown(claims_df: pd.DataFrame, out_md: str | Path) -> None:
    lines = [
        '# Literature Alignment',
        '',
        '| claim | classification | confidence | traceability |',
        '|---|---|---|---|',
    ]
    for _, r in claims_df.iterrows():
        lines.append(f"| {r['claim']} | {r['classification']} | {r['confidence']} | {r['traceability']} |")
    Path(out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(out_md).write_text('\n'.join(lines), encoding='utf-8')
