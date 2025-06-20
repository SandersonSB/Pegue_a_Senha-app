# app.py
# Aplicativo web criado com Streamlit para visualizar o desempenho de times de futebol

# Importação das bibliotecas necessárias
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

# Configuração inicial da página do Streamlit
st.set_page_config(page_title="Pegue a Senha 🌀", layout="wide")

# Inserção de estilo CSS customizado via Markdown (cores, fontes e alinhamento)
st.markdown("""
    <style>
        body { background-color: #f8f9fa; }
        h1 { font-family: 'Trebuchet MS', sans-serif; }
        .titulo-principal { text-align: center; color: #6c63ff; font-size: 48px; margin-bottom: 10px; }
        .subtitulo { text-align: center; color: #FFD700; font-size: 28px; font-weight: bold; margin-top: -10px; }
        .logo { text-align: center; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# Exibição de título, logotipo e subtítulo na interface
st.markdown("<div class='titulo-principal'>Seja Bem-vindo ao Pegue a Senha 🌀</div>", unsafe_allow_html=True)
logo_url = "https://raw.githubusercontent.com/SandersonSB/Pegue_a_Senha-app/main/Gemini_Generated_Image_3rlegz3rlegz3rle.png"
st.markdown(f"<div class='logo'><img src='{logo_url}' width='180'></div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>FUT ANALYSIS ⚽</div>", unsafe_allow_html=True)

# Exibe spinner de carregamento por 2 segundos simulando processamento
with st.spinner("⏳ Carregando..."):
    time.sleep(2)

# Linha divisória horizontal
st.divider()

# Função para carregar e transformar os dados de temporadas (para a aba 1)
@st.cache_data
def load_data_temporadas():
    url = 'https://raw.githubusercontent.com/SandersonSB/Pega-Senha-Project/main/BRA.csv'
    df = pd.read_csv(url)

    # Geração de códigos únicos para cada time
    codigotimes = 3090
    teams = pd.concat([df['Home'], df['Away']]).unique()
    team_ids = {team: i for i, team in enumerate(teams)}
    df['Home Team ID'] = df['Home'].map(team_ids) + codigotimes
    df['Away Team ID'] = df['Away'].map(team_ids) + codigotimes
    df['Cod Match'] = df['Home Team ID'].astype(str) + "-" + df['Away Team ID'].astype(str)

    # Agrupando resultados para quando o time joga em casa
    newdf1 = df.groupby(['Country', 'League', 'Season', 'Home'])['Res'].value_counts().reset_index(name='count')
    newdf1['Res'] = newdf1['Res'].replace({'A': 'DERROTA/DENTRO DE CASA','D': 'EMPATE/DENTRO DE CASA','H': 'VITORIA/DENTRO DE CASA'})

    # Agrupando resultados para quando o time joga fora
    newdf2 = df.groupby(['Country', 'League', 'Season', 'Away'])['Res'].value_counts().reset_index(name='count')
    newdf2['Res'] = newdf2['Res'].replace({'A': 'VITORIA/FORA DE CASA','D': 'EMPATE/FORA DE CASA','H': 'DERROTA/FORA DE CASA'})

    # Concatenando os dois dataframes em um único
    manlydf = pd.concat([newdf1, newdf2], ignore_index=True)
    manlydf['Time_Referente'] = manlydf['Home'].combine_first(manlydf['Away'])
    manlydf['Season'] = manlydf['Season'].astype(int)
    return manlydf

# Função para carregar dados detalhados de partidas (para análise de adversários semelhantes)

@st.cache_data
def load_data_semelhantes():
    url = 'https://raw.githubusercontent.com/SandersonSB/Pega-Senha-Project/main/BRA.csv'
    df = pd.read_csv(url)

    # Mesma lógica de criação de códigos dos times e partidas
    codigotimes = 3090
    teams = pd.concat([df['Home'], df['Away']]).unique()
    team_ids = {team: i for i, team in enumerate(teams)}
    df['Home Team ID'] = df['Home'].map(team_ids) + codigotimes
    df['Away Team ID'] = df['Away'].map(team_ids) + codigotimes
    df['Cod Match'] = df['Home Team ID'].astype(str) + "-" + df['Away Team ID'].astype(str)

    # Agrupamento detalhado incluindo gols, datas e identificadores
    newdf1 = df.groupby(['Country', 'League', 'Season', 'Home', 'Away','HG','AG','Date', 'Cod Match'])['Res'].value_counts().reset_index(name='count')
    newdf1['Res'] = newdf1['Res'].replace({'A': 'DERROTA/DENTRO DE CASA','D': 'EMPATE/DENTRO DE CASA','H': 'VITORIA/DENTRO DE CASA'})
    newdf1['Time_Referente'] = newdf1['Home']

    newdf2 = df.groupby(['Country', 'League', 'Season', 'Away', 'Home','HG','AG','Date', 'Cod Match'])['Res'].value_counts().reset_index(name='count')
    newdf2['Res'] = newdf2['Res'].replace({'A': 'VITORIA/FORA DE CASA','D': 'EMPATE/FORA DE CASA','H': 'DERROTA/FORA DE CASA'})
    newdf2['Time_Referente'] = newdf2['Away']

    manlydf = pd.concat([newdf1, newdf2], ignore_index=True)
    manlydf['Season'] = manlydf['Season'].astype(int)
    return manlydf

# Inicialização de variáveis globais que serão usadas em várias abas
ultimos_7_casa = None
ultimos_7_fora = None
timedecasa = None
timedefora = None

# Criação das abas principais do app
abas = st.tabs(["📘 Introdução", "📊 Histórico de temporadas", "🔢 Probabilidade", "🤔 Curiosidades"])

# Aba 0 - Introdução
with abas[0]:
    st.header("Introdução")
    st.write("Introdução! EM DESENVOLVIMENTO 🛠️🔧.")

# Aba 1 - Histórico de temporadas
with abas[1]:
    st.header("Análise de Temporada")
    st.title("📊 Análise de Resultados de Times de Futebol")

    manlydf = load_data_temporadas()  # Carrega dados agregados por temporada

    # Cria lista de times e categorias disponíveis para seleção pelo usuário
    times_disponiveis = sorted(manlydf['Time_Referente'].dropna().unique())
    categorias_disponiveis = sorted(manlydf['Res'].dropna().unique())

    # Multiselect para o usuário escolher quais times e categorias quer visualizar
    times_selecionados = st.multiselect("Selecione os times para análise:", times_disponiveis)
    categorias_selecionadas = st.multiselect("Selecione as categorias para análise:", categorias_disponiveis)

    # Se o usuário selecionar times, filtra e plota o gráfico de linha
    if times_selecionados:
        df_filtrado = manlydf[manlydf['Time_Referente'].isin(times_selecionados)]
        if categorias_selecionadas:
            df_filtrado = df_filtrado[df_filtrado['Res'].isin(categorias_selecionadas)]

        df_grouped = df_filtrado.groupby(['Season', 'Res'], as_index=False)['count'].sum()
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_grouped, x='Season', y='count', hue='Res', marker='o')
        plt.xticks(sorted(manlydf['Season'].unique()))
        plt.title(f'Contagem de Resultados por Temporada')
        plt.xlabel('Temporada')
        plt.ylabel('Contagem de Resultados')
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.info("👈 Por favor, selecione pelo menos um time.")
    st.title("📊 Analisar os um 7 jogos de cada time")
    # Parte que coleta os últimos 7 jogos dos times para a análise de probabilidade
    manlydf1 = load_data_semelhantes()
    lista_times = ["Selecione um time..."] + sorted(manlydf1['Time_Referente'].dropna().unique())
    timedecasa = st.selectbox("Selecione o time da **casa**:", lista_times)
    timedefora = st.selectbox("Selecione o time **visitante**:", lista_times)

    if timedecasa and timedefora and timedecasa != "Selecione um time..." and timedefora != "Selecione um time...":
        # Filtra os últimos 7 jogos de cada time
        jogos_casa = manlydf1[manlydf1['Time_Referente'] == timedecasa].copy()
        jogos_fora = manlydf1[manlydf1['Time_Referente'] == timedefora].copy()
        jogos_casa['Date'] = pd.to_datetime(jogos_casa['Date'], dayfirst=True)
        jogos_fora['Date'] = pd.to_datetime(jogos_fora['Date'], dayfirst=True)

        ultimos_7_casa = jogos_casa.sort_values('Date', ascending=False).drop_duplicates(subset='Cod Match').head(7)
        ultimos_7_fora = jogos_fora.sort_values('Date', ascending=False).drop_duplicates(subset='Cod Match').head(7)

        # Exibe as tabelas com os últimos 7 jogos
        st.subheader(f"📅 Últimos 7 jogos do time **{timedecasa}**:")
        st.dataframe(ultimos_7_casa[['Date', 'Home', 'Away','HG','AG','Res','Time_Referente', 'Cod Match']])
        st.subheader(f"📅 Últimos 7 jogos do time **{timedefora}**:")
        st.dataframe(ultimos_7_fora[['Date', 'Home', 'Away','HG','AG','Res','Time_Referente', 'Cod Match']])

# Aba 2 - Análise de probabilidade com adversários semelhantes
with abas[2]:
    st.header("🔢 Probabilidade com base em jogos semelhantes")

    if ultimos_7_casa is not None and ultimos_7_fora is not None:
        # Cria coluna de adversário (oponente) para comparar os dois times
        df_casa = ultimos_7_casa.copy()
        df_fora = ultimos_7_fora.copy()

        df_casa['Adversario'] = df_casa.apply(lambda row: row['Away'] if row['Home'] == timedecasa else row['Home'], axis=1)
        df_fora['Adversario'] = df_fora.apply(lambda row: row['Away'] if row['Home'] == timedefora else row['Home'], axis=1)

        adversarios_comuns = set(df_casa['Adversario']).intersection(set(df_fora['Adversario']))

        if adversarios_comuns:
            st.success("✅ Foram encontrados adversários em comum nos últimos 7 jogos.")
            comparacoes = []
            for adversario in adversarios_comuns:
                jogo_time_casa = df_casa[df_casa['Adversario'] == adversario].iloc[0]
                jogo_time_fora = df_fora[df_fora['Adversario'] == adversario].iloc[0]

                # Monta tabela comparativa entre o desempenho dos dois times contra o mesmo adversário
                comparacoes.append({
                    'Adversário': adversario,
                    'Data Jogo Time Casa': jogo_time_casa['Date'].date(),
                    'Local Time Casa': 'Casa' if jogo_time_casa['Home'] == timedecasa else 'Fora',
                    'Placar Time Casa': f"{jogo_time_casa['HG']} x {jogo_time_casa['AG']}",
                    'Resultado Time Casa': jogo_time_casa['Res'],
                    'Data Jogo Time Fora': jogo_time_fora['Date'].date(),
                    'Local Time Fora': 'Casa' if jogo_time_fora['Home'] == timedefora else 'Fora',
                    'Placar Time Fora': f"{jogo_time_fora['HG']} x {jogo_time_fora['AG']}",
                    'Resultado Time Fora': jogo_time_fora['Res'],
                })

            df_comparacoes = pd.DataFrame(comparacoes)
            st.dataframe(df_comparacoes)
        else:
            st.warning("⚠️ Nenhum adversário em comum foi encontrado nos últimos 7 jogos.")
    else:
        st.info("🔎 Primeiro selecione os times na aba anterior para realizar a comparação.")

# Aba 3 - Área para curiosidades (em desenvolvimento)
with abas[3]:
    st.header("Curiosidades")
    st.write("Curiosidades - EM DESENVOLVIMENTO! 🛠️🔧.")
