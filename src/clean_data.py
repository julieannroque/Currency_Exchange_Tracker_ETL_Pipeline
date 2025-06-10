import json
import pandas as pd
from pathlib import Path
import datetime
import sys
import logging
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.utils.email_alert import send_email_alert

# Logging setup
logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def clean_json(file_path):
    try:
        with open(file_path) as f:
            data = json.load(f)

        processed_path = Path("data/processed")
        processed_path.mkdir(parents=True, exist_ok=True)

        # Check for multi-day range format
        if "rates" in data and isinstance(list(data['rates'].values())[0], dict):
            rows = []
            for date, rates in data["rates"].items():
                for currency, rate in rates.items():
                    rows.append({
                        "date": date,
                        "base": data["base"],
                        "currency": currency,
                        "rate": rate
                    })
            df = pd.DataFrame(rows)
            start = list(data['rates'].keys())[0]
            end = list(data['rates'].keys())[-1]
            filename = f"cleaned_{start}_to_{end}.csv"
            logging.info(f"✅ Cleaned data for range: {start} to {end}")

        else:
            # Single-day structure — use actual returned date
            date = data['date']
            df = pd.DataFrame(data['rates'].items(), columns=["currency", "rate"])
            df["base"] = data["base"]
            df["date"] = date
            filename = f"cleaned_{date}.csv"
            logging.info(f"✅ Cleaned data for single date: {date}")

        # Save the cleaned data
        df.to_csv(processed_path / filename, index=False)
        logging.info(f"✅ Cleaned data saved to: data/processed/{filename}")

    except Exception as e:
        logging.error(f"❌ Clean failed: {e}")
        send_email_alert(f"Clean failed: {e}")

if __name__ == "__main__":
    today = datetime.date.today().isoformat()
    default_file = Path(f"data/raw/exchange_{today}.json")

    # Allow override via command-line argument
    file = Path(sys.argv[1]) if len(sys.argv) > 1 else default_file

    if file.exists():
        clean_json(file)
    else:
        logging.error(f"❌ File not found: {file}")
        send_email_alert(f"Clean failed — file not found: {file}")
