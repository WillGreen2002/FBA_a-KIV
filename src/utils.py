from __future__ import annotations
import hashlib
import json
import platform
import subprocess
from pathlib import Path
from datetime import datetime
import yaml


def load_yaml(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def dump_yaml(data: dict, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, sort_keys=False)


def dump_json(data: dict, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def utc_now() -> str:
    return datetime.utcnow().isoformat() + 'Z'


def package_versions() -> dict:
    pkgs = ['cobra', 'pandas', 'numpy', 'matplotlib', 'yaml', 'networkx']
    out = {}
    for p in pkgs:
        try:
            out[p] = __import__(p).__version__
        except Exception:
            out[p] = 'not-installed'
    return out


def env_snapshot() -> dict:
    return {
        'python': platform.python_version(),
        'platform': platform.platform(),
        'packages': package_versions(),
    }


def run_cmd(cmd: str) -> tuple[int, str]:
    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return p.returncode, (p.stdout + '\n' + p.stderr).strip()
