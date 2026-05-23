"""
Exporta as 4 tabelas Gold do PostgreSQL local para CSVs em dashboard/data/
Rode uma vez antes do deploy (ou sempre que rodar dbt run com dados novos).
"""
import os
import pandas as pd
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=int(os.getenv("POSTGRES_PORT", 5433)),
    dbname=os.getenv("POSTGRES_DB", "ecommerce"),
    user=os.getenv("POSTGRES_USER", "dw_user"),
    password=os.getenv("POSTGRES_PASSWORD", "dw_password"),
)

out = Path(__file__).parent / "data"
out.mkdir(exist_ok=True)

tables = [
    "gold_kpis_vendas",
    "gold_customer_360",
    "gold_kpis_produtos",
    "gold_kpis_pricing",
]

for t in tables:
    df = pd.read_sql_query(f"SELECT * FROM raw.{t}", conn)
    df.to_csv(out / f"{t}.csv", index=False)
    print(f"OK {t}.csv ({len(df)} linhas)")

conn.close()
print(f"\nExportacao concluida -> {out}")
