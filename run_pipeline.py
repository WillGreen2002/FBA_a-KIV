#!/usr/bin/env python3
from __future__ import annotations
import argparse
from src.experiments import run_all


def main():
    ap=argparse.ArgumentParser(description='Run α-KIV FBA pipeline with checkpointing-friendly summaries.')
    ap.add_argument('--model', default='iML1515', choices=['iML1515','iJO1366'])
    ap.add_argument('--run', default='all', help='all or specific experiment directory name')
    args=ap.parse_args()
    ctx={'model_id':args.model,'config_files':['configs/base.yaml','configs/media_m9_lactate.yaml','configs/scenarios_lactate_isomers.yaml','configs/scenarios_process_modes.yaml','configs/targets_alphaKIV.yaml','configs/solver.yaml','assumptions.yaml']}
    only=None if args.run=='all' else args.run
    status=run_all(ctx, only=only)
    print('Pipeline status:')
    for k,v in status.items():
        print(f' - {k}: {v}')

if __name__=='__main__':
    main()
