# app.py
# Aplicativo web para visualizar o desempenho de times de futebol

# Importa as bibliotecas necessárias
import streamlit as st  # cria a interface do app
import pandas as pd  # manipula os dados
import seaborn as sns  # cria gráficos mais bonitos
import matplotlib.pyplot as plt  # biblioteca de gráficos

# Configura o visual da página do app
st.set_page_config(page_title="Análise de Resultados por Time", layout="wide", initial_sidebar_state="expanded")

# Título principal do aplicativo
st.title("📊 Análise de Resultados de Times de Futebol")

# Função para carregar e preparar os dados, usando cache para não carregar toda hora
@st.cache_data
def load_data():
    # Pega os dados de jogos de futebol de um link na internet
    url = 'https://raw.githubusercontent.com/SandersonSB/Pega-Senha-Project/main/BRA.csv'
    df = pd.read_csv(url)

    # Cria códigos únicos para cada time, para facilitar o trabalho com eles
    codigotimes = 3090
    teams = pd.concat([df['Home'], df['Away']]).unique()  # junta todos os times da casa e visitantes
    team_ids = {team: i for i, team in enumerate(teams)}  # cria um dicionário com ID para cada time
    df['Home Team ID'] = df['Home'].map(team_ids) + codigotimes  # cria o ID do time da casa
    df['Away Team ID'] = df['Away'].map(team_ids) + codigotimes  # cria o ID do time visitante
    df['Cod Match'] = df['Home Team ID'].astype(str) + "-" + df['Away Team ID'].astype(str)  # cria um código para o jogo

    # Conta quantas vitórias, empates e derrotas o time da casa teve por temporada
    newdf1 = df.groupby(['Country','League','Season','Home'])['Res'].value_counts().reset_index()
    # Traduz as siglas para palavras mais claras
    newdf1['Res'] = newdf1['Res'].replace({'A': 'DERROTA/DENTRO DE CASA', 'D': 'EMPATE/DENTRO DE CASA', 'H': 'VITORIA/DENTRO DE CASA'})

    # Faz o mesmo para o time visitante
    newdf2 = df.groupby(['Country','League','Season','Away'])['Res'].value_counts().reset_index()
    newdf2['Res'] = newdf2['Res'].replace({'A': 'VITORIA/FORA DE CASA', 'D': 'EMPATE/FORA DE CASA', 'H': 'DERROTA/FORA DE CASA'})

    # Junta os dois dataframes (casa e fora) em um só
    manlydf = pd.concat([newdf1, newdf2], ignore_index=True)

    # Cria uma nova coluna com o nome do time (de casa ou fora, dependendo de onde jogou)
    manlydf['Time_Referente'] = manlydf['Home'].combine_first(manlydf['Away'])

    # Garante que a temporada seja número (e não texto)
    manlydf['Season'] = manlydf['Season'].astype(int)

    return manlydf  # devolve o conjunto de dados preparado

# Carrega os dados
manlydf = load_data()

# Cria a lista de times únicos disponíveis para escolher
times_disponiveis = sorted(manlydf['Time_Referente'].dropna().unique())

# Caixa de seleção para o usuário escolher um ou mais times
times_selecionados = st.multiselect("Selecione os times para análise:", times_disponiveis)

# Se o usuário escolheu pelo menos um time:
if times_selecionados:
    # Filtra os dados para mostrar só os times escolhidos
    df_filtrado = manlydf[manlydf['Time_Referente'].isin(times_selecionados)]

    # Agrupa os dados por temporada e tipo de resultado, somando a quantidade
    df_grouped = df_filtrado.groupby(['Season', 'Res'], as_index=False)['count'].sum()

    # Cria um gráfico de linha com os resultados ao longo das temporadas
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_grouped, x='Season', y='count', hue='Res', marker='o')  # um gráfico para cada tipo de resultado
    plt.xticks(sorted(manlydf['Season'].unique()))  # coloca os anos certinhos no eixo
    plt.title(f'Contagem de Resultados por Temporada\nTimes: {", ".join(times_selecionados)}')
    plt.xlabel('Temporada')
    plt.ylabel('Contagem de Resultados')
    plt.grid(True)
    plt.tight_layout()

    # Mostra o gráfico no app
    st.pyplot(plt)
else:
    # Se o usuário não escolheu nenhum time, mostra uma mensagem
    st.info("👈 Por favor, selecione pelo menos um time na lista acima.")
