--============================================
-- CAMADA GOLD: Customer 360        
--============================================
-- Conceito: Terceira camada da arquitetura Medalhão    
-- Objetivo: Criar uma visão unificada do cliente, integrando dados de vendas, produtos, preços e comportamento de compra.
-- Responde:
-- 1. Quem são nossos clientes VIP?
-- 2. Qual a receita por cliente?
-- 3. Qual o ranking de clientes por receita?
-- 4. Qual o ticket médio por cliente?
-- 5. Quantas compras cada cliente fez?
-- 6. De qual estado vêm os melhores clientes?

WITH metricas_cliente AS (
    -- Etapa 1: agrega métricas por cliente
    SELECT
        v.id_cliente,
        SUM(v.receita_total)        AS receita_total, -- 2. receita por cliente
        COUNT(DISTINCT v.id_venda)  AS total_compras, -- 5. quantas compras cada cliente fez
        AVG(v.receita_total)        AS ticket_medio -- 4. ticket médio por cliente
    FROM {{ ref('silver_vendas') }} v
    GROUP BY 1
)

SELECT
    c.id_cliente,
    c.nome_cliente,
    c.estado, -- 6. de qual estado vêm os melhores clientes?
    c.data_cadastro,
    m.receita_total,
    m.total_compras,
    m.ticket_medio,
    -- 3. ranking
    RANK() OVER (ORDER BY m.receita_total DESC) AS ranking_receita,
    -- 1. segmentação VIP
    CASE
        WHEN m.receita_total >= {{ var('vip_threshold') }}     THEN 'VIP'
        WHEN m.receita_total >= {{ var('top_tier_threshold') }} THEN 'Top Tier'
        ELSE 'Regular'
    END AS segmento_cliente
FROM {{ ref('silver_clientes') }} c
JOIN metricas_cliente m ON c.id_cliente = m.id_cliente

