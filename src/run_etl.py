import datetime
import subprocess
import glob
import logging
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.utils.email_alert import send_email_alert

# Setup logging
logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def run_step(step_name, command):
    try:
        logging.info(f"🚀 Starting: {step_name}")
        subprocess.run(command, check=True)
        logging.info(f"✅ Finished: {step_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Failed: {step_name} — {e}")
        send_email_alert(f"{step_name} failed:\n{e}")
        raise

if __name__ == "__main__":
    try:
        today = datetime.date.today().isoformat()
        raw_file = f"data/raw/exchange_{today}.json"
        processed_file = f"data/processed/cleaned_{today}.csv"

        # Step 1: Fetch data
        run_step("Fetch Data", [sys.executable, "-m", "src.fetch_data"])

        # Step 2: Clean data (find latest cleaned file)
        cleaned_files = sorted(glob.glob("data/raw/exchange_*.json"), reverse=True)
        if not cleaned_files:
            raise FileNotFoundError("❌ No raw exchange files found.")
        latest_raw = cleaned_files[0]
        run_step("Clean Data", [sys.executable, "-m", "src.clean_data", latest_raw])

        # Step 3: Load data (find latest cleaned file)
        cleaned_csvs = sorted(glob.glob("data/processed/cleaned_*.csv"), reverse=True)
        if not cleaned_csvs:
            raise FileNotFoundError("❌ No cleaned CSV files found.")
        latest_cleaned = cleaned_csvs[0]
        run_step("Load to DB", [sys.executable, "-m", "src.load_to_db", latest_cleaned])

        logging.info("🎉 ETL pipeline completed successfully.")

    except Exception as e:
        logging.error(f"❌ ETL pipeline failed: {e}")
        send_email_alert(f"ETL pipeline failed:\n{e}")
