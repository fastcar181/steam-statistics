# Steam Statistics

This is a simple program that uses Steam's public API to display data and statistics for users depending on their Steam ID. It will also store basic user info (ID, gamertag, profile URL, and date joined) in an SQL database.

**NOTE:** This program is currently in its simplest form, but I will be updating it to include a GUI and more complexity.

## Requirements
You will need a **Steam API key** and the **Steam ID** of the profiles you wish to view. To register for a Steam API key, visit the [Steam site](https://steamcommunity.com/dev) for more info!

## Installation
Make sure to do `pip install requests` and `pip install streamlit` before running!

## Usage
In your Windows terminal, move to the directory with the application and then type `python -m streamlit run main.py` to run it in your web browser.