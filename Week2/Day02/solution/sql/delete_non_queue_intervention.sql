DELETE FROM care_interventions
WHERE encounter_id = %s
  AND EXISTS (
      SELECT 1
      FROM patient_encounters
      WHERE patient_encounters.encounter_id = care_interventions.encounter_id
        AND patient_encounters.risk_level = 'LOW'
  );

