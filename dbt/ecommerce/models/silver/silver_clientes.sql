-- ============================================
-- CAMADA SILVER: Clientes
-- ============================================
-- Conceito: Segunda camada da arquitetura Medalhão
-- Objetivo: Criar colunas calculadas a partir dos dados brutos
SELECT  
    id_cliente,

    nome_cliente,

    estado,

    pais,

    data_cadastro,
    -- Exemplo de coluna calculada: Ano de cadastro
    EXTRACT(YEAR FROM data_cadastro::timestamp) AS ano_cadastro        
FROM {{ ref( 'bronze_clientes') }}