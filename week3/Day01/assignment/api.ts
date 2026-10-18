export type RiskLevel = "LOW" | "MEDIUM" | "HIGH";

export type InterventionStatus =
    | "PENDING_REVIEW"
    | "ASSIGNED"
    | "CONTACTED"
    | "FOLLOW_UP_SCHEDULED"
    | "CLOSED";

export interface Encounter {
    encounter_id: number;
    patient_nbr: number;
    age: string | null;
    time_in_hospital: number;
    number_inpatient: number;
    number_emergency: number;
    number_outpatient: number;
    num_medications: number;
    num_lab_procedures: number;
    discharge_disposition_id: number | null;
    discharge_disposition_description: string | null;
    admission_type_id: number | null;
    admission_type_description: string | null;
    admission_source_id: number | null;
    admission_source_description: string | null;
    readmitted: string | null;
    risk_score: number;
    risk_level: RiskLevel;
}

export interface CareQueueItem extends Encounter {
    intervention_id: number;
    status: InterventionStatus;
    assigned_to: string | null;
    notes: string | null;
    created_at: string;
    updated_at: string;
}

export interface OperationsSummary {
    total_encounters: number;
    high_risk: number;
    medium_risk: number;
    low_risk: number;
    pending_interventions: number;
    completed_interventions: number;
}

export interface ReadmissionOverall {
    total_patients: number;
    readmitted_under_30_days: number;
    readmission_rate: number | null;
}

export interface ReadmissionByRisk {
    risk_level: RiskLevel;
    patients: number;
    readmitted_under_30_days: number;
    readmission_rate: number | null;
}

export interface ReadmissionAnalysis {
    overall: ReadmissionOverall;
    by_risk_level: ReadmissionByRisk[];
}

export interface ManagementDashboard {
    total_encounters: number;
    care_queue_size: number;
    high_risk_count: number;
    medium_risk_count: number;
    pending_interventions: number;
    closed_interventions: number;
    high_risk_readmission_rate: number | null;
    overall_readmission_rate: number | null;
}

type QueryOptions = Record<string, string | number | undefined>;

export interface EncounterListOptions {
    limit?: number;
    offset?: number;
    risk_level?: RiskLevel;
    [key: string]: string | number | undefined;
}

export interface CareQueueOptions {
    minimum_risk_score?: number;
    limit?: number;
    offset?: number;
    [key: string]: string | number | undefined;
}

export interface HighRiskQueueOptions {
    limit?: number;
    offset?: number;
    [key: string]: string | number | undefined;
}

const API_BASE_URL = "http://127.0.0.1:8000";

function makeUrl(path: string, options?: QueryOptions): string {
    const url = new URL(path, API_BASE_URL);

    for (const [key, value] of Object.entries(options ?? {})) {
        if (value !== undefined) {
            url.searchParams.set(key, String(value));
        }
    }

    return url.toString();
}

async function getJson<T>(path: string, options?: QueryOptions): Promise<T> {
    const response = await fetch(makeUrl(path, options));

    if (!response.ok) {
        throw new Error(
            `GET ${path} failed: ${response.status} ${response.statusText}`,
        );
    }

    return response.json() as Promise<T>;
}

export async function getManagementDashboard(): Promise<void> {
    const dashboard = await getJson<ManagementDashboard>("/management/dashboard");
    console.log("Management dashboard:", JSON.stringify(dashboard, null, 2));
    // return dashboard;
}

export async function getOperationsSummary(): Promise<void> {
    const summary = await getJson<OperationsSummary>("/operations/summary");
    console.log("Operations summary:", JSON.stringify(summary, null, 2));
    // return summary;
}

export async function getCareQueue(
    options: CareQueueOptions = {},
): Promise<void> {
    const queue = await getJson<CareQueueItem[]>("/care-queue", options);
    console.log("Care queue:", JSON.stringify(queue, null, 2));
    // return queue;
}

export async function getHighRiskQueue(
    options: HighRiskQueueOptions = {},
): Promise<void> {
    const queue = await getJson<CareQueueItem[]>("/care-queue/high", options);
    console.log("High-risk care queue:", JSON.stringify(queue, null, 2));
    // return queue;
}

export async function getEncounters(
    options: EncounterListOptions = {},
): Promise<void> {
    const encounters = await getJson<Encounter[]>("/encounters", options);
    console.log("Encounters:", JSON.stringify(encounters, null, 2));
    // return encounters;
}

export async function getEncounterById(encounterId: number): Promise<void> {
    const encounter = await getJson<Encounter>(`/encounters/${encounterId}`);
    console.log(`Encounter ${encounterId}:`, JSON.stringify(encounter, null, 2));
    // return encounter;
}

export async function getReadmissionAnalysis(): Promise<void> {
    const analysis = await getJson<ReadmissionAnalysis>(
        "/operations/readmission-analysis",
    );
    console.log("Readmission analysis:", JSON.stringify(analysis, null, 2));
    // return analysis;
}

async function runApiExamples(): Promise<void> {
    await getManagementDashboard();
    await getOperationsSummary();
    await getCareQueue({ limit: 10, offset: 0 });
    await getHighRiskQueue({ limit: 10, offset: 0 });
    await getEncounters({ limit: 10, offset: 0 });
    await getEncounterById(10001);
    await getReadmissionAnalysis();
}

void runApiExamples().catch((error: unknown) => {
    console.error("API example calls failed:", error);
});
