O que é dbt em uma frase:

dbt transforma dados dentro do banco usando SQL — e trata esse SQL como código de verdade.

O que isso significa na prática:

Sem dbt você escreveria SQL solto, sem organização:

CREATE TABLE silver.vendas AS
SELECT *, quantidade * preco_unitario AS receita_total
FROM raw.vendas
Com dbt você escreve o mesmo SQL mas ganha:

Versionamento — tudo no Git
Dependências — ele sabe que Silver depende de Bronze
Testes — valida se os dados estão corretos
Documentação — gera automaticamente
Linhagem — gráfico visual de como os dados fluem
O dbt não move dados — ele só transforma.

raw.*  ← dados brutos (você já populou!)
  ↓ dbt
bronze.*  ← réplica limpa
  ↓ dbt  
silver.*  ← transformado
  ↓ dbt
gold.*    ← pronto para o dashboard