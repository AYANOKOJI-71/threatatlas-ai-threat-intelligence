from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from threatatlas.contracts import CaseInput

PROJECT_ROOT = Path(__file__).resolve().parents[4]
FIXTURE_DIR = PROJECT_ROOT / "fixtures" / "cases"


@lru_cache(maxsize=1)
def load_cases() -> dict[str, CaseInput]:
    cases = {}
    for path in sorted(FIXTURE_DIR.glob("*.json")):
        case = CaseInput.model_validate(json.loads(path.read_text(encoding="utf-8")))
        cases[case.case_id] = case
    return cases


def get_case(case_id: str) -> CaseInput | None:
    return load_cases().get(case_id)
