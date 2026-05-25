-- ============================================

-- CAMADA BRONZE: Vendas (Dados Brutos)

-- ============================================

-- Conceito: Primeira camada da arquitetura Medalhão

-- Objetivo: Capturar dados exatamente como vêm da fonte



SELECT 

    id_venda,

    id_cliente,

    id_produto,

     quantidade,

    canal_venda,

    preco_unitario,

    data_venda

FROM {{ source('raw', 'vendas') }}