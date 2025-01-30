# Steam Statistics App

This is a simple program that uses Steam's public API to display data and statistics for users depending on their Steam ID. It will also store basic user info (ID, gamertag, avatar, profile URL, and date joined) in an SQL database.

## Updates
I plan to make the `View existing users` selection to allow the user to select one of the users in the database and view that user's game info. Right now, it just displays the player info of the users in the database.

## Requirements
You will need a **Steam API key** and the **Steam ID** of the profiles you wish to view. To register for a Steam API key, visit the [Steam site](https://steamcommunity.com/dev) for more info!

## Installation
Make sure to do `pip install requests` and `pip install streamlit` before running!

## Usage
In your Windows terminal, move to the `src` folder and then type `python -m streamlit run app.py` to run it in your web browser.