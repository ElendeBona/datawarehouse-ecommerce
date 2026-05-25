"""
Ingestão de Dados — CSV → PostgreSQL (schema raw)
==================================================
Lê os CSVs gerados e popula as tabelas raw.* no banco.

Uso:
    python ingestion/load_raw.py

Pré-requisitos:
    - Docker rodando: docker compose up -d
    - CSVs gerados:   python data/scripts/generate_data.py
    - .env configurado (copiar de .env.example)
"""

import os
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────
load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("POSTGRES_HOST", "localhost"),
    "port":     int(os.getenv("POSTGRES_PORT", 5432)),
    "dbname":   os.getenv("POSTGRES_DB", "ecommerce"),
    "user":     os.getenv("POSTGRES_USER", "dw_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "dw_password"),
}

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"

TABELAS = {
    "raw.clientes": {
        "arquivo": "clientes.csv",
        "colunas": ["id_cliente", "nome_cliente", "estado", "pais", "data_cadastro"],
    },
    "raw.produtos": {
        "arquivo": "produtos.csv",
        "colunas": ["id_produto", "nome_produto", "categoria", "marca", "preco", "data_criacao"],
    },
    "raw.vendas": {
        "arquivo": "vendas.csv",
        "colunas": ["id_venda", "data_venda", "id_cliente", "id_produto", "canal_venda", "quantidade", "preco_unitario"],
    },
    "raw.preco_competidores": {
        "arquivo": "preco_competidores.csv",
        "colunas": ["id_produto", "nome_concorrente", "preco_concorrente", "data_coleta"],
    },
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def truncate_and_load(conn, tabela: str, df: pd.DataFrame, colunas: list):
    """Limpa a tabela e insere todos os registros em batch."""
    with conn.cursor() as cur:
        cur.execute(f"TRUNCATE TABLE {tabela} RESTART IDENTITY CASCADE")
        rows = [tuple(row[col] for col in colunas) for _, row in df.iterrows()]
        cols_str = ", ".join(colunas)
        execute_values(
            cur,
            f"INSERT INTO {tabela} ({cols_str}) VALUES %s",
            rows,
            page_size=1000,
        )
    conn.commit()
    return len(rows)


def main():
    print("\n🚀 Iniciando ingestão de dados para o PostgreSQL...\n")

    # Verifica se os CSVs existem
    for tabela, config in TABELAS.items():
        arquivo = DATA_DIR / config["arquivo"]
        if not arquivo.exists():
            print(f"❌ Arquivo não encontrado: {arquivo}")
            print("   Execute primeiro: python data/scripts/generate_data.py")
            return

    # Conecta ao banco
    print(f"🔌 Conectando ao banco: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")
    try:
        conn = get_connection()
        print("   ✓ Conexão estabelecida\n")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        print("   Verifique se o Docker está rodando: docker compose up -d")
        return

    # Carrega cada tabela
    total_registros = 0
    for tabela, config in TABELAS.items():
        arquivo = DATA_DIR / config["arquivo"]
        print(f"📥 Carregando {tabela}...")
        df = pd.read_csv(arquivo)
        n = truncate_and_load(conn, tabela, df, config["colunas"])
        print(f"   ✓ {n:,} registros inseridos")
        total_registros += n

    conn.close()
    print(f"\n✅ Ingestão concluída! {total_registros:,} registros no total.")
    print("   Próximo passo: executar os modelos dbt")
    print("   cd dbt/ecommerce && dbt run")


if __name__ == "__main__":
    main()
