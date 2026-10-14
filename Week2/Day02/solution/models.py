from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class InterventionStatus(StrEnum):
    PENDING_REVIEW = "PENDING_REVIEW"
    ASSIGNED = "ASSIGNED"
    CONTACTED = "CONTACTED"
    FOLLOW_UP_SCHEDULED = "FOLLOW_UP_SCHEDULED"
    CLOSED = "CLOSED"


class EncounterResponse(BaseModel):
    encounter_id: int
    patient_nbr: int
    age: str | None = None
    time_in_hospital: int
    number_inpatient: int
    number_emergency: int
    number_outpatient: int
    num_medications: int
    num_lab_procedures: int
    discharge_disposition_id: int | None = None
    admission_type_id: int | None = None
    readmitted: str | None = None
    risk_score: int
    risk_level: RiskLevel


class CareQueueItem(EncounterResponse):
    intervention_id: int
    status: InterventionStatus
    assigned_to: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class InterventionUpdateRequest(BaseModel):
    status: InterventionStatus | None = None
    assigned_to: str | None = Field(default=None, max_length=200)
    notes: str | None = None


class InterventionResponse(BaseModel):
    intervention_id: int
    encounter_id: int
    status: InterventionStatus
    assigned_to: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class OperationsSummaryResponse(BaseModel):
    total_encounters: int
    high_risk: int
    medium_risk: int
    low_risk: int
    pending_interventions: int
    completed_interventions: int


class ReadmissionOverall(BaseModel):
    total_patients: int
    readmitted_under_30_days: int
    readmission_rate: float | None


class ReadmissionByRisk(BaseModel):
    risk_level: RiskLevel
    patients: int
    readmitted_under_30_days: int
    readmission_rate: float | None


class ReadmissionAnalysisResponse(BaseModel):
    overall: ReadmissionOverall
    by_risk_level: list[ReadmissionByRisk]


class ManagementDashboardResponse(BaseModel):
    total_encounters: int
    care_queue_size: int
    high_risk_count: int
    medium_risk_count: int
    pending_interventions: int
    closed_interventions: int
    high_risk_readmission_rate: float | None
    overall_readmission_rate: float | None

