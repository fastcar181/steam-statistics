import streamlit as st

def display_game_info(games_images, games_names, games_playtimes, games_owned):
    for i in range(games_owned):
        with st.expander(f"{games_names[i]} ({games_playtimes[i]} hours)"):
            st.image(games_images[i])