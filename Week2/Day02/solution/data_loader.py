import argparse
import csv
from pathlib import Path
from typing import Any

from database import get_connection
from repository import EncounterRepository
from services import calculate_risk_score, map_risk_level


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CSV_PATH = BASE_DIR / "data" / "sample_diabetes_readmission.csv"

REQUIRED_FIELDS = [
    "encounter_id",
    "patient_nbr",
    "age",
    "time_in_hospital",
    "number_inpatient",
    "number_emergency",
    "number_outpatient",
    "num_medications",
    "num_lab_procedures",
    "discharge_disposition_id",
    "admission_type_id",
    "readmitted",
]

INTEGER_FIELDS = [
    "encounter_id",
    "patient_nbr",
    "time_in_hospital",
    "number_inpatient",
    "number_emergency",
    "number_outpatient",
    "num_medications",
    "num_lab_procedures",
    "discharge_disposition_id",
    "admission_type_id",
]


def parse_int(value: str | None) -> int:
    if value is None or value.strip() in {"", "?"}:
        return 0
    return int(value)


def clean_row(row: dict[str, str]) -> dict[str, Any]:
    cleaned: dict[str, Any] = {}
    for field in REQUIRED_FIELDS:
        cleaned[field] = row.get(field)

    for field in INTEGER_FIELDS:
        cleaned[field] = parse_int(cleaned[field])

    cleaned["age"] = cleaned["age"] or None
    cleaned["readmitted"] = cleaned["readmitted"] or None

    risk_score = calculate_risk_score(cleaned)
    cleaned["risk_score"] = risk_score
    cleaned["risk_level"] = map_risk_level(risk_score)
    return cleaned


def load_csv(csv_path: Path) -> int:
    loaded = 0
    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing_fields = sorted(set(REQUIRED_FIELDS) - set(reader.fieldnames or []))
        if missing_fields:
            raise ValueError(f"Missing required CSV fields: {', '.join(missing_fields)}")

        with get_connection() as conn:
            repository = EncounterRepository(conn)
            for row in reader:
                encounter = clean_row(row)
                repository.upsert_patient_encounter(encounter)
                if encounter["risk_level"] in {"MEDIUM", "HIGH"}:
                    repository.create_queue_intervention(encounter["encounter_id"])
                else:
                    repository.delete_non_queue_intervention(encounter["encounter_id"])
                loaded += 1
            conn.commit()
    return loaded


def main() -> None:
    parser = argparse.ArgumentParser(description="Load diabetes encounters into PostgreSQL.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV_PATH,
        help="Path to diabetes readmission CSV.",
    )
    args = parser.parse_args()

    count = load_csv(args.csv)
    print(f"Loaded {count} encounters from {args.csv}")


if __name__ == "__main__":
    main()

