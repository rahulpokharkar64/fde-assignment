SELECT
    COUNT(*) AS total_patients,
    COUNT(*) FILTER (WHERE readmitted = '<30') AS readmitted_under_30_days,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE readmitted = '<30') / NULLIF(COUNT(*), 0),
        2
    ) AS readmission_rate
FROM patient_encounters;

