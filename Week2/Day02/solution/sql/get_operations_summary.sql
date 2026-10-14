SELECT
    COUNT(*) AS total_encounters,
    COUNT(*) FILTER (WHERE risk_level = 'HIGH') AS high_risk,
    COUNT(*) FILTER (WHERE risk_level = 'MEDIUM') AS medium_risk,
    COUNT(*) FILTER (WHERE risk_level = 'LOW') AS low_risk,
    (
        SELECT COUNT(*)
        FROM care_interventions
        WHERE status IN ('PENDING_REVIEW', 'ASSIGNED', 'CONTACTED', 'FOLLOW_UP_SCHEDULED')
    ) AS pending_interventions,
    (
        SELECT COUNT(*)
        FROM care_interventions
        WHERE status = 'CLOSED'
    ) AS completed_interventions
FROM patient_encounters;

