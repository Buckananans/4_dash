import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

data_nba = pd.read_csv("nba_all_elo.csv")


#valores unicos 
year_list = sorted(data_nba['year_id'].unique())

# Sidebar
st.sidebar.title("Filtros")
with st.sidebar:
# Selectbox de año
        selected_year = st.sidebar.selectbox("Selecciona el año", year_list)

        # Filtrar por año
        filtered_year = data_nba[data_nba['year_id'] == selected_year]

        # Selectbox de equipo
        team_list = sorted(filtered_year['fran_id'].unique())
        selected_team = st.sidebar.selectbox("Selecciona el equipo", team_list)

# Pills para tipo de juego
game_type = st.sidebar.pills(
    "Tipo de juego",
    options=["Temporada regular", "Playoffs", "Ambos"],
    selection_mode='single'
)

# Filtro por tipo de juego
if game_type == "Temporada regular":
    filtered_games = filtered_year[(filtered_year['fran_id'] == selected_team) & (filtered_year['is_playoffs'] == 0)]#no es play off
elif game_type == "Playoffs":
    filtered_games = filtered_year[(filtered_year['fran_id'] == selected_team) & (filtered_year['is_playoffs'] == 1)]# si es play off
else:
    filtered_games = filtered_year[filtered_year['fran_id'] == selected_team]# veces que aparce el equipo independientemente del juego
    
# Ordenar por fecha
filtered_games = filtered_games.sort_values(by="date_game")

#calculo de acumulados 
filtered_games['win'] = (filtered_games['game_result'] == 'W').astype(int)
filtered_games['loss'] = (filtered_games['game_result'] == 'L').astype(int)
filtered_games['win_cum'] = filtered_games['win'].cumsum()
filtered_games['loss_cum'] = filtered_games['loss'].cumsum()

ganados_df = filtered_games[filtered_games['game_result'] == 'W'][['date_game', 'fran_id', 'pts', 'opp_pts']]
perdidos_df = filtered_games[filtered_games['game_result'] == 'L'][['date_game', 'fran_id', 'pts', 'opp_pts']]

# Mostrar tabla de juegos ganados
st.subheader(f"Juegos ganados por {selected_team} en {selected_year}")
st.dataframe(ganados_df.reset_index(drop=True), use_container_width=True)

# Mostrar tabla de juegos perdidos
st.subheader(f"Juegos perdidos por {selected_team} en {selected_year}")
st.dataframe(perdidos_df.reset_index(drop=True), use_container_width=True)

        # Gráfica de líneas
st.subheader(f"{selected_team} - Acumulado de juegos ganados y perdidos ({selected_year})")
fig1, ax1 = plt.subplots()
ax1.plot(filtered_games['date_game'], filtered_games['win_cum'], label='Ganados', color='green')
ax1.plot(filtered_games['date_game'], filtered_games['loss_cum'], label='Perdidos', color='purple')
ax1.set_xlabel("Fecha")
ax1.set_ylabel("Cantidad acumulada")
ax1.legend()
plt.xticks(rotation=45) 
st.pyplot(fig1)

# Gráfica de pastel
total_wins = filtered_games['win'].sum()
total_losses = filtered_games['loss'].sum()
st.subheader("Porcentaje de resultados")
fig2, ax2 = plt.subplots()
ax2.pie([total_wins, total_losses], labels=["Ganados", "Perdidos"], autopct='%2.2f%%', startangle=90)
ax2.axis("equal")
st.pyplot(fig2)