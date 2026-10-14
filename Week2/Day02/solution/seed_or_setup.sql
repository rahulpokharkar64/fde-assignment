INSERT INTO patient_encounters (
    encounter_id,
    patient_nbr,
    age,
    time_in_hospital,
    number_inpatient,
    number_emergency,
    number_outpatient,
    num_medications,
    num_lab_procedures,
    discharge_disposition_id,
    admission_type_id,
    readmitted,
    risk_score,
    risk_level
) VALUES
    (10001, 501, '[70-80)', 8, 4, 2, 3, 22, 55, 1, 1, '<30', 8, 'HIGH'),
    (10002, 502, '[60-70)', 5, 3, 0, 1, 18, 44, 1, 3, '>30', 3, 'MEDIUM'),
    (10003, 503, '[50-60)', 3, 0, 1, 0, 10, 32, 1, 2, 'NO', 0, 'LOW'),
    (10004, 504, '[80-90)', 9, 2, 2, 4, 21, 61, 3, 1, '<30', 5, 'HIGH'),
    (10005, 505, '[40-50)', 2, 1, 0, 0, 8, 23, 1, 1, 'NO', 0, 'LOW'),
    (10006, 506, '[70-80)', 7, 3, 1, 3, 16, 48, 6, 2, '>30', 5, 'HIGH'),
    (10007, 507, '[30-40)', 4, 0, 2, 3, 12, 30, 1, 3, 'NO', 3, 'MEDIUM'),
    (10008, 508, '[60-70)', 6, 2, 1, 4, 25, 57, 1, 1, '<30', 2, 'LOW'),
    (10009, 509, '[50-60)', 10, 3, 3, 2, 20, 69, 1, 2, '<30', 7, 'HIGH'),
    (10010, 510, '[80-90)', 7, 1, 0, 5, 20, 52, 3, 1, '>30', 3, 'MEDIUM')
ON CONFLICT (encounter_id) DO UPDATE SET
    patient_nbr = EXCLUDED.patient_nbr,
    age = EXCLUDED.age,
    time_in_hospital = EXCLUDED.time_in_hospital,
    number_inpatient = EXCLUDED.number_inpatient,
    number_emergency = EXCLUDED.number_emergency,
    number_outpatient = EXCLUDED.number_outpatient,
    num_medications = EXCLUDED.num_medications,
    num_lab_procedures = EXCLUDED.num_lab_procedures,
    discharge_disposition_id = EXCLUDED.discharge_disposition_id,
    admission_type_id = EXCLUDED.admission_type_id,
    readmitted = EXCLUDED.readmitted,
    risk_score = EXCLUDED.risk_score,
    risk_level = EXCLUDED.risk_level;

INSERT INTO care_interventions (
    encounter_id,
    status,
    assigned_to,
    notes
)
SELECT
    encounter_id,
    'PENDING_REVIEW',
    NULL,
    'Seeded queue item'
FROM patient_encounters
WHERE risk_level IN ('MEDIUM', 'HIGH')
ON CONFLICT (encounter_id) DO NOTHING;

