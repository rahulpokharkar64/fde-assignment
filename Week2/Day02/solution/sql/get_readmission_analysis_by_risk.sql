SELECT
    risk_level,
    COUNT(*) AS patients,
    COUNT(*) FILTER (WHERE readmitted = '<30') AS readmitted_under_30_days,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE readmitted = '<30') / NULLIF(COUNT(*), 0),
        2
    ) AS readmission_rate
FROM patient_encounters
GROUP BY risk_level
ORDER BY CASE risk_level WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 ELSE 3 END;

