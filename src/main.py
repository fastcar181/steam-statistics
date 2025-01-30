# import requests
# import datetime
# import sqlite3
# import streamlit as st
# import json

# def create_table():
#     with sqlite3.connect("steam.db") as connection:
#         cursor = connection.cursor() # Execute queries
        
#         cursor.execute("""CREATE TABLE IF NOT EXISTS users (
#                             steam_ID TEXT PRIMARY KEY,
#                             gamertag TEXT,
#                             avatar_medium TEXT,
#                             profile_url TEXT,
#                             date_joined TEXT
#                         )""")
        
#         cursor.execute("""CREATE TABLE IF NOT EXISTS games (
#                             steam_ID TEXT PRIMARY KEY,
#                             games_owned INTEGER,
#                             games_appIDs TEXT,
#                             games_names TEXT,
#                             games_images TEXT,
#                             games_playtimes TEXT
#                         )""")

# def insert_player_info(steam_ID, gamertag, avatar_medium, profile_url, date_joined):
#     with sqlite3.connect("steam.db") as connection:
#         cursor = connection.cursor()
#         cursor.execute("""INSERT OR REPLACE INTO users (steam_ID, gamertag, avatar_medium, profile_url, date_joined) VALUES (?, ?, ?, ?, ?)""", (steam_ID, gamertag, avatar_medium, profile_url, date_joined))
#         connection.commit()

# def insert_game_info(steam_ID, games_owned, games_appIDs, games_names, games_images, games_playtimes):
#     with sqlite3.connect("steam.db") as connection:
#         cursor = connection.cursor()
#         cursor.execute("""INSERT OR REPLACE INTO games (steam_ID, games_owned, games_appIDs, games_names, games_images, games_playtimes) VALUES (?, ?, ?, ?, ?, ?)""", (steam_ID, games_owned, json.dumps(games_appIDs), json.dumps(games_names), json.dumps(games_images), json.dumps(games_playtimes)))

# def fetch_players():
#     with sqlite3.connect("steam.db") as connection:
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM users")
#         return cursor.fetchall()
    
# def fetch_games(steam_ID):
#     with sqlite3.connect("steam.db") as connection:
#         cursor = connection.cursor()
#         cursor.execute("SELECT * from games WHERE steam_ID = ?", (steam_ID,))
#         return cursor.fetchone()

# # This function gets the player's info at the specified ID using the key, attempting to display the info if both parameters are valid
# def get_player_info(API_key, steam_ID):
#     games_owned = 0
#     games_appIDs = []
#     games_names = []
#     games_images = []
#     games_playtimes = []
#     # Get the player summary at the steam ID passed in as a parameter
#     PLAYER_SUMMARIES_URL = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + API_key + "&steamids=" + steam_ID
#     PLAYER_OWNED_GAMES_URL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + API_key + "&steamid=" + steam_ID + "&format=json&include_appinfo=true"
#     data_player_summaries = fetch_steam_api(PLAYER_SUMMARIES_URL)
#     if not data_player_summaries:
#         return
#     # Check if we found a profile with the steam ID
#     if(len(data_player_summaries["response"]["players"]) > 0):
#         gamertag = data_player_summaries["response"]["players"][0]["personaname"]
#         profile_URL = data_player_summaries["response"]["players"][0]["profileurl"]
#         avatar_medium = data_player_summaries["response"]["players"][0]["avatarmedium"]
#         # Convert from Epoch to date
#         date_joined = datetime.datetime.utcfromtimestamp(data_player_summaries["response"]["players"][0]["timecreated"])
#         st.image(avatar_medium)
#         st.write(gamertag)
#         st.write(profile_URL)
#         st.write("Date joined: " + str(date_joined))
#         insert_player_info(steam_ID, gamertag, avatar_medium, profile_URL, date_joined)
#     else:
#         st.error("Hey, that Steam account doesn't exist!")
#         return
#     # Successful response...
#     data_player_games_owned = fetch_steam_api(PLAYER_OWNED_GAMES_URL)
#     if not data_player_games_owned:
#         return
#     # Check if we found a profile with the steam ID
#     if(len(data_player_games_owned["response"]["games"]) > 0):
#         games_owned = data_player_games_owned["response"]["game_count"]
#         # Keeping an index of the game with the most playtime and the hours
#         index = 0
#         most_played = 0
#         # Iterate through all of the owned games, displaying the name, the hours, and checking if its the most played game seen up to this point
#         for i in range(games_owned):
#             name = data_player_games_owned["response"]["games"][i]["name"]
#             playtime = round(data_player_games_owned["response"]["games"][i]["playtime_forever"]/60)
#             appID = data_player_games_owned["response"]["games"][i]["appid"]
#             image_URL = "http://media.steampowered.com/steamcommunity/public/images/apps/" + str(appID) + "/" + data_player_games_owned["response"]["games"][i]["img_icon_url"] + ".jpg"
#             # If the current game has more playtime than the previous one, replace the most played time and keep track of the index
#             if most_played < playtime:
#                 most_played = playtime
#                 index = i
#             games_appIDs.append(appID)
#             games_names.append(name)
#             games_images.append(image_URL)
#             games_playtimes.append(playtime)
#     else:
#         st.error("Hey, that Steam account doesn't exist!")
#         return
#     st.write("Most played game: " + data_player_games_owned["response"]["games"][index]["name"])
#     insert_game_info(steam_ID, games_owned, games_appIDs, games_names, games_images, games_playtimes)
#     display_game_info(games_images, games_names, games_playtimes, games_owned)

# def display_game_info(games_images, games_names, games_playtimes, games_owned):
#     for i in range(games_owned):
#         with st.expander(f"{games_names[i]} ({games_playtimes[i]} hours)"):
#             st.image(games_images[i])

# @st.cache_data
# def determine_genres(steam_ID):
#     genres_dict = {} # Key will be genre, value will be number of times this genre is present
#     games = fetch_games(steam_ID)
#     if not games:
#         return genres_dict
    
#     games_owned = games[1]
#     for i in range(games_owned):
#         appID = json.loads(games[2])[i] # Get the app id of the current game
#         appID_URL = "https://store.steampowered.com/api/appdetails?appids=" + str(appID)
#         data_app_details = fetch_steam_api(appID_URL)
#         if not data_app_details:
#             continue
#         # Some games (like test servers) do not have a "data" key, so skip over them
#         if "data" not in data_app_details[str(appID)]:
#             continue
#         # Some games do not have a genre key, so skip over them
#         if "genres" not in data_app_details[str(appID)]["data"]:
#             continue
#         genres = data_app_details[str(appID)]["data"]["genres"] # List of the genres of the game
#         for gen in genres:
#             genre = gen["description"]
#             # Old genre, increase by 1
#             if genre in genres_dict:
#                 genres_dict[genre] += 1
#             # New genre
#             else:
#                 genres_dict[genre] = 1
#     print(genres_dict)
#     return genres_dict

# @st.cache_data
# def fetch_steam_api(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return None

# def main():
#     st.title("Steam Statistics")
#     create_table()
#     choice = st.selectbox("Select: ", ("Add a user", "View existing users"))
#     if choice == "Add a user":
#         API_key = st.text_input("Enter your Steam API key: ")
#         steam_ID = st.text_input("Enter your Steam ID: ")
#         if st.button("Search"):
#             if API_key and steam_ID:
#                 get_player_info(API_key, steam_ID)
#             else:
#                 st.warning("You need to enter an API key AND a Steam ID!")
#     elif choice == "View existing users":
#         players = fetch_players()
#         if players:
#             for row in players:
#                 st.write("ID: " + row[0])
#                 st.write("Gamertag: " + row[1])
#                 st.image(row[2])
#                 st.write("Profile URL: " + row[3])
#                 st.write("Date joined: " + row[4])
#                 if st.button("Load game data"):
#                     genres_dict = determine_genres(row[0])
#                     st.bar_chart(genres_dict)
#         else:
#             st.info("No users found in database.")

# main()