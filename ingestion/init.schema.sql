-- ============================================================
-- Inicialização dos Schemas do Data Warehouse
-- Executado automaticamente pelo Docker na primeira inicialização
-- ============================================================

-- Schema RAW: dados brutos vindos das fontes
CREATE SCHEMA IF NOT EXISTS raw;

-- Schema BRONZE: réplica 1:1 da raw (via dbt views)
CREATE SCHEMA IF NOT EXISTS bronze;

-- Schema SILVER: dados limpos e transformados (via dbt views)
CREATE SCHEMA IF NOT EXISTS silver;

-- Schema GOLD: camadas analíticas por domínio (via dbt)
CREATE SCHEMA IF NOT EXISTS gold_sales;
CREATE SCHEMA IF NOT EXISTS gold_cs;
CREATE SCHEMA IF NOT EXISTS gold_pricing;

-- ============================================================
-- Tabelas RAW
-- ============================================================

CREATE TABLE IF NOT EXISTS raw.vendas (
    id_venda        VARCHAR(50) PRIMARY KEY,
    data_venda      TIMESTAMP NOT NULL,
    id_cliente      VARCHAR(50) NOT NULL,
    id_produto      VARCHAR(50) NOT NULL,
    canal_venda     VARCHAR(30),
    quantidade      INTEGER NOT NULL,
    preco_unitario  NUMERIC(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.clientes (
    id_cliente      VARCHAR(50) PRIMARY KEY,
    nome_cliente    VARCHAR(150) NOT NULL,
    estado          VARCHAR(2) NOT NULL,
    pais            VARCHAR(50) DEFAULT 'Brasil',
    data_cadastro   TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.produtos (
    id_produto      VARCHAR(50) PRIMARY KEY,
    nome_produto    VARCHAR(200) NOT NULL,
    categoria       VARCHAR(80) NOT NULL,
    marca           VARCHAR(80),
    preco           NUMERIC(10, 2) NOT NULL,
    data_criacao    TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.preco_competidores (
    id              SERIAL PRIMARY KEY,
    id_produto      VARCHAR(50) NOT NULL,
    nome_concorrente VARCHAR(100) NOT NULL,
    preco_concorrente NUMERIC(10, 2) NOT NULL,
    data_coleta     TIMESTAMP NOT NULL
);
