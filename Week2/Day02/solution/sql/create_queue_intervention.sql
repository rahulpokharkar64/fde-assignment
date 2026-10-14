INSERT INTO care_interventions (
    encounter_id,
    status,
    assigned_to,
    notes
) VALUES (
    %s,
    'PENDING_REVIEW',
    NULL,
    'Created by data loader'
)
ON CONFLICT (encounter_id) DO NOTHING;

