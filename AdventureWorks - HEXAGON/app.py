import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================
# CONFIGURAÇÃO INICIAL
# ======================================
# Define o título da página e usa o layout "wide" (tela cheia)
st.set_page_config(page_title="AdventureWorks - Pedidos", layout="wide")

# ======================================
# IMPORTA O CSS PERSONALIZADO
# ======================================
# Carrega o arquivo CSS com as configurações de estilo
with open("styles/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ======================================
# LEITURA DOS DADOS
# ======================================
# Lê os dados do arquivo Excel e renomeia as colunas
df = pd.read_excel("dataset.xlsx")

df = df.rename(columns={
    'DT_PEDIDO': 'DATA',
    'NO_VALOR_TOTAL': 'VENDA',
    'DS_REGIAO': 'REGIAO',
    'DS_PRODUTO': 'PRODUTO'
})

# Converte a coluna de datas para o formato datetime
df['DATA'] = pd.to_datetime(df['DATA'])

# ======================================
# TÍTULO DO DASHBOARD
# ======================================
st.markdown("<h2 style='font-weight:700;'>AdventureWorks - Pedidos</h2>", unsafe_allow_html=True)

# ======================================
# FILTROS
# ======================================
# Cria três colunas para os filtros principais
col1, col2, col3 = st.columns(3)

# Captura a data mínima e máxima do dataset
data_min, data_max = df['DATA'].min(), df['DATA'].max()

# Filtro de intervalo de datas
with col1:
    data_selecionada = st.date_input(
        "Intervalo de Datas",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max
    )

# Filtro de regiões
with col2:
    regiao_selecionada = st.multiselect("Região", df['REGIAO'].unique())

# Filtro de produtos
with col3:
    produto_selecionado = st.multiselect("Produto", df['PRODUTO'].unique())

# ======================================
# FILTRAGEM DOS DADOS
# ======================================
df_filtrado = df.copy()

# Filtra o intervalo de datas selecionado
if isinstance(data_selecionada, tuple) and len(data_selecionada) == 2:
    inicio, fim = map(pd.to_datetime, data_selecionada)
    df_filtrado = df_filtrado[(df_filtrado['DATA'] >= inicio) & (df_filtrado['DATA'] <= fim)]
else:
    df_filtrado = df_filtrado[df_filtrado['DATA'].between(data_min, data_max)]

# Filtra pelas regiões escolhidas
if regiao_selecionada:
    df_filtrado = df_filtrado[df_filtrado['REGIAO'].isin(regiao_selecionada)]

# Filtra pelos produtos escolhidos
if produto_selecionado:
    df_filtrado = df_filtrado[df_filtrado['PRODUTO'].isin(produto_selecionado)]

# ======================================
# INDICADORES (KPIs)
# ======================================
# Cria três colunas para mostrar os indicadores principais
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

# Define os valores e estilos de cada indicador
kpis = [
    {"titulo": "Total de Regiões Ativas", "valor": df_filtrado['REGIAO'].nunique(), "classe": "border-blue"},
    {"titulo": "Total de Pedidos", "valor": len(df_filtrado), "classe": "border-yellow"},
    {"titulo": "Total Vendido (R$)", "valor": f"{df_filtrado['VENDA'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), "classe": "border-green"}
]

# Exibe cada indicador na tela
for kpi, col in zip(kpis, [kpi_col1, kpi_col2, kpi_col3]):
    with col:
        st.markdown(f"""
        <div class="metric-container {kpi['classe']}">
            <div class="metric-label">{kpi['titulo']}</div>
            <div class="metric-value">{kpi['valor']}</div>
        </div>
        """, unsafe_allow_html=True)

# ======================================
# FUNÇÃO DE AJUSTE VISUAL DOS GRÁFICOS
# ======================================
# Essa função deixa os gráficos com o mesmo estilo (cores e margens)
def configure_plotly_layout(fig, title):
    fig.update_layout(
        title=f"<b>{title}</b>",
        title_x=0.5,
        plot_bgcolor='#172A46',
        paper_bgcolor='#172A46',
        font=dict(color='white'),
        margin=dict(t=50, b=50, l=20, r=20),
        xaxis=dict(gridcolor='#2A405F', linecolor='#2A405F'),
        yaxis=dict(gridcolor='#2A405F', linecolor='#2A405F'),
    )
    return fig

# ======================================
# GRÁFICO - TOP 10 REGIÕES
# ======================================
col_g1, col_g2 = st.columns(2)

with col_g1:
    top_regioes = (
        df_filtrado.groupby('REGIAO', as_index=False)['VENDA']
        .sum()
        .sort_values('VENDA', ascending=False)
        .head(10)
    )

    # Cria o gráfico de barras horizontal
    fig1 = px.bar(
        top_regioes.sort_values('VENDA'),
        x='VENDA', y='REGIAO',
        orientation='h',
        text=top_regioes['VENDA'].apply(lambda x: f'R$ {x:,.0f}'),
        color='VENDA',
        color_continuous_scale=px.colors.sequential.Cividis
    )

    fig1.update_traces(textposition='outside', marker_color='#4AD9E8')
    fig1 = configure_plotly_layout(fig1, 'Top 10 Regiões com Maiores Vendas')
    st.plotly_chart(fig1, use_container_width=True)

# ======================================
# GRÁFICO - TOP 10 PRODUTOS
# ======================================
with col_g2:
    top_produtos = (
        df_filtrado.groupby('PRODUTO', as_index=False)['VENDA']
        .sum()
        .sort_values('VENDA', ascending=False)
        .head(10)
    )

    # Cria o gráfico de barras vertical
    fig2 = px.bar(
        top_produtos,
        x='PRODUTO', y='VENDA',
        text=top_produtos['VENDA'].apply(lambda x: f'R$ {x:,.0f}'),
        color='VENDA',
        color_continuous_scale=px.colors.sequential.Plasma
    )

    fig2.update_traces(textposition='outside', marker_color='#FFA500')
    fig2 = configure_plotly_layout(fig2, 'Top 10 Produtos Mais Vendidos')
    st.plotly_chart(fig2, use_container_width=True)

# ======================================
# GRÁFICO - EVOLUÇÃO MENSAL DAS VENDAS
# ======================================
# Cria uma coluna com o mês/ano e soma as vendas
df_mes = df_filtrado.assign(MES_ANO=df_filtrado['DATA'].dt.to_period('M').astype(str))
df_mes = df_mes.groupby('MES_ANO', as_index=False)['VENDA'].sum().sort_values('MES_ANO')

# Gráfico de linha com a evolução das vendas
fig3 = px.line(
    df_mes, x='MES_ANO', y='VENDA', markers=True,
    line_shape='spline', color_discrete_sequence=['#4AD9E8']
)

fig3.update_traces(
    text=df_mes['VENDA'].apply(lambda x: f'R$ {x:,.0f}'),
    textposition='top center',
    marker=dict(size=10, color='#4AD9E8', line=dict(width=2, color='white')),
    line=dict(width=4)
)

fig3 = configure_plotly_layout(fig3, 'Evolução das Vendas por Mês')
st.plotly_chart(fig3, use_container_width=True)
