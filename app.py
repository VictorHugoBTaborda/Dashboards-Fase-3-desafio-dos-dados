
import streamlit as st
import pandas as pd
import plotly.express as px

# --- ESTILO (O equivalente ao seu style.css) ---
st.set_page_config(page_title="Dashboard Logístico", layout="wide")

# Injetando um CSS personalizado para deixar o visual ainda mais profissional
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allowed_html=True)

# --- ESTRUTURA DA PÁGINA (O equivalente ao seu index.html) ---
st.title("🚨 Dashboard Inteligente de Monitoramento Logístico")
st.markdown("Análise estratégica de entregas e monitoramento de atrasos em tempo real.")
st.divider()

# Dados fornecidos no exercício
dados = {
    'id_entrega': [301, 302, 303, 304, 305, 306, 307, 308, 309, 310],
    'transportadora': ['RotaMax', 'ViaCargo', 'FlashLog', 'RotaMax', 'ViaCargo', 'FlashLog', 'RotaMax', 'ViaCargo', 'FlashLog', 'ViaCargo'],
    'regiao': ['Sudeste', 'Sul', 'Nordeste', 'Norte', 'Centro-Oeste', 'Sul', 'Sul', 'Sudeste', 'Norte', 'Nordeste'],
    'prazo_dias': [3, 5, 4, 6, 2, 5, 6, 3, 5, 4],
    'dias_reais': [7, 5, 9, 4, 6, 12, 9, 4, 5, 8]
}
df = pd.DataFrame(dados)

# --- LÓGICA E INTERAÇÃO (O equivalente ao seu script.js) ---
df['atrasou'] = df['dias_reais'] > df['prazo_dias']
df['dias_atraso'] = (df['dias_reais'] - df['prazo_dias']).apply(lambda x: x if x > 0 else 0)
df['status'] = df['atrasou'].map({True: '🚨 Atrasado', False: '✅ No Prazo'})

# Barra lateral com filtros interativos
st.sidebar.header("Filtros Operacionais")
regiao_sel = st.sidebar.multiselect("Filtrar por Região:", options=df['regiao'].unique(), default=df['regiao'].unique())
transp_sel = st.sidebar.multiselect("Filtrar por Transportadora:", options=df['transportadora'].unique(), default=df['transportadora'].unique())

# Aplicando os filtros dinamicamente
df_filtrado = df[df['regiao'].isin(regiao_sel) & df['transportadora'].isin(transp_sel)]

# Indicadores (Cartões de resumo)
total_entregas = len(df_filtrado)
total_atrasos = df_filtrado['atrasou'].sum()
taxa_atraso = (total_atrasos / total_entregas * 100) if total_entregas > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Entregas", f"{total_entregas}")
with col2:
    st.metric("Entregas com Atraso", f"{total_atrasos}")
with col3:
    st.metric("Taxa de Atraso (%)", f"{taxa_atraso:.1f}%")

st.divider()

# Gráficos em colunas
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("⚠️ Atrasos por Transportadora")
    df_transp = df_filtrado[df_filtrado['atrasou'] == True].groupby('transportadora').size().reset_index(name='qtd')
    fig_barra = px.bar(df_transp, x='transportadora', y='qtd', labels={'qtd': 'Nº de Atrasos'}, color='transportadora')
    st.plotly_chart(fig_barra, use_container_width=True)

with col_g2:
    st.subheader("🗺️ Distribuição de Atrasos por Região")
    df_regiao = df_filtrado[df_filtrado['atrasou'] == True].groupby('regiao').size().reset_index(name='qtd')
    fig_pizza = px.pie(df_regiao, values='qtd', names='regiao')
    st.plotly_chart(fig_pizza, use_container_width=True)

st.divider()

# Tabela de classificação/ranking
st.subheader("📋 Ranking de Prioridade (Maiores Atrasos no Topo)")
df_ranking = df_filtrado.sort_values(by='dias_atraso', ascending=False)
st.dataframe(df_ranking[['id_entrega', 'transportadora', 'regiao', 'prazo_dias', 'dias_reais', 'dias_atraso', 'status']], use_container_width=True)