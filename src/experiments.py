from __future__ import annotations
from pathlib import Path
import traceback
import pandas as pd
from .utils import load_yaml, dump_json, env_snapshot, utc_now, sha256_file
from .model_loader import detect_solvers, load_bigg_model, model_qc_summary, save_exchange_inventory
from .medium_builder import apply_medium, set_lactate_scenario
from .id_mapper import find_metabolites_by_synonyms, reaction_candidates
from .pathway_validation import list_prod_cons_reactions, ensure_export_or_demand
from .plotting import line_plot, bar_plot
from .literature_parser import parse_review_to_claims, build_alignment_markdown
from .report_builder import build_final_report


def _write_step_summary(step_dir: Path, payload: dict):
    step_dir.mkdir(parents=True, exist_ok=True)
    dump_json(payload, step_dir / 'summary.json')


def run_00(ctx: dict):
    step = Path('experiments/00_env_and_model_qc')
    model = load_bigg_model(ctx['model_id'])
    solvers = detect_solvers()
    qc = model_qc_summary(model)
    save_exchange_inventory(model, 'results/tables/exchange_inventory.csv')
    manifest = {
        'timestamp': utc_now(),
        'env': env_snapshot(),
        'solvers': solvers,
        'model_qc': qc,
        'config_hashes': {p: sha256_file(p) for p in ctx['config_files'] if Path(p).exists()},
    }
    dump_json(manifest, 'results/manifests/run_manifest.json')
    _write_step_summary(step, {'status': 'ok', 'model': qc['model_id']})


def run_01(ctx: dict):
    step = Path('experiments/01_media_and_lactate_growth_validation')
    model = load_bigg_model(ctx['model_id'])
    med = load_yaml('configs/media_m9_lactate.yaml')['medium']
    scenarios = load_yaml('configs/scenarios_lactate_isomers.yaml')['lactate_scenarios']
    apply_medium(model, med)
    rows = []
    for scen, b in scenarios.items():
        with model:
            set_lactate_scenario(model, b)
            sol = model.optimize()
            rows.append({'scenario': scen, 'growth_rate_per_h': sol.objective_value, 'status': sol.status})
    df = pd.DataFrame(rows)
    df.to_csv('results/tables/exp01_growth_by_scenario.csv', index=False)
    line_plot(
        df.assign(point=range(len(df))),
        x='point',
        y='growth_rate_per_h',
        hue='scenario',
        out_png='results/figures/exp01_growth_scenarios.png',
        title='Growth across lactate scenarios',
    )
    _write_step_summary(step, {'status': 'ok', 'rows': len(df)})


def run_02(ctx: dict):
    step = Path('experiments/02_alphaKIV_id_mapping_and_pathway_validation')
    model = load_bigg_model(ctx['model_id'])
    target_cfg = load_yaml('configs/targets_alphaKIV.yaml')
    mets = find_metabolites_by_synonyms(model, target_cfg['target_synonyms'])
    mets.to_csv('results/tables/metabolite_id_map_alphaKIV.csv', index=False)
    cands = reaction_candidates(model, ['lac__L', 'lac__D', 'lactate', 'pyruvate', '3mob', 'ilv', 'leu', 'pan'])
    cands.to_csv('results/tables/reaction_id_candidates_lactate_pyruvate_alphaKIV.csv', index=False)
    notes = []
    if not mets.empty:
        met_id = mets.iloc[0]['met_id']
        pc = list_prod_cons_reactions(model, met_id)
        pc.to_csv('results/tables/exp02_alphaKIV_prod_cons.csv', index=False)
        notes.extend(ensure_export_or_demand(model, met_id))
        if not pc.empty:
            top = pc.assign(abs_coeff=pc['stoich_coeff'].abs()).sort_values('abs_coeff', ascending=False).head(15)
            bar_plot(top, 'rxn_id', 'stoich_coeff', 'results/figures/exp02_alphaKIV_prod_cons.png', 'α-KIV producing/consuming reaction coefficients')
    _write_step_summary(step, {'status': 'ok', 'notes': notes, 'met_hits': len(mets)})


def run_06_lit(ctx: dict):
    claims = parse_review_to_claims('data/raw/literature/attached_review.pdf')
    claims.to_csv('data/processed/literature_extracts/literature_claims.csv', index=False)
    build_alignment_markdown(claims, 'results/reports/literature_alignment.md')


def run_stub(step_name: str):
    p = Path(f'experiments/{step_name}')
    _write_step_summary(
        p,
        {
            'status': 'stubbed',
            'note': 'Workflow scaffold created; fill with full run for compute-intensive analysis.',
        },
    )


def run_12_report(ctx: dict, status: dict):
    sections = {
        'Executive summary': 'Scaffold run completed with automated QC, lactate growth setup, α-KIV ID mapping, and literature-alignment placeholders. Full optimization-intensive experiments are scaffolded with resumable stubs.',
        'Methods': 'COBRApy with BiGG model loading, explicit M9+lactate media constraints, scenario configs, and GLPK-first strategy with fallback enumeration.',
        'Results': f"Current status by experiment: {status}",
        'Discussion': 'Redox coupling, KARI cofactor assumptions, and oxygen-stage transitions are represented as stoichiometric proxies only; kinetic/regulatory behavior remains out of scope.',
        'Recommendations': 'Populate attached_review.pdf, run full experiments 03-11 incrementally, and prioritize sink audit plus process-mode comparison before large combinatorial searches.',
    }
    build_final_report('results/reports/final_report.md', sections)


def run_all(ctx: dict, only: str | None = None):
    steps = [
        ('00_env_and_model_qc', run_00),
        ('01_media_and_lactate_growth_validation', run_01),
        ('02_alphaKIV_id_mapping_and_pathway_validation', run_02),
    ]
    stubs = [
        '03_stoichiometry_and_theoretical_yield',
        '04_native_sink_audit',
        '05_process_mode_comparisons',
        '06_literature_guided_overexpression_proxies',
        '07_canonical_and_literature_KOs',
        '08_enumerative_deletion_searches',
        '09_optknock_or_fallback_design_search',
        '10_best_design_robustness',
        '11_incremental_intervention_ladder',
    ]
    status = {}
    for n, fn in steps:
        if only and only != n:
            continue
        try:
            fn(ctx)
            status[n] = 'ok'
        except Exception as e:
            status[n] = f'failed: {e}'
            Path(f'results/logs/{n}.log').write_text(traceback.format_exc(), encoding='utf-8')
    run_06_lit(ctx)
    for s in stubs:
        if only and only != s:
            continue
        run_stub(s)
        status[s] = status.get(s, 'stubbed')

    if only is None or only == '12_report_generation':
        run_12_report(ctx, status)
        status['12_report_generation'] = 'ok'

    dump_json(status, 'results/manifests/pipeline_status.json')
    return status
