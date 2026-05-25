-- ============================================
-- CAMADA GOLD: KPI - Preços
-- ============================================
-- Conceito: Terceira camada da arquitetura Medalhão
-- Objetivo: Criar métricas de negócio prontas para análise relacionadas a preços dos produtos e concorrentes   
-- Responde:
-- 1. Qual é o preço médio dos produtos por categoria?
-- 2. Qual é a faixa de preço mais comum para cada marca?
-- 3. Qual é a diferença de preço entre nossos produtos e os concorrentes?
-- 4. Qual é a evolução do preço médio dos produtos ao longo do tempo?
-- 5. Como está nossa competitividade de preço?
-- 6. Somos mais caros ou mais baratos que os concorrentes?
-- 7. Qual a diferença percentual vs média do mercado?
-- 8. Quais categorias estamos fora do preço?

WITH precos_mercado AS (
    SELECT
        id_produto,
        AVG(preco_concorrente)           AS preco_medio_concorrentes,
        MAX(preco_concorrente)           AS preco_max_concorrentes,
        MIN(preco_concorrente)           AS preco_min_concorrentes,
        COUNT(DISTINCT nome_concorrente) AS qtd_concorrentes
    FROM {{ ref('silver_preco_competidores') }}
    GROUP BY 1
),

-- KPI 4: evolução do preço médio ao longo do tempo
evolucao_preco AS (
    SELECT
        id_produto,
        ano_coleta,
        mes_coleta,
        AVG(preco_concorrente) AS preco_medio_mensal
    FROM {{ ref('silver_preco_competidores') }}
    GROUP BY 1, 2, 3
),

-- KPI 2: faixa de preço mais comum por marca
faixa_por_marca_contagem AS (
    -- Passo 1: conta cada faixa por marca com GROUP BY
    SELECT
        marca,
        faixa_preco,
        COUNT(*) AS contagem
    FROM {{ ref('silver_produtos') }}
    GROUP BY 1, 2
),

faixa_por_marca AS (
    -- Passo 2: agora aplica o RANK sobre o resultado
    SELECT
        marca,
        faixa_preco,
        RANK() OVER (PARTITION BY marca ORDER BY contagem DESC) AS rank_faixa
    FROM faixa_por_marca_contagem
)

SELECT
    p.id_produto,
    p.nome_produto,
    p.categoria,
    p.marca,
    p.preco                              AS nosso_preco,
    -- KPI 1: preço médio por categoria
    AVG(p.preco) OVER (PARTITION BY p.categoria) AS preco_medio_categoria,
    -- KPI 2: faixa de preço mais comum por marca
    f.faixa_preco                        AS faixa_predominante_marca,
    -- KPI 3: diferença vs concorrentes
    m.preco_medio_concorrentes,
    m.preco_max_concorrentes,
    m.preco_min_concorrentes,
    ROUND((p.preco - m.preco_medio_concorrentes)
        / m.preco_medio_concorrentes * 100, 2) AS diferenca_pct_vs_media,
    CASE
        WHEN p.preco > m.preco_max_concorrentes THEN 'Mais caro que todos'
        WHEN p.preco < m.preco_min_concorrentes THEN 'Mais barato que todos'
        WHEN p.preco > m.preco_medio_concorrentes THEN 'Acima da média'
        ELSE 'Abaixo da média'
    END AS classificacao_preco
FROM {{ ref('silver_produtos') }} p
JOIN precos_mercado m ON p.id_produto = m.id_produto
JOIN faixa_por_marca f ON p.marca = f.marca AND f.rank_faixa = 1