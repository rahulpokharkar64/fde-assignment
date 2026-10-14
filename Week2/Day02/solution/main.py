from collections.abc import Generator

from fastapi import Depends, FastAPI, HTTPException, Query

from database import get_connection
from models import (
    CareQueueItem,
    EncounterResponse,
    InterventionResponse,
    InterventionUpdateRequest,
    ManagementDashboardResponse,
    OperationsSummaryResponse,
    ReadmissionAnalysisResponse,
    RiskLevel,
)
from repository import EncounterRepository
from services import EncounterService, InvalidWorkflowError, NotFoundError


app = FastAPI(
    title="Diabetes Readmission Intervention Queue",
    version="1.0.0",
    description="Learning MVP for prioritizing diabetes readmission intervention workflows.",
)


def get_service() -> Generator[EncounterService, None, None]:
    with get_connection() as conn:
        yield EncounterService(EncounterRepository(conn))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/encounters", response_model=list[EncounterResponse])
def list_encounters(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    risk_level: RiskLevel | None = None,
    service: EncounterService = Depends(get_service),
) -> list[dict]:
    return service.list_encounters(limit=limit, offset=offset, risk_level=risk_level)


@app.get("/encounters/{encounter_id}", response_model=EncounterResponse)
def get_encounter(
    encounter_id: int,
    service: EncounterService = Depends(get_service),
) -> dict:
    try:
        return service.get_encounter(encounter_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/care-queue", response_model=list[CareQueueItem])
def list_care_queue(
    minimum_risk_score: int = Query(default=0, ge=0, le=8),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    service: EncounterService = Depends(get_service),
) -> list[dict]:
    return service.list_care_queue(
        minimum_risk_score=minimum_risk_score,
        limit=limit,
        offset=offset,
    )


@app.get("/care-queue/high", response_model=list[CareQueueItem])
def list_high_risk_queue(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    service: EncounterService = Depends(get_service),
) -> list[dict]:
    return service.list_high_risk_queue(limit=limit, offset=offset)


@app.patch("/interventions/{encounter_id}", response_model=InterventionResponse)
def update_intervention(
    encounter_id: int,
    payload: InterventionUpdateRequest,
    service: EncounterService = Depends(get_service),
) -> dict:
    try:
        return service.update_intervention(encounter_id, payload)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except InvalidWorkflowError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/operations/summary", response_model=OperationsSummaryResponse)
def get_operations_summary(
    service: EncounterService = Depends(get_service),
) -> dict:
    return service.get_operations_summary()


@app.get("/operations/readmission-analysis", response_model=ReadmissionAnalysisResponse)
def get_readmission_analysis(
    service: EncounterService = Depends(get_service),
) -> dict:
    return service.get_readmission_analysis()


@app.get("/management/dashboard", response_model=ManagementDashboardResponse)
def get_management_dashboard(
    service: EncounterService = Depends(get_service),
) -> dict:
    return service.get_management_dashboard()

