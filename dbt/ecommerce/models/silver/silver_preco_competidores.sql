--============================================
-- CAMADA SILVER: Preços dos Competidores           

-- ============================================
-- Conceito: Segunda camada da arquitetura Medalhão
-- Objetivo: Criar colunas calculadas a partir dos dados brutos

SELECT
    
    id_produto,

    nome_concorrente,

    preco_concorrente,

    data_coleta,
    -- Dimensão temporal útil para análises
    EXTRACT(YEAR FROM data_coleta::timestamp) AS ano_coleta,
    EXTRACT(MONTH FROM data_coleta::timestamp) AS mes_coleta
FROM {{ ref('bronze_preco_competidores') }}

-- Exemplo de coluna calculada: diferença de preço em relação ao nosso preço
-- preco_concorrente - (SELECT preco FROM {{ ref('bronze_produtos') }} WHERE id_produto = {{ ref('bronze_preco_competidores') }}.id_produto) AS diferenca_preco    
