# Steam Statistics App
This is a simple Python program that integrates the Steam API to fetch and display info on a user's profile, including their games and playtime for each. These users are added to a database and can be viewed later. A person can also generate a graph of all the genres in their library, seeing which genres they tend to prefer.

## Status
I plan to implement a Flask backend to turn this into more of an API development project rather than an API integration project.

## Requirements
You will need a **Steam API key** and the **Steam ID** of the profiles you wish to view. To register for a Steam API key, visit the [Steam site](https://steamcommunity.com/dev) for more info!

## Installation
Make sure to do `pip install requests` and `pip install streamlit` before running!

## Usage
In your Windows terminal, move to the `src` folder and then type `python -m streamlit run app.py` to run it in your web browser.