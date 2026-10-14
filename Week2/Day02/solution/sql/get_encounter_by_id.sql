SELECT
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
FROM patient_encounters
WHERE encounter_id = %s;

