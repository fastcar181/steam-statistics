import streamlit as st
from database import create_table, fetch_players
from api import get_player_info, determine_genres

def main():
    st.title("Steam Statistics")
    create_table()
    choice = st.selectbox("Select: ", ("Add a user", "View existing users"))
    if choice == "Add a user":
        API_key = st.text_input("Enter your Steam API key: ")
        steam_ID = st.text_input("Enter your Steam ID: ")
        if st.button("Search"):
            if API_key and steam_ID:
                get_player_info(API_key, steam_ID)
            else:
                st.warning("You need to enter an API key AND a Steam ID!")
    elif choice == "View existing users":
        players = fetch_players()
        if players:
            for row in players:
                st.write("ID: " + row[0])
                st.write("Gamertag: " + row[1])
                st.image(row[2])
                st.write("Profile URL: " + row[3])
                st.write("Date joined: " + row[4])
                if st.button("Load game data"):
                    genres_dict = determine_genres(row[0])
                    st.bar_chart(genres_dict)
        else:
            st.info("No users found in database.")

if __name__ == "__main__":
    main()