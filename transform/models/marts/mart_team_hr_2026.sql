-- transform/models/marts/mart_team_hr_2026.sql
-- Enriches team HR data with ranking and efficiency metrics
-- Source: wbc_2026_team_hr.csv

WITH raw AS (
    SELECT
        team,
        pool,
        hr,
        w,
        l,
        stage,
        ingested_at
    FROM {{ source('wbc_raw', 'wbc_2026_team_hr') }}
),

enriched AS (
    SELECT
        team,
        pool,
        hr,
        w,
        l,
        stage,
        (w + l) AS games_played,
        ROUND(CAST(hr AS FLOAT) / NULLIF((w + l), 0), 2) AS hr_per_game,
        RANK() OVER (ORDER BY hr DESC) AS hr_rank,
        CASE
            WHEN stage IN ('Semifinals', 'Finals') THEN 'Advanced'
            WHEN stage = 'Quarterfinals'            THEN 'Quarterfinals'
            ELSE 'Eliminated'
        END AS advancement_group,
        ingested_at
    FROM raw
)

SELECT * FROM enriched
ORDER BY hr_rank
