from typing import Any

from models import InterventionUpdateRequest, RiskLevel
from repository import EncounterRepository


class NotFoundError(Exception):
    pass


class InvalidWorkflowError(Exception):
    pass


def calculate_risk_score(encounter: dict[str, Any]) -> int:
    score = 0
    if int(encounter.get("number_inpatient") or 0) >= 3:
        score += 3
    if int(encounter.get("number_emergency") or 0) >= 2:
        score += 2
    if int(encounter.get("number_outpatient") or 0) >= 3:
        score += 1
    if int(encounter.get("time_in_hospital") or 0) >= 7:
        score += 1
    if int(encounter.get("num_medications") or 0) >= 20:
        score += 1
    return score


def map_risk_level(score: int) -> str:
    if score >= 5:
        return RiskLevel.HIGH.value
    if score >= 3:
        return RiskLevel.MEDIUM.value
    return RiskLevel.LOW.value


class EncounterService:
    def __init__(self, repository: EncounterRepository):
        self.repository = repository

    def list_encounters(
        self,
        limit: int,
        offset: int,
        risk_level: RiskLevel | None = None,
    ) -> list[dict[str, Any]]:
        return self.repository.list_encounters(
            limit=limit,
            offset=offset,
            risk_level=risk_level.value if risk_level else None,
        )

    def get_encounter(self, encounter_id: int) -> dict[str, Any]:
        encounter = self.repository.get_encounter_by_id(encounter_id)
        if encounter is None:
            raise NotFoundError("Encounter not found")
        return encounter

    def list_care_queue(
        self,
        minimum_risk_score: int,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]]:
        return self.repository.list_care_queue(
            minimum_risk_score=minimum_risk_score,
            limit=limit,
            offset=offset,
        )

    def list_high_risk_queue(self, limit: int, offset: int) -> list[dict[str, Any]]:
        return self.repository.list_high_risk_queue(limit=limit, offset=offset)

    def update_intervention(
        self,
        encounter_id: int,
        payload: InterventionUpdateRequest,
    ) -> dict[str, Any]:
        self.get_encounter(encounter_id)
        intervention = self.repository.get_intervention_by_encounter_id(encounter_id)
        if intervention is None:
            raise NotFoundError("Intervention not found for encounter")

        if payload.status is None and payload.assigned_to is None and payload.notes is None:
            raise InvalidWorkflowError("At least one field must be provided")

        updated = self.repository.update_intervention(
            encounter_id=encounter_id,
            status=payload.status.value if payload.status else None,
            assigned_to=payload.assigned_to,
            notes=payload.notes,
        )
        if updated is None:
            raise NotFoundError("Intervention not found for encounter")
        return updated

    def get_operations_summary(self) -> dict[str, Any]:
        return self.repository.get_operations_summary()

    def get_readmission_analysis(self) -> dict[str, Any]:
        return {
            "overall": self.repository.get_readmission_analysis_overall(),
            "by_risk_level": self.repository.get_readmission_analysis_by_risk(),
        }

    def get_management_dashboard(self) -> dict[str, Any]:
        return self.repository.get_management_dashboard()

