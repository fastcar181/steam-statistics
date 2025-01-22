import requests
import datetime
import sqlite3
import streamlit as st

sqliteConnection = sqlite3.connect("steam.db") # Connect to database
cursor = sqliteConnection.cursor() # Execute queries

# The steam ID is the primary key and is unique, meaning a person's profile will only be on the table once
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    steam_id TEXT PRIMARY KEY,
                    gamertag TEXT,
                    avatarmedium TEXT,
                    profile_url TEXT,
                    date_joined TEXT
                  )""")

# This function gets the player's info at the specified ID using the key, attempting to display the info if both parameters are valid
def getPlayerInfo(API_key, steam_ID):
    games_images = []
    games_names = []
    games_playtimes = []
    games_owned = 0
    # Get the player summary at the steam ID passed in as a parameter
    PLAYER_SUMMARIES_URL = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + API_key + "&steamids=" + steam_ID
    PLAYER_OWNED_GAMES_URL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + API_key + "&steamid=" + steam_ID + "&format=json"
    params = {
        "key": API_key,   
        "steamid": steam_ID,
        "include_appinfo": True # For additional info on games
    }
    # JSON response of the requests
    response_player_summaries = requests.get(PLAYER_SUMMARIES_URL)
    response_player_games_owned = requests.get(PLAYER_OWNED_GAMES_URL, params=params)
    # Successful response...
    if(response_player_summaries.status_code == 200):
        data_player_summaries = response_player_summaries.json()
        # Check if we found a profile with the steam ID
        if(len(data_player_summaries["response"]["players"]) > 0):
            gamertag = data_player_summaries["response"]["players"][0]["personaname"]
            profile_URL = data_player_summaries["response"]["players"][0]["profileurl"]
            avatarmedium = data_player_summaries["response"]["players"][0]["avatarmedium"]
            # Convert from Epoch to date
            date_joined = datetime.datetime.utcfromtimestamp(data_player_summaries["response"]["players"][0]["timecreated"])
            cursor.execute("""INSERT OR REPLACE INTO users (steam_id, gamertag, avatarmedium, profile_url, date_joined) VALUES (?, ?, ?, ?, ?)""", (steam_ID, gamertag, avatarmedium, profile_URL, date_joined))
            sqliteConnection.commit()
            st.image(avatarmedium)
            st.write(gamertag)
            st.write(profile_URL)
            st.write("Date joined: " + str(date_joined))
        else:
            print("Hey, that Steam account doesn't exist!")
    else:
        print("Error fetching player's summaries data!")
    # Successful response...
    if(response_player_games_owned.status_code == 200):
        data_player_games_owned = response_player_games_owned.json()
        # Check if we found a profile with the steam ID
        if(len(data_player_games_owned["response"]["games"]) > 0):
            games_owned = data_player_games_owned["response"]["game_count"]
            # Keeping an index of the game with the most playtime and the hours
            index = 0
            most_played = 0
            # Iterate through all of the owned games, displaying the name, the hours, and checking if its the most played game seen up to this point
            for i in range(games_owned):
                name = data_player_games_owned["response"]["games"][i]["name"]
                playtime = round(data_player_games_owned["response"]["games"][i]["playtime_forever"]/60)
                appid = data_player_games_owned["response"]["games"][i]["appid"]
                image_URL = "http://media.steampowered.com/steamcommunity/public/images/apps/" + str(appid) + "/" + data_player_games_owned["response"]["games"][i]["img_icon_url"] + ".jpg"
                # If the current game has more playtime than the previous one, replace the most played time and keep track of the index
                if most_played < playtime:
                    most_played = playtime
                    index = i
                games_images.append(image_URL)
                games_names.append(name)
                games_playtimes.append(playtime)
        else:
            print("Hey, that Steam account doesn't exist!")
        st.write("Most played game: " + data_player_games_owned["response"]["games"][index]["name"])
    else:
        print("Error fetching player's games owned data!")
    displayGameInfo(games_images, games_names, games_playtimes, games_owned)

def displayGameInfo(games_images, games_names, games_playtimes, games_owned):
    for i in range(games_owned):
        col_1, col_2 = st.columns(2)
        with col_1:
            st.image(games_images[i])
        with col_2:
            st.write(games_names[i] + " (" + str(games_playtimes[i]) + " hours)")

def main():
    st.title("Steam App")
    choice = st.selectbox("Select: ", ("View existing users", "Add a user", "Exit"))
    if choice == "View existing users":
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            st.write("ID: " + str(row[0]))
            st.write("Gamertag: " + str(row[1]))
            st.image(row[2])
            st.write("Profile URL: " + str(row[3]))
            st.write("Date joined: " + str(row[4]))
    elif choice == "Add a user":
        API_key = st.text_input("Enter your Steam API key: ")
        steam_ID = st.text_input("Enter your Steam ID: ")
        if st.button("Search"):
            if API_key and steam_ID:
                getPlayerInfo(API_key, steam_ID)
            else:
                st.warning("you're on thin ice pal!")
    elif choice == "Exit":
        st.write("bye!")
        sqliteConnection.close()

main()