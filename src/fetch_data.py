import requests
import datetime
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.utils.email_alert import send_email_alert

# Load environment variables
load_dotenv()

# Setup logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def fetch_exchange_rates(start_date, end_date=None, base_currency='EUR'):
    try:
        # Determine the filename
        filename = (
            f"exchange_{start_date}_to_{end_date}.json"
            if end_date else f"exchange_{start_date}.json"
        )
        file_path = Path("data/raw") / filename

        # Skip if file already exists
        if file_path.exists():
            logging.info(f"📦 File already exists: {filename} — skipping fetch.")
            return

        # Construct URL
        if end_date:
            url = f"https://api.frankfurter.app/{start_date}..{end_date}?from={base_currency}"
        else:
            url = f"https://api.frankfurter.app/{start_date}?from={base_currency}"

        # Fetch data
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Save file
        raw_dir = Path("data/raw")
        raw_dir.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(data, f)

        logging.info(f"✅ Fetched data saved to: {filename}")

    except Exception as e:
        logging.error(f"❌ Fetch failed: {e}")
        send_email_alert(f"Fetch failed: {e}")

if __name__ == "__main__":
    # Default: fetch today’s data
    today = datetime.date.today().isoformat()

    # Call the function (use only one at a time)
    fetch_exchange_rates(today)

    # Uncomment to fetch a historical range instead
    #fetch_exchange_rates("2024-01-01", "2025-05-31")
