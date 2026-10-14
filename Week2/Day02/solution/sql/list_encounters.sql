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
WHERE (%s::text IS NULL OR risk_level = %s::text)
ORDER BY encounter_id
LIMIT %s OFFSET %s;

