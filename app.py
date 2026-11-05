import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="analise-de-dados | Guerra dos Consoles e Dinâmica Cultural",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    body {
        color: #0F172A;
        background-color: #F8FAFC;
    }
    .header-container {
        padding-bottom: 16px;
        margin-bottom: 24px;
        border-bottom: 1px solid #E2E8F0;
    }
    .repo-badge {
        display: inline-block;
        background-color: #F1F5F9;
        border: 1px solid #CBD5E1;
        color: #334155;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }
    .subtitle {
        color: #475569;
        font-size: 1.05rem;
        margin-top: 0;
        margin-bottom: 0;
    }
    .metric-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0F172A;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #64748B;
        margin-top: 2px;
    }
    .card-discovery {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .card-discovery h3 {
        margin-top: 0;
        margin-bottom: 12px;
        font-size: 1.2rem;
        font-weight: 700;
        color: #0F172A;
    }
    .card-discovery p, .card-discovery li {
        color: #334155;
        font-size: 0.98rem;
        line-height: 1.65;
    }
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 10px;
    }
    .tag-blue { background-color: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; }
    .tag-red { background-color: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; }
    .tag-amber { background-color: #FFFBEB; color: #B45309; border: 1px solid #FDE68A; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_dataset():
    primary_path = Path("data/vgsales_cleaned.csv")
    if primary_path.exists():
        return pd.read_csv(primary_path)
    
    fallback_path = Path("data/vgsales.csv")
    if fallback_path.exists():
        df = pd.read_csv(fallback_path)
    else:
        df = pd.read_csv("vgsales.csv")

    df.columns = [col.strip().replace(" ", "_") for col in df.columns]
    df = df.dropna(subset=['Year']).copy()
    df['Year'] = df['Year'].astype(int)
    df = df[(df['Year'] >= 1980) & (df['Year'] <= 2017)]

    def get_manufacturer(platform):
        nintendo = ['NES', 'SNES', 'N64', 'GC', 'Wii', 'WiiU', 'GB', 'GBA', 'DS', '3DS']
        sony = ['PS', 'PS2', 'PS3', 'PS4', 'PSP', 'PSV']
        microsoft = ['XB', 'X360', 'XOne']
        sega = ['GEN', 'SAT', 'DC', 'GG', 'SCD']
        if platform in nintendo:
            return 'Nintendo'
        elif platform in sony:
            return 'Sony'
        elif platform in microsoft:
            return 'Microsoft'
        elif platform in sega:
            return 'Sega'
        elif platform == 'PC':
            return 'PC'
        else:
            return 'Outros'

    df['Manufacturer'] = df['Platform'].apply(get_manufacturer)
    return df

df_full = load_dataset()

COLORS = {
    'Nintendo': '#DC2626',
    'Sony': '#1D4ED8',
    'Microsoft': '#059669',
    'Sega': '#0284C7',
    'PC': '#475569',
    'Outros': '#D97706'
}

with st.sidebar:
    st.markdown("**Repositório:** [`analise-de-dados`](https://github.com/theotavio/analise-de-dados)")
    st.markdown("**Deploy Online:** [guerradeconsoles.streamlit.app](https://guerradeconsoles.streamlit.app/)")
    st.subheader("Filtros de Análise")
    
    min_year = int(df_full['Year'].min())
    max_year = int(df_full['Year'].max())
    
    selected_years = st.slider(
        "Período de Lançamento (Anos)",
        min_value=min_year,
        max_value=max_year,
        value=(1985, 2016),
        step=1
    )

    all_manufacturers = sorted(list(df_full['Manufacturer'].unique()))
    selected_manufacturers = st.multiselect(
        "Fabricantes de Plataforma",
        options=all_manufacturers,
        default=all_manufacturers
    )

    all_genres = sorted(list(df_full['Genre'].unique()))
    selected_genres = st.multiselect(
        "Gêneros",
        options=all_genres,
        default=all_genres
    )

    title_query = st.text_input("Filtrar por Nome de Jogo", placeholder="Exemplo: Mario, Pokémon, Halo")

df = df_full[
    (df_full['Year'] >= selected_years[0]) &
    (df_full['Year'] <= selected_years[1]) &
    (df_full['Manufacturer'].isin(selected_manufacturers)) &
    (df_full['Genre'].isin(selected_genres))
]

if title_query:
    df = df[df['Name'].str.contains(title_query, case=False, na=False)]

st.markdown("""
<div class="header-container">
    <div class="repo-badge">
        <a href="https://github.com/theotavio/analise-de-dados" target="_blank" style="text-decoration:none; color:inherit;">Repositório: analise-de-dados</a>
        &nbsp;&bull;&nbsp;
        <a href="https://guerradeconsoles.streamlit.app/" target="_blank" style="text-decoration:none; color:#1D4ED8;">guerradeconsoles.streamlit.app</a>
    </div>
    <div class="main-title">A Guerra dos Consoles e o Choque Cultural</div>
    <div class="subtitle">Análise visual de 4 décadas de vendas, padrões de consumo regional e eficiência comercial de publicadoras</div>
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.info("Nenhum registro corresponde aos filtros selecionados. Ajuste os parâmetros na barra lateral para carregar os dados.")
    st.stop()

col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

total_games = len(df)
total_volume = df['Global_Sales'].sum()
leading_platform = df.groupby('Platform')['Global_Sales'].sum().idxmax()
leading_platform_sales = df.groupby('Platform')['Global_Sales'].sum().max()
leading_genre = df.groupby('Genre')['Global_Sales'].sum().idxmax()
leading_genre_sales = df.groupby('Genre')['Global_Sales'].sum().max()
leading_pub = df.groupby('Publisher')['Global_Sales'].sum().idxmax()
leading_pub_sales = df.groupby('Publisher')['Global_Sales'].sum().max()

with col_kpi1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Catálogo Filtrado</div>
        <div class="metric-value">{total_games:,}</div>
        <div class="metric-sub">Títulos analisados</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Vendas Globais</div>
        <div class="metric-value">{total_volume:,.1f}M</div>
        <div class="metric-sub">Cópias registradas</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Plataforma Líder</div>
        <div class="metric-value">{leading_platform}</div>
        <div class="metric-sub">{leading_platform_sales:,.1f}M unidades</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Gênero Campeão</div>
        <div class="metric-value">{leading_genre}</div>
        <div class="metric-sub">{leading_genre_sales:,.1f}M unidades</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi5:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Maior Publicadora</div>
        <div class="metric-value" style="font-size: 1.25rem;">{leading_pub}</div>
        <div class="metric-sub">{leading_pub_sales:,.1f}M unidades</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

tab1, tab2, tab3, tab4 = st.tabs([
    "Painel de Visualizações",
    "Descobertas Principais",
    "Metodologia e Justificativas",
    "Tabela de Dados"
])

with tab1:
    st.markdown("### 1. Corrida das Plataformas no Tempo")
    st.markdown("Animação interativa do avanço de vendas das 10 principais plataformas históricas. Pressione o botão Play para acompanhar a troca de posições ao longo dos anos.")

    top10_plats = df_full.groupby('Platform')['Global_Sales'].sum().nlargest(10).index.tolist()
    years_list = sorted([y for y in df_full['Year'].unique() if y >= selected_years[0] and y <= selected_years[1]])
    
    race_records = []
    for yr in years_list:
        sub_yr = df_full[df_full['Year'] <= yr]
        plat_totals = sub_yr[sub_yr['Platform'].isin(top10_plats)].groupby(['Platform', 'Manufacturer'])['Global_Sales'].sum().reset_index()
        plat_totals['Year'] = yr
        race_records.append(plat_totals)

    if race_records:
        race_df = pd.concat(race_records, ignore_index=True)
        max_val_race = race_df['Global_Sales'].max() * 1.08

        fig_race = px.bar(
            race_df,
            x="Global_Sales",
            y="Platform",
            color="Manufacturer",
            color_discrete_map=COLORS,
            animation_frame="Year",
            range_x=[0, max_val_race],
            orientation="h",
            labels={"Global_Sales": "Vendas Acumuladas (Milhões)", "Platform": "Plataforma", "Manufacturer": "Fabricante"},
            height=530
        )
        fig_race.update_layout(
            template="plotly_white",
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=30, r=30, t=20, b=30)
        )
        st.plotly_chart(fig_race)

    st.markdown("---")

    st.markdown("### 2. Fluxo de Mercado: Fabricantes para Gêneros")
    st.markdown("Diagrama de fluxo que traça as fitas de faturamento global fluindo de cada ecossistema de hardware diretamente para os gêneros de jogos.")

    flow_agg = df.groupby(['Manufacturer', 'Genre'])['Global_Sales'].sum().reset_index()
    flow_agg = flow_agg[flow_agg['Global_Sales'] > 15]

    mfr_nodes = sorted(list(flow_agg['Manufacturer'].unique()))
    genre_nodes = sorted(list(flow_agg['Genre'].unique()))
    all_nodes = mfr_nodes + genre_nodes
    node_map = {name: idx for idx, name in enumerate(all_nodes)}

    sources = [node_map[m] for m in flow_agg['Manufacturer']]
    targets = [node_map[g] for g in flow_agg['Genre']]
    values = flow_agg['Global_Sales'].tolist()

    node_colors = [COLORS.get(n, '#64748B') for n in all_nodes]
    link_colors = [COLORS.get(m, '#94A3B8') for m in flow_agg['Manufacturer']]

    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=18,
            thickness=22,
            line=dict(color="#0F172A", width=0.5),
            label=all_nodes,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=[f"rgba({int(c[1:3], 16)}, {int(c[3:5], 16)}, {int(c[5:7], 16)}, 0.4)" for c in link_colors]
        )
    )])
    fig_sankey.update_layout(
        template="plotly_white",
        height=540,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_sankey)

    st.markdown("---")

    st.markdown("### 3. Hierarquia Radial Concéntrica (Sunburst)")
    st.markdown("Estrutura circular que mapeia os volumes em camadas aninhadas. Clique em um fabricante ou console para abrir a hierarquia e focar nos detalhes.")

    fig_sun = px.sunburst(
        df[df['Global_Sales'] > 0],
        path=['Manufacturer', 'Platform', 'Genre'],
        values='Global_Sales',
        color='Manufacturer',
        color_discrete_map=COLORS,
        height=550
    )
    fig_sun.update_traces(
        textinfo="label+value",
        hovertemplate="<b>%{label}</b><br>Vendas: %{value:.2f}M cópias<extra></extra>"
    )
    fig_sun.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10)
    )
    st.plotly_chart(fig_sun)

    st.markdown("---")

    st.markdown("### 4. Disparidade Cultural Regional (Dumbbell)")
    st.markdown("Comparativo direto para contrastar a preferência de consumo entre América do Norte (azul) e Japão (vermelho) em cada gênero.")

    genre_comp = df.groupby('Genre')[['NA_Sales', 'JP_Sales']].sum().reset_index()
    sum_na = genre_comp['NA_Sales'].sum()
    sum_jp = genre_comp['JP_Sales'].sum()

    if sum_na > 0 and sum_jp > 0:
        genre_comp['NA_Share'] = (genre_comp['NA_Sales'] / sum_na) * 100
        genre_comp['JP_Share'] = (genre_comp['JP_Sales'] / sum_jp) * 100
        genre_comp = genre_comp.sort_values(by='JP_Share', ascending=True)

        fig_dumb = go.Figure()

        for _, r in genre_comp.iterrows():
            fig_dumb.add_trace(go.Scatter(
                x=[r['NA_Share'], r['JP_Share']],
                y=[r['Genre'], r['Genre']],
                mode='lines',
                line=dict(color='#CBD5E1', width=3),
                showlegend=False,
                hoverinfo='none'
            ))

        fig_dumb.add_trace(go.Scatter(
            x=genre_comp['NA_Share'],
            y=genre_comp['Genre'],
            mode='markers+text',
            name='América do Norte (% do Mercado Regional)',
            marker=dict(color='#2563EB', size=13),
            text=[f"{val:.1f}%" for val in genre_comp['NA_Share']],
            textposition='top center',
            textfont=dict(size=9, color='#1E40AF')
        ))

        fig_dumb.add_trace(go.Scatter(
            x=genre_comp['JP_Share'],
            y=genre_comp['Genre'],
            mode='markers+text',
            name='Japão (% do Mercado Regional)',
            marker=dict(color='#DC2626', size=13),
            text=[f"{val:.1f}%" for val in genre_comp['JP_Share']],
            textposition='top center',
            textfont=dict(size=9, color='#991B1B')
        ))

        fig_dumb.update_layout(
            template="plotly_white",
            height=520,
            xaxis_title="Participação Percentual sobre o Total da Região (%)",
            yaxis_title="Gênero",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=30, r=30, t=20, b=30)
        )
        st.plotly_chart(fig_dumb)

    st.markdown("---")

    st.markdown("### 5. Matriz de Concentração de Vendas (Plataforma vs. Gênero)")
    st.markdown("Tabela gráfica com valores explícitos indicando o volume de vendas globais no cruzamento das 10 principais plataformas e os gêneros.")

    top_platforms = df.groupby('Platform')['Global_Sales'].sum().nlargest(10).index
    heat_matrix = df[df['Platform'].isin(top_platforms)].pivot_table(
        index='Platform',
        columns='Genre',
        values='Global_Sales',
        aggfunc='sum',
        fill_value=0
    ).loc[top_platforms]

    fig_heat = px.imshow(
        heat_matrix,
        text_auto=".1f",
        labels=dict(x="Gênero", y="Plataforma", color="Vendas (M)"),
        x=heat_matrix.columns,
        y=heat_matrix.index,
        color_continuous_scale="Blues",
        height=500
    )
    fig_heat.update_layout(
        template="plotly_white",
        margin=dict(l=30, r=20, t=20, b=30)
    )
    st.plotly_chart(fig_heat)

with tab2:
    st.markdown("### Análise e Interpretação dos Resultados")
    st.markdown("Principais conclusões fundamentadas nos cruzamentos de dados realizados:")

    st.markdown("""
    <div class="card-discovery">
        <span class="tag tag-red">Padrão Cultural Regional</span>
        <h3>1. Divergência Estrutural entre o Mercado Japonês e o Norte-Americano</h3>
        <p>A análise comparativa do gráfico Dumbbell (Visualização 4) evidencia um contraste histórico pronunciado entre os dois principais polos consumidores:</p>
        <ul>
            <li>No <b>Japão</b>, o gênero <b>Role-Playing (RPG)</b> concentra <b>27,3%</b> de todas as vendas históricas em mídia física, impulsionado por séries consagradas como Pokémon, Dragon Quest e Final Fantasy. Por outro lado, títulos do gênero <b>Shooter</b> representam apenas <b>3,0%</b> do mercado local.</li>
            <li>Na <b>América do Norte</b>, a relação se inverte expressivamente: os gêneros <b>Action</b> e <b>Shooter</b> somam mais de <b>33%</b> da demanda do continente (destaque para Call of Duty e Halo), enquanto RPGs detêm aproximadamente <b>7,5%</b> de participação.</li>
            <li><b>Implicação de Negócios:</b> Publicadoras ocidentais encontram grande barreira de entrada no Japão ao tentar comercializar jogos de tiro convencionais. De forma análoga, JRPGs tradicionais de ritmo lento dependem de adaptações narrativas profundas para alcançar tração em escala no Ocidente.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-discovery">
        <span class="tag tag-blue">Modelo de Negócio e Eficiência</span>
        <h3>2. O Modelo First-Party da Nintendo contra a Produção Fabril de Third-Parties</h3>
        <p>O fluxo de receitas no diagrama Alluvial (Visualização 2) expõe estratégias comerciais diametralmente opostas:</p>
        <ul>
            <li>Empresas como <b>Electronic Arts (1.339 jogos)</b> e <b>Ubisoft (918 jogos)</b> adotam uma operação em escala industrial, com atualizações anuais de catálogo, alcançando médias moderadas de <b>0,82M e 0,52M de cópias por título</b>.</li>
            <li>A <b>Nintendo</b>, trabalhando com volume bem mais enxuto de títulos (696 jogos), registra uma média expressiva de <b>2,56 milhões de cópias por título</b>, mais que o triplo dos concorrentes de grande porte.</li>
            <li><b>Implicação de Negócios:</b> O controle integrado entre software proprietário e hardware próprio, aliado a marcas consolidadas (Mario, Zelda, Pokémon), gera uma curva de retenção e cauda longa de vendas muito superior à de publicadoras dependentes de licenças de terceiros.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-discovery">
        <span class="tag tag-amber">Dinâmica de Hardware</span>
        <h3>3. A Quebra de Paradigma da Sétima Geração com o Nintendo Wii (2006)</h3>
        <p>A corrida temporal de plataformas (Visualização 1) e o diagrama Sunburst (Visualização 3) demonstram a transição de liderança do mercado:</p>
        <ul>
            <li>Até meados de 2005, o ecossistema <b>PlayStation 2 (Sony)</b> manteve hegemonia isolada, concentrando mais de metade das vendas anuais de software, alavancado por jogos de Ação e Corrida (GTA San Andreas e Gran Turismo).</li>
            <li>Em 2006, o lançamento do <b>Nintendo Wii</b> expandiu a base demográfica de consumidores ao introduzir sensores de movimento intuitivos, levando os gêneros de <b>Esportes</b> e <b>Misc</b> a picos históricos (Wii Sports atingiu mais de 82 milhões de unidades).</li>
            <li>Esse movimento fragmentou o setor, abrindo espaço simultâneo para a consolidação do <b>Xbox 360</b> no segmento competitivo ocidental e criando a primeira concorrência verdadeiramente tripartite na indústria.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Limitações dos Dados")
    st.markdown("""
    * **Vendas Digitais:** A base registra primordialmente vendas físicas de varejo. O crescimento das plataformas digitais (Steam, PSN, Xbox Live, Nintendo eShop) a partir de 2013 não está plenamente capturado nos anos finais da série histórica.
    * **Mercado Mobile e Jogos como Serviço:** Títulos de smartphones e modelos gratuitos baseados em microtransações contínuas (como League of Legends e Fortnite) não estão no escopo do levantamento.
    """)

with tab3:
    st.markdown("### Justificativas Técnicas das Visualizações")
    st.markdown("""
    #### Escolha das Ferramentas
    * **Streamlit:** Permite a interatividade de parâmetros em tempo real, integração de dados e publicação web imediata.
    * **Plotly:** Utilizado para fornecer gráficos vetoriais de alta resolução com interatividade fluida, animações temporais e tooltips detalhados.
    * **Pandas:** Empregado no tratamento vetorial, agrupamentos multidimensionais e criação de atributos agregados.

    #### Justificativa dos Tipos de Visualização
    * **Corrida de Barras Animada (Bar Chart Race):** Apresenta a evolução temporal do mercado de forma dinâmica, permitindo acompanhar ano a ano a dança das plataformas líderes.
    * **Diagrama de Fluxo Alluvial (Sankey):** Representa com clareza o volume de receita que flui de cada fabricante para os diferentes gêneros de jogos.
    * **Hierarquia Radial (Sunburst):** Permite explorar visualmente as proporções de vendas em três níveis interdependentes (Fabricante, Plataforma e Gênero) com navegação por clique.
    * **Gráfico de Disparidade (Dumbbell):** Modelo analítico que evidencia a distância relativa entre duas populações geográficas distintas (América do Norte vs. Japão).
    * **Matriz de Concentração com Rótulos Numéricos:** Facilita a leitura rápida de valores exatos em cruzamentos bidimensionais densos, eliminando dúvidas de interpretação visual.
    """)

with tab4:
    st.markdown("### Consulta e Exportação de Dados")
    st.markdown("Tabela interativa com os registros correspondentes aos filtros ativos:")

    st.dataframe(df)

    csv_output = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Exportar Dados Filtrados em CSV",
        data=csv_output,
        file_name="vgsales_export.csv",
        mime="text/csv"
    )
