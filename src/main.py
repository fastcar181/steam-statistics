import requests
import datetime
import time

# This function gets the player's info at the specified ID using the key, attempting to display the info if both parameters are valid
def getPlayerInfo(API_key, steam_ID):
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
        print(len(data_player_summaries["response"]["players"]))
        # Check if we found a profile with the steam ID
        if(len(data_player_summaries["response"]["players"]) > 0):
            gamertag = data_player_summaries["response"]["players"][0]["personaname"]
            profile_URL = data_player_summaries["response"]["players"][0]["profileurl"]
            # Convert from Epoch to date
            date_joined = datetime.datetime.utcfromtimestamp(data_player_summaries["response"]["players"][0]["timecreated"])
            last_online = datetime.datetime.utcfromtimestamp(data_player_summaries["response"]["players"][0]["lastlogoff"])
            print("Gamertag: " + gamertag)
            print("Profile URL: " + profile_URL)
            print("Date joined: " + str(date_joined))
            print("Last online: " + str(last_online))
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
            print("# of games owned: " + str(games_owned))
            # Keeping an index of the game with the most playtime and the hours
            index = 0
            most_played = 0
            # Iterate through all of the owned games, displaying the name, the hours, and checking if its the most played game seen up to this point
            for i in range(games_owned):
                name = data_player_games_owned["response"]["games"][i]["name"]
                playtime = round(data_player_games_owned["response"]["games"][i]["playtime_forever"]/60)
                # If the current game has more playtime than the previous one, replace the most played time and keep track of the index
                if most_played < playtime:
                    most_played = playtime
                    index = i
                print("Game #" + str(i+1) + ": " + name + " [" + str(playtime) + " hours]")
            print("Most played game: " + data_player_games_owned["response"]["games"][index]["name"] + " with " + str(most_played) + " hours")
        else:
            print("Hey, that Steam account doesn't exist!")
    else:
        print("Error fetching player's games owned data!")
def main():
    while(True):
        API_key = input("Enter your Steam API key (\"exit\" to quit): ")
        if API_key.lower() == "exit":
            break
        else:
            steam_ID = input("Enter your Steam ID: ")
            getPlayerInfo(API_key, steam_ID)
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(1)
            print("")

main()