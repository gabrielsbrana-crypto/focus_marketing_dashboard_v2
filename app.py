
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 FOCUS MARKETING DASHBOARD — V2 (FORCE BUILD)",
                   page_icon="📊", layout="wide")

st.markdown("""
<div style="padding:14px;border:2px dashed #FF6600;border-radius:14px;margin:8px 0 18px 0;">
  <h2 style="margin:0;color:#FF6600;">FOCUS BUILD V2 ✅ — Se você está vendo esta faixa, este é o app da Focus.</h2>
  <p style="margin:6px 0 0 0;">Se ainda aparecer o dashboard de "gorjetas", o deploy está apontando para outro repositório.</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("focus_marketing_data.csv", parse_dates=["inicio", "fim"])

df = load_data()

st.sidebar.header("Filtros")
servicos = st.sidebar.multiselect("Serviço", df["servico"].unique().tolist(), default=df["servico"].unique().tolist())
plataformas = st.sidebar.multiselect("Plataforma", df["plataforma"].unique().tolist(), default=df["plataforma"].unique().tolist())
campanhas = st.sidebar.multiselect("Campanha", df["campanha"].unique().tolist(), default=df["campanha"].unique().tolist())
data_inicio = st.sidebar.date_input("Data inicial", df["inicio"].min())
data_fim = st.sidebar.date_input("Data final", df["fim"].max())

df_filtrado = df[
    (df["servico"].isin(servicos)) &
    (df["plataforma"].isin(plataformas)) &
    (df["campanha"].isin(campanhas)) &
    (df["inicio"] >= pd.to_datetime(data_inicio)) &
    (df["fim"] <= pd.to_datetime(data_fim))
]

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Investimento Total", f"R$ {df_filtrado['investimento'].sum():,.2f}")
c2.metric("Receita Total", f"R$ {df_filtrado['receita'].sum():,.2f}")
c3.metric("ROI Médio", f"{df_filtrado['roi'].mean():.2f}%")
c4.metric("Leads Totais", f"{int(df_filtrado['leads'].sum())}")

c5, c6, c7, c8 = st.columns(4)
c5.metric("Conversões Totais", f"{int(df_filtrado['conversoes'].sum())}")
c6.metric("CTR Médio", f"{df_filtrado['ctr'].mean():.2f}%")
c7.metric("CPL Médio", f"R$ {df_filtrado['cpl'].mean():.2f}")
c8.metric("CPA Médio", f"R$ {df_filtrado['cpa'].mean():.2f}")

st.subheader("Investimento vs Receita")
st.plotly_chart(px.scatter(df_filtrado, x="investimento", y="receita", color="servico",
                           size="roi", hover_data=["campanha"], template="plotly_dark"),
                use_container_width=True)

st.subheader("ROI por Serviço")
roi_serv = df_filtrado.groupby("servico", as_index=False)["roi"].mean()
st.plotly_chart(px.bar(roi_serv, x="servico", y="roi", color="servico", template="plotly_dark"),
                use_container_width=True)

st.subheader("CPL por Plataforma")
st.plotly_chart(px.box(df_filtrado, x="plataforma", y="cpl", color="plataforma", template="plotly_dark"),
                use_container_width=True)

st.subheader("Evolução de Investimento e Receita")
df_time = df_filtrado.groupby("inicio", as_index=False)[["investimento", "receita"]].sum()
st.plotly_chart(px.line(df_time, x="inicio", y=["investimento", "receita"], template="plotly_dark"),
                use_container_width=True)

st.subheader("Conversões por Campanha")
conv = df_filtrado.groupby("campanha", as_index=False)["conversoes"].sum().sort_values("conversoes", ascending=False).head(30)
st.plotly_chart(px.bar(conv, x="campanha", y="conversoes", template="plotly_dark"),
                use_container_width=True)

st.subheader("📋 Dados (5 primeiras linhas)")
st.dataframe(df_filtrado.head())

st.caption("Focus Marketing © 2025 — V2")
