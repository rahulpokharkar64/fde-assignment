CREATE TABLE IF NOT EXISTS patient_encounters (
    encounter_id BIGINT PRIMARY KEY,
    patient_nbr BIGINT NOT NULL,
    age TEXT,
    time_in_hospital INTEGER NOT NULL DEFAULT 0,
    number_inpatient INTEGER NOT NULL DEFAULT 0,
    number_emergency INTEGER NOT NULL DEFAULT 0,
    number_outpatient INTEGER NOT NULL DEFAULT 0,
    num_medications INTEGER NOT NULL DEFAULT 0,
    num_lab_procedures INTEGER NOT NULL DEFAULT 0,
    discharge_disposition_id INTEGER,
    admission_type_id INTEGER,
    readmitted TEXT,
    risk_score INTEGER NOT NULL,
    risk_level TEXT NOT NULL CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH'))
);

CREATE TABLE IF NOT EXISTS care_interventions (
    intervention_id BIGSERIAL PRIMARY KEY,
    encounter_id BIGINT NOT NULL UNIQUE REFERENCES patient_encounters(encounter_id) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK (
        status IN (
            'PENDING_REVIEW',
            'ASSIGNED',
            'CONTACTED',
            'FOLLOW_UP_SCHEDULED',
            'CLOSED'
        )
    ),
    assigned_to TEXT,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_patient_encounters_risk_level
ON patient_encounters (risk_level);

CREATE INDEX IF NOT EXISTS idx_patient_encounters_risk_score
ON patient_encounters (risk_score DESC);

CREATE INDEX IF NOT EXISTS idx_patient_encounters_readmitted
ON patient_encounters (readmitted);

CREATE INDEX IF NOT EXISTS idx_care_interventions_status
ON care_interventions (status);

CREATE INDEX IF NOT EXISTS idx_care_interventions_encounter_id
ON care_interventions (encounter_id);

