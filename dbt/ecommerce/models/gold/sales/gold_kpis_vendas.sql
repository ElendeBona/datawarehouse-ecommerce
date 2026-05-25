-- ============================================
-- CAMADA GOLD: KPI - Vendas Temporais  
-- ============================================
-- Conceito: Terceira camada da arquitetura Medalhão
-- Objetivo: Criar métricas de negócio prontas para análise relacionadas a vendas ao longo do tempo
-- Responde:            
-- 1. Qual foi nossa receita total?
-- 2. Como as vendas evoluem ao longo do tempo?
-- 3. Qual o ticket médio?
-- 4. Quais os dias e horários de pico?
-- 5. Quantos clientes únicos por período?
-- 6. Qual o volume por canal de venda?

WITH vendas_temporais AS (
    SELECT
        data_venda_date, -- 2. evolução das vendas ao longo do tempo
        ano_venda,
        mes_venda, 
        dia_semana, -- 4. dias e horários de pico
        hora_venda, -- 4. dias e horários de pico
        canal_venda, -- 6. volume por canal de venda
        receita_total, -- 1. receita total
        id_venda,
        id_cliente
    FROM {{ ref('silver_vendas') }}
)           

SELECT
    data_venda_date, -- 2. evolução das vendas ao longo do tempo
    ano_venda,
    mes_venda, -- 2. evolução das vendas ao longo do tempo
    dia_semana, -- 4. dias e horários de pico
    hora_venda, -- 4. dias e horários de pico
    canal_venda, -- 6. volume por canal de venda
    SUM(receita_total)          AS receita_total, -- 1. receita total
    COUNT(DISTINCT id_venda)    AS total_pedidos, -- 2. evolução das vendas ao longo do tempo
    COUNT(DISTINCT id_cliente)  AS clientes_unicos, -- 5. clientes únicos por período
    AVG(receita_total)          AS ticket_medio -- 3. ticket médio
FROM vendas_temporais
GROUP BY 1, 2, 3, 4, 5, 6
ORDER BY data_venda_date, hora_venda


