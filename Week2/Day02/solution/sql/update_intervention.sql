UPDATE care_interventions
SET
    status = COALESCE(%s, status),
    assigned_to = COALESCE(%s, assigned_to),
    notes = COALESCE(%s, notes),
    updated_at = CURRENT_TIMESTAMP
WHERE encounter_id = %s
RETURNING
    intervention_id,
    encounter_id,
    status,
    assigned_to,
    notes,
    created_at,
    updated_at;

