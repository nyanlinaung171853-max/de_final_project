# config/settings.py
import os
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Environment variable override
def get(key, default=None):
    keys = key.split(".")
    value = config
    for k in keys:
        value = value.get(k, {})
    return os.getenv(key.upper().replace(".", "_"), value or default)

API_URL = get("api.url")
KAFKA_BOOTSTRAP = get("kafka.bootstrap")
DB_HOST = get("database.host")
# ... etc