from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# Data Directories
# =========================

DATA_DIR = BASE_DIR / "data"

BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"

CHECKPOINT_DIR = DATA_DIR / "checkpoints"
DLQ_DIR = DATA_DIR / "dlq"
STATE_DIR = DATA_DIR / "state"

WAREHOUSE_DIR = DATA_DIR / "warehouse"

LOG_DIR = BASE_DIR / "logs"


# =========================
# API Configuration
# =========================

API_URL = os.getenv(
    "API_URL",
    "https://dummyjson.com/products"
)

REQUEST_TIMEOUT = int(
    os.getenv("REQUEST_TIMEOUT", "30")
)


# =========================
# Environment
# =========================

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)