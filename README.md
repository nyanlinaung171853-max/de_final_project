@"
# DE Project Final — E-commerce Data Pipeline

## Architecture
- **Batch**: API → Bronze → Silver → Gold → Postgres
- **Streaming**: Kafka → Silver → Gold → Postgres
- **Medallion Architecture** (Bronze/Silver/Gold)
- **Star Schema** in Postgres

## Tech Stack
- Docker + Docker Compose
- Apache Spark 3.5 (PySpark)
- Apache Kafka 7.5
- PostgreSQL 16
- Apache Airflow 2.9

## Quick Start
\`\`\`bash
docker compose up -d
docker exec spark-master /opt/spark/bin/spark-submit /app/batch/run_batch.py
\`\`\`

## Structure
- \`src/\` — Shared modules
- \`batch/\` — Batch pipeline
- \`streaming/\` — Kafka streaming
- \`spark/\` — Spark jobs
- \`airflow/\` — Orchestration
- \`sql/\` — Database schema
- \`tests/\` — Unit tests

## Testing
\`\`\`bash
pytest tests/ -v
\`\`\`
"@ | Out-File -FilePath README.md -Encoding utf8