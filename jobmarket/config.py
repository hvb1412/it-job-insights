from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_REFERENCE = ROOT / "data" / "raw" / "reference_2026"
RAW_LIVE = ROOT / "data" / "raw" / "live"
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "reports" / "figures"
TABLES = ROOT / "reports" / "tables"
ARTIFACTS = ROOT / "reports" / "artifacts"

for path in (RAW_LIVE, INTERIM, PROCESSED, FIGURES, TABLES, ARTIFACTS):
    path.mkdir(parents=True, exist_ok=True)
