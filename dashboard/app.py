import streamlit as st
import pandas as pd
import warnings
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

warnings.filterwarnings(
    "ignore", "pandas only supports SQLAlchemy connectable")

DATA_DIR = Path(__file__).parent / "data"

# ==========================================
# 1. Page Config
# ==========================================
st.set_page_config(
    page_title="DataWarehouse E-commerce e Analytics Engineer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. CSS — Dark Slate Glassmorphism
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');

.stApp {
    background: linear-gradient(135deg, #080D1A 0%, #0F1729 50%, #080D1A 100%);
    background-attachment: fixed;
    font-family: 'Inter', sans-serif;
}
.stApp > header { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(8, 13, 26, 0.9) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-right: 1px solid rgba(139, 92, 246, 0.15);
}

/* Headings */
h1 {
    color: #F1F5F9 !important;
    font-weight: 900 !important;
    letter-spacing: -1.5px;
    text-shadow: 0 0 30px rgba(139, 92, 246, 0.4);
}
h2, h3 { color: #E2E8F0 !important; font-weight: 700 !important; }
p { color: #64748B !important; }

/* KPI Cards */
.kpi-card {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 22px 24px;
    border-left: 3px solid var(--ac, #8B5CF6);
    transition: all 0.3s ease;
    margin-bottom: 4px;
}
.kpi-card:hover {
    background: rgba(255, 255, 255, 0.07);
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
}
.kpi-label {
    color: #64748B;
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 8px;
}
.kpi-value {
    color: #F1F5F9;
    font-size: 1.85rem;
    font-weight: 900;
    letter-spacing: -1px;
    line-height: 1;
    text-shadow: 0 0 20px rgba(255, 255, 255, 0.08);
}
.kpi-sub {
    color: #475569;
    font-size: 0.73rem;
    margin-top: 8px;
    font-weight: 500;
}

/* Section divider */
.sec {
    color: #334155;
    font-size: 0.63rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    padding: 20px 0 10px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 16px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. Database
# ==========================================


@st.cache_data
def load(table: str) -> pd.DataFrame:
    try:
        return pd.read_csv(DATA_DIR / f"{table}.csv")
    except Exception as e:
        st.error(f"Erro ao carregar {table}: {e}")
        return pd.DataFrame()

# ==========================================
# 4. Helpers
# ==========================================


def brl(v):
    if pd.isna(v):
        return "R$ 0,00"
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def num(v):
    if pd.isna(v):
        return "0"
    return f"{int(v):,}".replace(",", ".")


def kpi(label, value, sub="", ac="#8B5CF6"):
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return (
        f'<div class="kpi-card" style="--ac:{ac}">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'{sub_html}</div>'
    )


def sec(label):
    st.markdown(f'<div class="sec">{label}</div>', unsafe_allow_html=True)


# Plotly dark template
DARK = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94A3B8", family="Inter, sans-serif", size=12),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(color="#64748B"),
        zerolinecolor="rgba(255,255,255,0.05)",
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(color="#64748B"),
        zerolinecolor="rgba(255,255,255,0.05)",
    ),
    margin=dict(l=10, r=16, t=36, b=10),
    legend=dict(
        bgcolor="rgba(15,23,42,0.6)",
        bordercolor="rgba(255,255,255,0.08)",
        borderwidth=1,
        font=dict(color="#94A3B8"),
    ),
    title_font=dict(color="#E2E8F0", size=13),
    hoverlabel=dict(
        bgcolor="rgba(15,23,42,0.9)",
        bordercolor="rgba(139,92,246,0.4)",
        font=dict(color="#F1F5F9"),
    ),
    colorway=["#8B5CF6", "#06B6D4", "#10B981",
              "#F59E0B", "#EF4444", "#EC4899", "#FB923C"],
)
COLORS = ["#8B5CF6", "#06B6D4", "#10B981",
          "#F59E0B", "#EF4444", "#EC4899", "#FB923C"]


def chart(fig, h=340):
    fig.update_layout(**DARK, height=h)
    return fig

# ==========================================
# 5. Página — Vendas
# ==========================================


def page_vendas():
    st.title("📊 Vendas & Receita")
    st.markdown("Métricas comerciais consolidadas no Data Warehouse.")

    df = load("gold_kpis_vendas")
    if not df.empty and "data_venda_date" in df.columns:
        df = df.sort_values("data_venda_date")
    if df.empty:
        st.warning("Sem dados em raw.gold_kpis_vendas")
        return

    # KPIs
    receita = df["receita_total"].sum()
    pedidos = df["total_pedidos"].sum()
    ticket = receita / pedidos if pedidos > 0 else 0
    clientes = df["clientes_unicos"].sum()

    sec("Resumo Geral")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi("Receita Total",    brl(receita),
                ac="#8B5CF6"), unsafe_allow_html=True)
    c2.markdown(kpi("Total de Pedidos", num(pedidos),
                ac="#06B6D4"), unsafe_allow_html=True)
    c3.markdown(kpi("Ticket Médio",     brl(ticket),
                ac="#10B981"), unsafe_allow_html=True)
    c4.markdown(kpi("Clientes Únicos",  num(clientes),
                ac="#F59E0B"), unsafe_allow_html=True)

    # Receita diária
    sec("Evolução Temporal")
    daily = df.groupby("data_venda_date")["receita_total"].sum().reset_index()
    fig = go.Figure(go.Scatter(
        x=daily["data_venda_date"], y=daily["receita_total"],
        mode="lines",
        line=dict(color="#8B5CF6", width=2.5),
        fill="tozeroy", fillcolor="rgba(139,92,246,0.08)",
        hovertemplate="<b>%{x}</b><br>Receita: R$ %{y:,.2f}<extra></extra>",
    ))
    fig.update_layout(title="Receita Diária",
                      yaxis_tickformat=",.0f", hovermode="x unified")
    st.plotly_chart(chart(fig, 300), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        canal = (
            df.groupby("canal_venda")["receita_total"]
            .sum().reset_index()
            .sort_values("receita_total")
        )
        fig2 = go.Figure(go.Bar(
            x=canal["receita_total"], y=canal["canal_venda"], orientation="h",
            marker_color=COLORS[:len(canal)],
            hovertemplate="%{y}: R$ %{x:,.2f}<extra></extra>",
        ))
        fig2.update_layout(title="Receita por Canal de Venda",
                           xaxis_tickformat=",.0f", showlegend=False)
        st.plotly_chart(chart(fig2, 320), use_container_width=True)

    with col2:
        meses_pt = ["Jan", "Fev", "Mar", "Abr", "Mai",
                    "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        monthly = (
            df.groupby(["ano_venda", "mes_venda"])["receita_total"]
            .sum().reset_index()
            .sort_values(["ano_venda", "mes_venda"])
        )
        monthly["periodo"] = monthly.apply(
            lambda r: f"{meses_pt[int(r.mes_venda)-1]}/{str(int(r.ano_venda))[-2:]}", axis=1
        )
        fig3 = go.Figure(go.Bar(
            x=monthly["periodo"], y=monthly["receita_total"],
            marker_color="#06B6D4",
            marker_line_color="rgba(6,182,212,0.3)", marker_line_width=1,
            hovertemplate="%{x}: R$ %{y:,.2f}<extra></extra>",
        ))
        fig3.update_layout(title="Receita por Mês",
                           yaxis_tickformat=",.0f", showlegend=False)
        st.plotly_chart(chart(fig3, 320), use_container_width=True)

    # Heatmap
    sec("Padrão de Compras")
    DIAS = {0: "Dom", 1: "Seg", 2: "Ter",
            3: "Qua", 4: "Qui", 5: "Sex", 6: "Sáb"}
    ORDER = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    heat = df.groupby(["dia_semana", "hora_venda"])[
        "total_pedidos"].sum().reset_index()
    heat["dia_nome"] = heat["dia_semana"].map(DIAS)
    pivot = heat.pivot_table(
        index="dia_nome", columns="hora_venda", values="total_pedidos", fill_value=0)
    pivot = pivot.reindex([d for d in ORDER if d in pivot.index])
    fig4 = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[f"{int(h):02d}h" for h in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=[[0, "#080D1A"], [0.4, "#4C1D95"], [1, "#06B6D4"]],
        showscale=True,
        colorbar=dict(tickfont=dict(color="#64748B"), bgcolor="rgba(0,0,0,0)"),
        hovertemplate="<b>%{y} %{x}</b><br>Pedidos: %{z}<extra></extra>",
    ))
    fig4.update_layout(title="Pedidos por Hora × Dia da Semana")
    st.plotly_chart(chart(fig4, 280), use_container_width=True)


# ==========================================
# 6. Página — Clientes
# ==========================================
def page_clientes():
    st.title("👥 Clientes")
    st.markdown("Segmentação, ranking e perfil da base de clientes.")

    df = load("gold_customer_360")
    if not df.empty and "ranking_receita" in df.columns:
        df = df.sort_values("ranking_receita")
    if df.empty:
        st.warning("Sem dados em raw.gold_customer_360")
        return

    total = len(df)
    n_vip = (df["segmento_cliente"] == "VIP").sum()
    rec_vip = df.loc[df["segmento_cliente"] == "VIP", "receita_total"].sum()
    ticket = df["ticket_medio"].mean()

    sec("Resumo")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi("Total Clientes",  num(total),
                ac="#8B5CF6"), unsafe_allow_html=True)
    c2.markdown(kpi("Clientes VIP",    num(
        n_vip), f"{n_vip/total*100:.1f}% da base", ac="#06B6D4"), unsafe_allow_html=True)
    c3.markdown(kpi("Receita VIP",     brl(rec_vip),
                ac="#10B981"), unsafe_allow_html=True)
    c4.markdown(kpi("Ticket Médio",    brl(ticket),
                ac="#F59E0B"), unsafe_allow_html=True)

    sec("Segmentação")
    SEG_COLORS = {"VIP": "#8B5CF6",
                  "Top Tier": "#06B6D4", "Regular": "#334155"}
    col1, col2 = st.columns(2)
    with col1:
        seg = df["segmento_cliente"].value_counts().reset_index()
        seg.columns = ["segmento", "count"]
        fig1 = go.Figure(go.Pie(
            labels=seg["segmento"], values=seg["count"], hole=0.55,
            marker_colors=[SEG_COLORS.get(s, "#8B5CF6")
                           for s in seg["segmento"]],
            textinfo="label+percent",
            textfont=dict(color="#E2E8F0", size=12),
            hovertemplate="<b>%{label}</b><br>%{value} clientes (%{percent})<extra></extra>",
        ))
        fig1.update_layout(title="Distribuição por Segmento", showlegend=False)
        st.plotly_chart(chart(fig1, 320), use_container_width=True)

    with col2:
        seg_rec = (
            df.groupby("segmento_cliente")["receita_total"]
            .sum().reset_index()
            .sort_values("receita_total", ascending=True)
        )
        fig2 = go.Figure(go.Bar(
            x=seg_rec["receita_total"], y=seg_rec["segmento_cliente"], orientation="h",
            marker_color=[SEG_COLORS.get(s, "#8B5CF6")
                          for s in seg_rec["segmento_cliente"]],
            hovertemplate="%{y}: R$ %{x:,.2f}<extra></extra>",
        ))
        fig2.update_layout(title="Receita por Segmento",
                           xaxis_tickformat=",.0f", showlegend=False)
        st.plotly_chart(chart(fig2, 320), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        top10 = df.nsmallest(
            10, "ranking_receita").sort_values("receita_total")
        fig3 = go.Figure(go.Bar(
            x=top10["receita_total"], y=top10["nome_cliente"], orientation="h",
            marker_color="#8B5CF6",
            hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f}<extra></extra>",
        ))
        fig3.update_layout(title="Top 10 Clientes por Receita",
                           xaxis_tickformat=",.0f", showlegend=False)
        st.plotly_chart(chart(fig3, 360), use_container_width=True)

    with col4:
        estados = (
            df.groupby("estado").size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
            .head(12)
        )
        fig4 = go.Figure(go.Bar(
            x=estados["estado"], y=estados["count"],
            marker_color="#06B6D4",
            hovertemplate="%{x}: %{y} clientes<extra></extra>",
        ))
        fig4.update_layout(
            title="Clientes por Estado (Top 12)", showlegend=False)
        st.plotly_chart(chart(fig4, 360), use_container_width=True)

    sec("Tabela Detalhada")
    filtro = st.selectbox("Filtrar por segmento", [
                          "Todos"] + df["segmento_cliente"].unique().tolist())
    view = df if filtro == "Todos" else df[df["segmento_cliente"] == filtro]
    st.dataframe(
        view[["ranking_receita", "nome_cliente", "estado", "segmento_cliente",
              "receita_total", "total_compras", "ticket_medio"]]
        .rename(columns={
            "ranking_receita": "Rank", "nome_cliente": "Cliente",
            "estado": "Estado", "segmento_cliente": "Segmento",
            "receita_total": "Receita", "total_compras": "Compras",
            "ticket_medio": "Tkt Médio",
        }),
        use_container_width=True, hide_index=True,
    )


# ==========================================
# 7. Página — Produtos
# ==========================================
def page_produtos():
    st.title("📦 Produtos")
    st.markdown("Performance, categorias e tendências de venda.")

    df = load("gold_kpis_produtos")
    if not df.empty and "ranking_receita" in df.columns:
        df = df.sort_values("ranking_receita")
    if df.empty:
        st.warning("Sem dados em raw.gold_kpis_produtos")
        return

    total_prod = len(df)
    n_queda = (df["status_vendas"] == "Queda de Vendas").sum()
    top1 = df[df["ranking_receita"] == 1]
    rec_top = top1["receita_total"].values[0] if len(top1) > 0 else 0
    nome_top = top1["nome_produto"].values[0] if len(top1) > 0 else ""

    sec("Resumo")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi("Produtos Ativos",     num(total_prod),
                ac="#8B5CF6"), unsafe_allow_html=True)
    c2.markdown(kpi("Em Queda de Vendas",  num(
        n_queda), f"{n_queda/total_prod*100:.1f}% do catálogo", ac="#EF4444"), unsafe_allow_html=True)
    c3.markdown(kpi("Receita — #1",        brl(rec_top), nome_top,
                ac="#10B981"), unsafe_allow_html=True)
    c4.markdown(kpi("Receita Total",       brl(
        df["receita_total"].sum()),               ac="#F59E0B"), unsafe_allow_html=True)

    # Top 15
    sec("Ranking de Produtos")
    top15 = df.nsmallest(15, "ranking_receita").sort_values("receita_total")
    colors_bar = ["#EF4444" if s ==
                  "Queda de Vendas" else "#8B5CF6" for s in top15["status_vendas"]]
    fig1 = go.Figure(go.Bar(
        x=top15["receita_total"], y=top15["nome_produto"], orientation="h",
        marker_color=colors_bar,
        hovertemplate="<b>%{y}</b><br>Receita: R$ %{x:,.2f}<extra></extra>",
    ))
    fig1.update_layout(
        title="Top 15 Produtos por Receita  (🔴 = em queda de vendas)",
        xaxis_tickformat=",.0f", showlegend=False,
    )
    st.plotly_chart(chart(fig1, 460), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        cat = (
            df.groupby("categoria")["receita_total"]
            .sum().reset_index()
            .sort_values("receita_total", ascending=False)
        )
        fig2 = px.treemap(
            cat, path=["categoria"], values="receita_total",
            color="receita_total",
            color_continuous_scale=[[0, "#1E1B4B"],
                                    [0.5, "#7C3AED"], [1, "#06B6D4"]],
            title="Receita por Categoria",
        )
        fig2.update_traces(textfont=dict(color="#F1F5F9"))
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(**DARK, height=340)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        status = df.groupby(["categoria", "status_vendas"]
                            ).size().reset_index(name="count")
        fig3 = px.bar(
            status, x="categoria", y="count", color="status_vendas",
            title="Status de Vendas por Categoria",
            color_discrete_map={
                "Queda de Vendas":       "#EF4444",
                "Estável ou Crescendo":  "#10B981",
            },
            barmode="stack",
        )
        st.plotly_chart(chart(fig3, 340), use_container_width=True)

    # Tabela queda
    sec("⚠️ Produtos em Queda de Vendas")
    queda = df[df["status_vendas"] == "Queda de Vendas"][[
        "ranking_receita", "nome_produto", "categoria",
        "total_vendido", "vendas_ultimos_3m", "vendas_3m_anteriores", "receita_total",
    ]].rename(columns={
        "ranking_receita": "Rank", "nome_produto": "Produto", "categoria": "Categoria",
        "total_vendido": "Total Vendido", "vendas_ultimos_3m": "Últ. 3m",
        "vendas_3m_anteriores": "3m Anterior", "receita_total": "Receita",
    })
    if queda.empty:
        st.success("Nenhum produto em queda no período.")
    else:
        st.dataframe(queda, use_container_width=True, hide_index=True)


# ==========================================
# 8. Página — Pricing
# ==========================================
def page_pricing():
    st.title("💲 Pricing")
    st.markdown("Inteligência de preços vs concorrência.")

    df = load("gold_kpis_pricing")
    if df.empty:
        st.warning("Sem dados em raw.gold_kpis_pricing")
        return

    CLAS_COLORS = {
        "Mais caro que todos":    "#EF4444",
        "Acima da média":         "#F59E0B",
        "Abaixo da média":        "#10B981",
        "Mais barato que todos":  "#06B6D4",
    }

    total = len(df)
    n_caro = (df["classificacao_preco"] == "Mais caro que todos").sum()
    n_barato = (df["classificacao_preco"] == "Mais barato que todos").sum()
    dif_med = df["diferenca_pct_vs_media"].mean()

    sec("Resumo")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi("Produtos Analisados",  num(total),
                ac="#8B5CF6"), unsafe_allow_html=True)
    c2.markdown(kpi("Mais Caros que Todos", num(n_caro),
                "⚠️ risco de perda",  ac="#EF4444"), unsafe_allow_html=True)
    c3.markdown(kpi("Mais Baratos que Todos", num(n_barato),
                ac="#10B981"), unsafe_allow_html=True)
    c4.markdown(kpi("Dif. Média vs Mercado",
                f"{dif_med:+.1f}%", "positivo = mais caro", ac="#F59E0B"), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        clas = df["classificacao_preco"].value_counts().reset_index()
        clas.columns = ["classificacao", "count"]
        fig1 = go.Figure(go.Pie(
            labels=clas["classificacao"], values=clas["count"], hole=0.55,
            marker_colors=[CLAS_COLORS.get(c, "#8B5CF6")
                           for c in clas["classificacao"]],
            textinfo="label+percent",
            textfont=dict(color="#E2E8F0", size=11),
            hovertemplate="<b>%{label}</b><br>%{value} produtos (%{percent})<extra></extra>",
        ))
        fig1.update_layout(
            title="Posicionamento vs Concorrência", showlegend=False)
        st.plotly_chart(chart(fig1, 320), use_container_width=True)

    with col2:
        cat_dif = (
            df.groupby("categoria")["diferenca_pct_vs_media"]
            .mean().reset_index()
            .sort_values("diferenca_pct_vs_media")
        )
        cat_dif["color"] = cat_dif["diferenca_pct_vs_media"].apply(
            lambda x: "#10B981" if x <= 0 else "#EF4444"
        )
        fig2 = go.Figure(go.Bar(
            x=cat_dif["diferenca_pct_vs_media"], y=cat_dif["categoria"], orientation="h",
            marker_color=cat_dif["color"].tolist(),
            hovertemplate="<b>%{y}</b><br>%{x:+.1f}% vs mercado<extra></extra>",
        ))
        fig2.add_vline(x=0, line_dash="dash",
                       line_color="rgba(255,255,255,0.15)")
        fig2.update_layout(
            title="Diferença % vs Média por Categoria", showlegend=False)
        st.plotly_chart(chart(fig2, 320), use_container_width=True)

    # Scatter
    sec("Dispersão de Preços")
    fig3 = go.Figure()
    for clas, color in CLAS_COLORS.items():
        sub = df[df["classificacao_preco"] == clas]
        if sub.empty:
            continue
        fig3.add_trace(go.Scatter(
            x=sub["preco_medio_concorrentes"], y=sub["nosso_preco"],
            mode="markers", name=clas,
            marker=dict(color=color, size=8, opacity=0.75,
                        line=dict(color="rgba(0,0,0,0.3)", width=1)),
            text=sub["nome_produto"],
            hovertemplate="<b>%{text}</b><br>Nosso: R$ %{y:,.2f}<br>Concorr. médio: R$ %{x:,.2f}<extra></extra>",
        ))
    max_val = max(df["nosso_preco"].max(),
                  df["preco_medio_concorrentes"].max()) * 1.05
    fig3.add_trace(go.Scatter(
        x=[0, max_val], y=[0, max_val], mode="lines",
        line=dict(color="rgba(255,255,255,0.12)", dash="dash"),
        name="Paridade", hoverinfo="skip",
    ))
    fig3.update_layout(
        title="Nosso Preço vs Média dos Concorrentes  (acima da linha = mais caro)",
        xaxis_title="Preço Médio Concorrentes (R$)",
        yaxis_title="Nosso Preço (R$)",
    )
    st.plotly_chart(chart(fig3, 430), use_container_width=True)

    # Alertas
    sec("⚠️ Alerta — Mais Caros que Todos os Concorrentes")
    alertas = df[df["classificacao_preco"] == "Mais caro que todos"][[
        "nome_produto", "categoria", "nosso_preco",
        "preco_medio_concorrentes", "preco_max_concorrentes",
        "diferenca_pct_vs_media", "classificacao_preco",
    ]].rename(columns={
        "nome_produto": "Produto", "categoria": "Categoria",
        "nosso_preco": "Nosso Preço", "preco_medio_concorrentes": "Média Concorr.",
        "preco_max_concorrentes": "Máx Concorr.",
        "diferenca_pct_vs_media": "Dif. % Média", "classificacao_preco": "Status",
    })
    if alertas.empty:
        st.success("Nenhum produto mais caro que todos os concorrentes!")
    else:
        st.dataframe(alertas, use_container_width=True, hide_index=True)


# ==========================================
# 9. Sidebar + Navegação
# ==========================================
st.sidebar.markdown("""
<div style="text-align:center; padding:16px 0 28px 0">
    <div style="font-size:2.2rem; margin-bottom:6px">⚡</div>
    <div style="color:#F1F5F9; font-size:1.05rem; font-weight:900; letter-spacing:-0.5px">E-Commerce Data Warehouse</div>
    <div style="color:#334155; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.14em; margin-top:4px">Data Analytics</div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "", ["📊 Vendas", "👥 Clientes", "📦 Produtos", "💲 Pricing"])

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size:0.72rem; color:#334155; line-height:1.8">
    🐳 PostgreSQL · Docker local<br>
    ⚙️ dbt Medallion Architecture<br>
    🏗️ Bronze → Silver → Gold
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="display:flex; justify-content:center; gap:8px; margin-top:12px">
    <a href="https://github.com/edsoo" target="_blank">
        <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"
             style="border-radius:6px; height:26px"/>
    </a>
    <a href="https://linkedin.com/in/edsoo" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"
             style="border-radius:6px; height:26px"/>
    </a>
</div>
<div style="text-align:center; margin-top:10px; color:#1F2937; font-size:0.68rem">
    by edsoo · Data Warehouse E-commerce
</div>
""", unsafe_allow_html=True)

# ==========================================
# 10. Router
# ==========================================
if page == "📊 Vendas":
    page_vendas()
elif page == "👥 Clientes":
    page_clientes()
elif page == "📦 Produtos":
    page_produtos()
elif page == "💲 Pricing":
    page_pricing()
