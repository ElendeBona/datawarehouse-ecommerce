-- ============================================
-- CAMADA GOLD: KPI - Produtos
-- ============================================
-- Conceito: Terceira camada da arquitetura Medalhão
-- Objetivo: Criar métricas de negócio prontas para análise
-- Precisa responder algumas perguntas de negócio:
-- 1. Quais produtos mais vendidos?
-- 2. Quais categorias vendem mais?
-- 3. Quais produtos têm maior receita?
-- 4. Quais produtos estão em queda de vendas?
-- 5. Qual é o ranking de produtos por receita?

WITH vendas_por_produto AS (
    -- Etapa 1: aggregates com GROUP BY
    SELECT
        p.id_produto,
        p.nome_produto,
        p.categoria,
        p.marca,
        p.preco,
        p.faixa_preco,
        SUM(v.quantidade)    AS total_vendido,
        SUM(v.receita_total) AS receita_total,
        COUNT(DISTINCT v.id_venda) AS total_pedidos,
        -- Queda de vendas
        SUM(CASE WHEN v.data_venda_date >= CURRENT_DATE - INTERVAL '3 months' 
            THEN v.quantidade ELSE 0 END) AS vendas_ultimos_3m,
        SUM(CASE WHEN v.data_venda_date >= CURRENT_DATE - INTERVAL '6 months' 
            AND v.data_venda_date < CURRENT_DATE - INTERVAL '3 months' 
            THEN v.quantidade ELSE 0 END) AS vendas_3m_anteriores
    FROM {{ ref('silver_vendas') }} v
    JOIN {{ ref('silver_produtos') }} p ON v.id_produto = p.id_produto
    GROUP BY 1, 2, 3, 4, 5, 6
)

-- Etapa 2: window functions sobre o resultado agregado
SELECT
    *,
    SUM(total_vendido) OVER (PARTITION BY categoria) AS total_vendido_categoria,
    AVG(preco) OVER (PARTITION BY categoria)         AS preco_medio_categoria,
    RANK() OVER (ORDER BY receita_total DESC)        AS ranking_receita,
    CASE 
        WHEN vendas_ultimos_3m < vendas_3m_anteriores THEN 'Queda de Vendas'
        ELSE 'Estável ou Crescendo'
    END AS status_vendas
FROM vendas_por_produto