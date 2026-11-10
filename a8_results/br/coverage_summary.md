# BR coverage summary (production code only)

Source: `a8_results/br/coverage.xml` (pytest-cov, `--cov=modules.rspc --cov-branch`).
Excluded: `modules/rspc/tests/*`, `modules/rspc/migrations/*`.

| File | Lines covered/total | Line % | Branches covered/total | Branch % |
|---|---|---|---|---|
| modules/rspc/__init__.py | 0/0 | n/a | 0/0 | n/a |
| modules/rspc/apps.py | 4/4 | 100.00 | 0/0 | n/a |
| modules/rspc/models.py | 29/31 | 93.55 | 0/0 | n/a |
| modules/rspc/registry.py | 4/4 | 100.00 | 0/0 | n/a |
| modules/rspc/api/__init__.py | 0/0 | n/a | 0/0 | n/a |
| modules/rspc/api/serializers.py | 26/26 | 100.00 | 4/4 | 100.00 |
| modules/rspc/api/urls.py | 3/3 | 100.00 | 0/0 | n/a |
| modules/rspc/api/views.py | 111/131 | 84.73 | 22/36 | 61.11 |
| **Total** | **177/199** | **88.94** | **26/40** | **65.00** |

Test outcome (junit/pytest.log): 66 collected — 33 passed, 1 failed (BR-040), 32 skipped (NOT_AUTOMATED), 0 errors.
