SELECT
    COUNT(*) AS total_encounters,
    COUNT(*) FILTER (WHERE risk_level IN ('MEDIUM', 'HIGH')) AS care_queue_size,
    COUNT(*) FILTER (WHERE risk_level = 'HIGH') AS high_risk_count,
    COUNT(*) FILTER (WHERE risk_level = 'MEDIUM') AS medium_risk_count,
    (
        SELECT COUNT(*)
        FROM care_interventions
        WHERE status IN ('PENDING_REVIEW', 'ASSIGNED', 'CONTACTED', 'FOLLOW_UP_SCHEDULED')
    ) AS pending_interventions,
    (
        SELECT COUNT(*)
        FROM care_interventions
        WHERE status = 'CLOSED'
    ) AS closed_interventions,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE risk_level = 'HIGH' AND readmitted = '<30')
        / NULLIF(COUNT(*) FILTER (WHERE risk_level = 'HIGH'), 0),
        2
    ) AS high_risk_readmission_rate,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE readmitted = '<30') / NULLIF(COUNT(*), 0),
        2
    ) AS overall_readmission_rate
FROM patient_encounters;

