--============================================      

-- CAMADA SILVER: Produtos (Dados Limpos) - limpa e padroniza, nunca agrega.    

--============================================
-- Conceito: Segunda camada da arquitetura Medalhão
-- Objetivo: Criar colunas calculadas a partir dos dados brutos

SELECT
    
    id_produto,

    nome_produto,

    categoria,

    marca,

    preco,

    data_criacao,
    -- Exemplo de coluna calculada: faixa de preço
    CASE 
        WHEN preco < 50 THEN 'Barato'
        WHEN preco BETWEEN 50 AND 200 THEN 'Médio'
        ELSE 'Caro'
    END AS faixa_preco
FROM {{ ref('bronze_produtos') }}