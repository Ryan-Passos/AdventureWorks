# Sobre o Projeto

O projeto foi dividido em duas partes:

## Parte 1 — Notebook de Análise de Dados

Nesta etapa, foi feita a manipulação e análise dos dados utilizando Python e bibliotecas de data science. Foram realizadas as seguintes etapas:

- Conexão e consulta ao banco de dados SQL Server (AdventureWorks)
- Limpeza e transformação dos dados com Pandas
- Agrupamentos por região, produto e período
- Criação de gráficos com Matplotlib

## Parte 2 — Dashboard Interativo

Nesta etapa, os dados tratados foram utilizados para criar um dashboard interativo com Streamlit. O dashboard permite:

- Filtrar dados por data, região e produto
- Visualizar indicadores (KPIs) como:
  - Total de Regiões Ativas
  - Total de Pedidos
  - Total Vendido (R$)
- Explorar gráficos interativos:
  - Top 10 Regiões com Maiores Vendas
  - Top 10 Produtos Mais Vendidos
  - Evolução Mensal das Vendas

## Bibliotecas Utilizadas

- Python 3.10+
- Pandas – Manipulação e tratamento dos dados (pip install pandas)
- Matplotlib / Seaborn / Plotly – Visualizações de dados (pip install matplotlib seaborn plotly)
- Streamlit – Criação do dashboard interativo (pip install streamlit
- CSS – Estilização do dashboard
- SQL Server – Origem dos dados (AdventureWorks)

## Como Rodar o Projeto

O projeto possui duas partes: o notebook de análise e o dashboard interativo. Siga as instruções abaixo para executar.

### 1. Notebook de Análise de Dados

- Baixe o arquivo `dataset.xlsx` e o notebook `Hexagon - Manipulação de Dados.ipynb`
- Abra o notebook no Google Colab ou no Jupyter Notebook
- Instale as bibliotecas necessárias:
```bash
pip install pandas matplotlib seaborn plotly openpyxl
```

### 2. Visualizar Dashboard

- No Terminal do Git digite:
```bash
git clone https://github.com/Ryan-Passos/AdventureWorks.git
```

- Tenha previamente o Python instalado na sua máquina

- Instale as seguintes bibliotecas:
```bash
pip install plotly
pip install openpyxl
python -m pip install streamlit
```

- No terminal, execute o dashboard com:
```bash
streamlit run app.py
```
