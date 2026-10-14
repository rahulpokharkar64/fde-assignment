SELECT
    pe.encounter_id,
    pe.patient_nbr,
    pe.age,
    pe.time_in_hospital,
    pe.number_inpatient,
    pe.number_emergency,
    pe.number_outpatient,
    pe.num_medications,
    pe.num_lab_procedures,
    pe.discharge_disposition_id,
    pe.admission_type_id,
    pe.readmitted,
    pe.risk_score,
    pe.risk_level,
    ci.intervention_id,
    ci.status,
    ci.assigned_to,
    ci.notes,
    ci.created_at,
    ci.updated_at
FROM patient_encounters pe
JOIN care_interventions ci ON ci.encounter_id = pe.encounter_id
WHERE pe.risk_level = 'HIGH'
ORDER BY pe.risk_score DESC, pe.encounter_id
LIMIT %s OFFSET %s;

