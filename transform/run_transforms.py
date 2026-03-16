"""
transform/run_transforms.py
----------------------------
Simulates dbt mart logic in pure Python/pandas for the Streamlit layer.
In a production setup, this is replaced by `dbt run`.
Reads from data/raw/, writes to data/marts/.
"""

import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR  = os.path.dirname(__file__)
RAW_DIR   = os.path.join(BASE_DIR, "..", "data", "raw")
MART_DIR  = os.path.join(BASE_DIR, "..", "data", "marts")
os.makedirs(MART_DIR, exist_ok=True)


def transform_hr_per_game():
    path = os.path.join(RAW_DIR, "wbc_historical_hr.csv")
    df = pd.read_csv(path)
    df = df.sort_values("edition")
    df["prev_hr_per_game"] = df["hr_per_game"].shift(1)
    df["pct_change_vs_prev"] = ((df["hr_per_game"] - df["prev_hr_per_game"]) / df["prev_hr_per_game"] * 100).round(2)
    out = os.path.join(MART_DIR, "mart_hr_per_game.csv")
    df.to_csv(out, index=False)
    logger.info(f"mart_hr_per_game written → {out}")
    return df


def transform_team_hr_2026():
    path = os.path.join(RAW_DIR, "wbc_2026_team_hr.csv")
    df = pd.read_csv(path)
    df["games_played"] = df["w"] + df["l"]
    df["hr_per_game"]  = (df["hr"] / df["games_played"].replace(0, 1)).round(2)
    df["hr_rank"]      = df["hr"].rank(method="min", ascending=False).astype(int)
    df["advancement_group"] = df["stage"].apply(
        lambda s: "Advanced" if s in ("Semifinals", "Finals")
        else ("Quarterfinals" if s == "Quarterfinals" else "Eliminated")
    )
    df = df.sort_values("hr_rank")
    out = os.path.join(MART_DIR, "mart_team_hr_2026.csv")
    df.to_csv(out, index=False)
    logger.info(f"mart_team_hr_2026 written → {out}")
    return df


def transform_multi_hr_games():
    path = os.path.join(RAW_DIR, "wbc_multi_hr_games.csv")
    df = pd.read_csv(path)
    df = df.sort_values("edition")
    out = os.path.join(MART_DIR, "mart_multi_hr_games.csv")
    df.to_csv(out, index=False)
    logger.info(f"mart_multi_hr_games written → {out}")
    return df


def run_all():
    logger.info("Running all transforms...")
    transform_hr_per_game()
    transform_team_hr_2026()
    transform_multi_hr_games()
    logger.info("All marts ready.")


if __name__ == "__main__":
    run_all()
