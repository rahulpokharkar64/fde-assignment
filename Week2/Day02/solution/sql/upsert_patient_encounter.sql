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
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
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

