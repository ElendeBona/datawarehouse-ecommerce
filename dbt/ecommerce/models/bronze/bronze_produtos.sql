-- ============================================

-- CAMADA BRONZE: Produtos (Dados Brutos)

-- ============================================

-- Conceito: Primeira camada da arquitetura Medalhão

-- Objetivo: Capturar dados exatamente como vêm da fonte



SELECT
    
    id_produto,

    nome_produto,

    categoria,

    marca,

    preco,

    data_criacao

FROM {{ source('raw', 'produtos') }}