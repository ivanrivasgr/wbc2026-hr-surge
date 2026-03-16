# ⚾ WBC 2026 — Home Run Surge Analytics

A data engineering portfolio project exploring the unprecedented home run surge
at the 2026 World Baseball Classic, built with a layered pipeline architecture.

## 🏗️ Architecture

```
Baseball Reference / MLB.com (public datasets)
        │
        ▼
[ ingestion/ingest_wbc.py ]    ← Python · requests · pandas
        │  Extracts raw game, team, and moment data
        ▼
[ data/raw/*.csv ]             ← Raw layer (versioned in repo)
        │
        ▼
[ transform/run_transforms.py ]← Simulates dbt mart logic
[ transform/models/marts/*.sql]← dbt SQL models (documented)
        │  Cleans, enriches, ranks, computes YoY metrics
        ▼
[ data/marts/*.csv ]           ← Mart layer (clean, analysis-ready)
        │
        ▼
[ app/streamlit_app.py ]       ← Streamlit · Plotly · deployed on Railway
```

## 📁 Project Structure

```
wbc2026-analytics/
├── ingestion/
│   └── ingest_wbc.py          # Data ingestion pipeline
├── transform/
│   ├── run_transforms.py      # Python transform runner (dbt equivalent)
│   ├── dbt_project.yml        # dbt project config
│   └── models/
│       └── marts/
│           ├── mart_hr_per_game.sql    # Historical HR trend mart
│           └── mart_team_hr_2026.sql  # Team power metrics mart
├── data/
│   ├── raw/                   # Raw ingested CSVs
│   └── marts/                 # Transformed mart CSVs
├── app/
│   └── streamlit_app.py       # Dashboard application
├── .streamlit/
│   └── config.toml            # Streamlit server config
├── Procfile                   # Railway deploy config
├── requirements.txt
└── README.md
```

## 🚀 Local Setup

```bash
# 1. Clone and install
git clone https://github.com/yourusername/wbc2026-analytics
cd wbc2026-analytics
pip install -r requirements.txt

# 2. Run the pipeline
python ingestion/ingest_wbc.py
python transform/run_transforms.py

# 3. Launch the app
streamlit run app/streamlit_app.py
```

## 🚢 Deploy to Railway

1. Push to GitHub
2. Connect repo on [railway.app](https://railway.app)
3. Railway auto-detects `Procfile` — no configuration needed
4. Set environment variables if needed (none required for this project)

## 📊 What's Inside

| Chart | Description |
|-------|-------------|
| HR per Game — Historical | Bar chart comparing all 6 WBC editions |
| Multi-HR Games per Edition | Record-tracking bar chart |
| HR by Team (2026) | Horizontal bar with advancement color coding |
| Power vs Advancement | Scatter plot: HR rate × games played × total HRs |
| Key Moments | Historic firsts and notable power moments |

## 📦 Data Sources

- **Baseball Reference** — 2026 WBC stats (public)
- **MLB.com** — Pool play summaries and facts/figures
- **Baseball America** — Schedule, scores, and context

## 🛠️ Stack

| Layer | Tool |
|-------|------|
| Ingestion | Python, pandas, requests |
| Transform | dbt Core (SQL models) + Python runner |
| Serving | Streamlit |
| Deploy | Railway |
| Visualization | Plotly |

## ⚠️ Limitations

- Pool play data only (32 games); knockout stage ongoing
- No Statcast (exit velocity, launch angle) for WBC games
- Small sample: 20 teams, 5 games each in pool play
- Roster selection bias and pitching limits not controlled for

## 💬 Community Question

Do you think the WBC home run surge reflects true offensive evolution,
or is it mostly a product of pitchers operating under strict inning limits
and unfamiliar batters? How would you model tournament-context adjustments?

---
Built by [Your Name] · March 2026 · Portfolio project
