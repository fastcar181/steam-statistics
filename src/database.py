import sqlite3
import json

def create_table():
    with sqlite3.connect("steam.db") as connection:
        cursor = connection.cursor() # Execute queries
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            steam_ID TEXT PRIMARY KEY,
                            gamertag TEXT,
                            avatar_medium TEXT,
                            profile_url TEXT,
                            date_joined TEXT
                        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS games (
                            steam_ID TEXT PRIMARY KEY,
                            games_owned INTEGER,
                            games_appIDs TEXT,
                            games_names TEXT,
                            games_images TEXT,
                            games_playtimes TEXT
                        )""")

def insert_player_info(steam_ID, gamertag, avatar_medium, profile_url, date_joined):
    with sqlite3.connect("steam.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""INSERT OR REPLACE INTO users (steam_ID, gamertag, avatar_medium, profile_url, date_joined) VALUES (?, ?, ?, ?, ?)""", (steam_ID, gamertag, avatar_medium, profile_url, date_joined))
        connection.commit()

def insert_game_info(steam_ID, games_owned, games_appIDs, games_names, games_images, games_playtimes):
    with sqlite3.connect("steam.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""INSERT OR REPLACE INTO games (steam_ID, games_owned, games_appIDs, games_names, games_images, games_playtimes) VALUES (?, ?, ?, ?, ?, ?)""", (steam_ID, games_owned, json.dumps(games_appIDs), json.dumps(games_names), json.dumps(games_images), json.dumps(games_playtimes)))

def fetch_players():
    with sqlite3.connect("steam.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    
def fetch_games(steam_ID):
    with sqlite3.connect("steam.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * from games WHERE steam_ID = ?", (steam_ID,))
        return cursor.fetchone()