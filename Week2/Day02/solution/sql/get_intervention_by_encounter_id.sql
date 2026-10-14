SELECT
    intervention_id,
    encounter_id,
    status,
    assigned_to,
    notes,
    created_at,
    updated_at
FROM care_interventions
WHERE encounter_id = %s;

