import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import sys
import logging
from pathlib import Path
import glob
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.utils.email_alert import send_email_alert

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def load_to_postgres(csv_file):
    try:
        # Get DB credentials from .env
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")

        conn_str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(conn_str)

        df = pd.read_csv(csv_file)
        df.to_sql('exchange_rates', engine, if_exists='append', index=False)

        logging.info(f"✅ Loaded data into PostgreSQL from: {csv_file}")

    except Exception as e:
        logging.error(f"❌ Load failed: {e}")
        send_email_alert(f"Load failed: {e}")

if __name__ == "__main__":
    # Check if a file path was provided
    if len(sys.argv) > 1:
        file = Path(sys.argv[1])
    else:
        # Dynamically find the latest cleaned CSV file
        cleaned_files = sorted(glob.glob("data/processed/cleaned_*.csv"), reverse=True)
        if not cleaned_files:
            logging.error("❌ No cleaned CSV files found.")
            send_email_alert("Load failed — no cleaned CSV files found.")
            sys.exit(1)
        file = Path(cleaned_files[0])

    if file.exists():
        load_to_postgres(file)
    else:
        logging.error(f"❌ Cleaned file not found: {file}")
        send_email_alert(f"Load failed — file not found: {file}")
