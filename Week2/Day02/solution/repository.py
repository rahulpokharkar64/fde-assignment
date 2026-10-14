from pathlib import Path
from typing import Any

from psycopg import Connection


SQL_DIR = Path(__file__).resolve().parent / "sql"


def load_sql(name: str) -> str:
    return (SQL_DIR / name).read_text(encoding="utf-8")


class EncounterRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def list_encounters(
        self,
        limit: int,
        offset: int,
        risk_level: str | None = None,
    ) -> list[dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                load_sql("list_encounters.sql"),
                (risk_level, risk_level, limit, offset),
            )
            return list(cur.fetchall())

    def get_encounter_by_id(self, encounter_id: int) -> dict[str, Any] | None:
        with self.conn.cursor() as cur:
            cur.execute(load_sql("get_encounter_by_id.sql"), (encounter_id,))
            return cur.fetchone()

    def list_care_queue(
        self,
        minimum_risk_score: int,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                load_sql("list_care_queue.sql"),
                (minimum_risk_score, limit, offset),
            )
            return list(cur.fetchall())

    def list_high_risk_queue(self, limit: int, offset: int) -> list[dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(load_sql("list_high_risk_queue.sql"), (limit, offset))
            return list(cur.fetchall())

    def get_intervention_by_encounter_id(
        self,
        encounter_id: int,
    ) -> dict[str, Any] | None:
        with self.conn.cursor() as cur:
            cur.execute(load_sql("get_intervention_by_encounter_id.sql"), (encounter_id,))
            return cur.fetchone()

    def update_intervention(
        self,
        encounter_id: int,
        status: str | None,
        assigned_to: str | None,
        notes: str | None,
    ) -> dict[str, Any] | None:
        with self.conn.cursor() as cur:
            cur.execute(
                load_sql("update_intervention.sql"),
                (status, assigned_to, notes, encounter_id),
            )
            return cur.fetchone()

    def get_operations_summary(self) -> dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute(load_sql("get_operations_summary.sql"))
            return cur.fetchone()

    def get_readmission_analysis_overall(self) -> dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute(load_sql("get_readmission_analysis_overall.sql"))
            return cur.fetchone()

    def get_readmission_analysis_by_risk(self) -> list[dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(load_sql("get_readmission_analysis_by_risk.sql"))
            return list(cur.fetchall())

    def get_management_dashboard(self) -> dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute(load_sql("get_management_dashboard.sql"))
            return cur.fetchone()

    def upsert_patient_encounter(self, encounter: dict[str, Any]) -> None:
        values = (
            encounter["encounter_id"],
            encounter["patient_nbr"],
            encounter.get("age"),
            encounter["time_in_hospital"],
            encounter["number_inpatient"],
            encounter["number_emergency"],
            encounter["number_outpatient"],
            encounter["num_medications"],
            encounter["num_lab_procedures"],
            encounter.get("discharge_disposition_id"),
            encounter.get("admission_type_id"),
            encounter.get("readmitted"),
            encounter["risk_score"],
            encounter["risk_level"],
        )
        with self.conn.cursor() as cur:
            cur.execute(load_sql("upsert_patient_encounter.sql"), values)

    def create_queue_intervention(self, encounter_id: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute(load_sql("create_queue_intervention.sql"), (encounter_id,))

    def delete_non_queue_intervention(self, encounter_id: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute(load_sql("delete_non_queue_intervention.sql"), (encounter_id,))

