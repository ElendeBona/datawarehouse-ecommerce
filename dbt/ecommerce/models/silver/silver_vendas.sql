-- ============================================
-- CAMADA SILVER: Vendas (Dados Limpos) - limpa e padroniza, nunca agrega.
-- ============================================
-- Conceito: Segunda camada da arquitetura Medalhão
-- Objetivo: Criar colunas calculadas a partir dos dados brutos

SELECT 

    id_venda,

    id_cliente,

    id_produto,

    quantidade,

    canal_venda,

    preco_unitario,

    data_venda,

-- Colunas calculadas
    quantidade * preco_unitario AS receita_total,
-- Dimensões temporais
    DATE(data_venda::timestamp) AS data_venda_date,
    EXTRACT(YEAR FROM data_venda::timestamp) AS ano_venda,
    EXTRACT(MONTH FROM data_venda::timestamp) AS mes_venda,
    EXTRACT(DAY FROM data_venda::timestamp) AS dia_venda,
    EXTRACT(DOW FROM data_venda::timestamp) AS dia_semana, -- 0 = Domingo, 6 = Sábado
    EXTRACT(HOUR FROM data_venda::timestamp) AS hora_venda
from {{ ref('bronze_vendas') }} 



-- Receita por categoria
--    SUM(quantidade * preco_unitario) / COUNT(DISTINCT categoria) AS receita_por_categoria
    -- Receita por canal
--    SUM(quantidade * preco_unitario) / COUNT(DISTINCT canal_venda) AS receita_por_canal


