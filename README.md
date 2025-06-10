
💱 Currency Exchange Tracker – ETL Pipeline

A complete ETL pipeline that fetches, cleans, stores, and visualizes currency exchange rates using the [Frankfurter API](https://www.frankfurter.app/). Built with Python, PostgreSQL, and Tableau Public.

---

Project Goals

- Automate exchange rate data ingestion (daily + historical)
- Clean and normalize data for analysis
- Store data in PostgreSQL
- Visualize currency trends over time
- Add logging, error alerts, and automation

---

Tech Stack

| Component       | Tool / Tech              |
|-----------------|--------------------------|
| Extract         | Python `requests`        |
| Transform       | Python `pandas`          |
| Load            | PostgreSQL + SQLAlchemy  |
| Orchestration   | Manual or `run_etl.py`   |
| Logging         | `logging` module         |
| Notifications   | Email via SMTP           |
| Scheduling      | macOS/Linux `cron`       |
| Visualization   | Jupyter                  |

---

Project Structure
 
```
currency_tracker/
├── data/                  # Raw and processed data files
│   ├── raw/
│   └── processed/
├── logs/                  # Log files
├── notebooks/             # Jupyter notebooks for analysis
├── src/                   # Source scripts
│   ├── fetch_data.py
│   ├── clean_data.py
│   ├── load_to_db.py
│   ├── run_etl.py
│   └── utils/
│       └── email_alert.py
├── .env                   # Environment config (DB, email settings)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

 ```

---

Setup Instructions

1. Install Dependencies
 ```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
 ```

2. Configure `.env`
 ```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=currency_tracker
DB_USER=postgres
DB_PASSWORD=your_password_here

EMAIL_FROM=your_email@gmail.com
EMAIL_TO=receiver_email@gmail.com
EMAIL_SUBJECT=Currency Tracker ETL Alert
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
 ```

Use a [Gmail App Password](https://myaccount.google.com/apppasswords)

---
Python code overview

1. run_etl.py - Main orchestrator
   - Coordinates the 3-step process
   - Handles error logging and alerts
   - Tracks execution status

2. fetch_data.py - Extraction step
   - Gets exchange rates from Frankfurter API
   - Supports single date or date range
   - Saves raw JSON to data/raw/

3. clean_data.py - Transformation step
   - Processes raw JSON into structured CSV
   - Handles both single-day and multi-day formats
   - Saves cleaned data to data/processed/

4. load_to_db.py - Loading step
   - Imports CSV data to PostgreSQL
   - Uses SQLAlchemy for connection
   - Appends to existing table

---

How to Use

Run the full ETL (daily or on-demand):
 ```
python -m src.run_etl
 ```

Fetch Historical Data (example):

In `src/fetch_data.py`, uncomment this line:
 ```
fetch_exchange_rates("2025-01-01", "2025-06-05")
 ```

Then run:
 ```
python -m src.fetch_data
python -m src.clean_data data/raw/exchange_2024-12-31_to_2025-06-05.json
python -m src.load_to_db data/processed/cleaned_2024-12-31_to_2025-06-05.csv
 ```

---

Schedule with Cron (macOS/Linux)

Edit crontab:
 ```
crontab -e
 ```
Add:
 ```
0 9 * * * /Users/yourname/currency_tracker/venv/bin/python -m src.run_etl
 ```

---

Visualization with Jupyter

![image](https://github.com/user-attachments/assets/2176c26d-6ea9-4aa9-a1bb-6d818358d9ed)


---

Features

* ✅ Auto file naming
* ✅ Historical + live data support
* ✅ Logging (`logs/etl.log`)
* ✅ Email alerts on failure
* ✅ Latest-file detection
* ✅ Analysis and Visualization in Jupyter

---

Author

Julie Roque


