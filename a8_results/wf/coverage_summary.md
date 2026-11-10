# WF — coverage summary (production code only)

Source: a8_results/wf/coverage.xml (pytest-cov, `--cov=modules.rspc --cov-branch`), run 2026-11-10 21:27 UTC.
Excluded: `modules/rspc/tests/*`, `modules/rspc/migrations/*`.
Test outcome (junit.xml / pytest.log): 34 collected — 6 passed, 0 failed, 0 errors, 28 skipped (NOT_AUTOMATED).

| File | Lines | Lines hit | Line % | Branches | Branches hit | Branch % |
|---|---:|---:|---:|---:|---:|---:|
| modules/rspc/__init__.py | 0 | 0 | — | 0 | 0 | — |
| modules/rspc/apps.py | 4 | 4 | 100.00 | 0 | 0 | — |
| modules/rspc/models.py | 31 | 29 | 93.55 | 0 | 0 | — |
| modules/rspc/registry.py | 4 | 4 | 100.00 | 0 | 0 | — |
| modules/rspc/api/__init__.py | 0 | 0 | — | 0 | 0 | — |
| modules/rspc/api/serializers.py | 26 | 24 | 92.31 | 4 | 2 | 50.00 |
| modules/rspc/api/urls.py | 3 | 3 | 100.00 | 0 | 0 | — |
| modules/rspc/api/views.py | 131 | 112 | 85.50 | 36 | 20 | 55.56 |
| **Total** | **199** | **176** | **88.44** | **40** | **22** | **55.00** |

- **Line coverage: 88.44 %** (176/199)
- **Branch coverage: 55.00 %** (22/40)
- (Combined line+branch as pytest-cov computes it, production only: (176+22)/(199+40) = 82.85 %.)

Branch figures come from each `<line branch="true" condition-coverage="x% (hit/total)">` entry in coverage.xml.
Uncovered (from term-missing in pytest.log): serializers.py 65, 68 (date-order and non-positive-budget validation);
views.py 25, 32-34, 42, 44, 47-50, 67, 72, 104, 109, 141, 180-184, 204, 232-236 (invalid-input/wrong-state error paths,
mine view, queue fallbacks); models.py 37, 56 (`__str__`). WF design exercises only valid transitions, so these error paths are outside its obligations.
