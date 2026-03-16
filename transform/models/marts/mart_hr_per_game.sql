-- transform/models/marts/mart_hr_per_game.sql
-- Transforms raw historical HR data into a mart with YoY growth
-- Source: wbc_historical_hr.csv (ingested by ingestion/ingest_wbc.py)

WITH raw AS (
    SELECT
        edition,
        total_hr,
        games,
        hr_per_game,
        ingested_at
    FROM {{ source('wbc_raw', 'wbc_historical_hr') }}
),

with_growth AS (
    SELECT
        edition,
        total_hr,
        games,
        hr_per_game,
        LAG(hr_per_game) OVER (ORDER BY edition) AS prev_hr_per_game,
        ROUND(
            (hr_per_game - LAG(hr_per_game) OVER (ORDER BY edition))
            / NULLIF(LAG(hr_per_game) OVER (ORDER BY edition), 0) * 100,
        2) AS pct_change_vs_prev,
        ingested_at
    FROM raw
)

SELECT * FROM with_growth
