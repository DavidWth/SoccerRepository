import requests
import json
import time
from random import randint
from datetime import datetime

# Configuration (extendable and modifiable)
API_CONFIG = {
    "base_url": "https://drop-api.ea.com/rating/ea-sports-fc",
    "params": {
        "locale": "en",
        "offset": 0,   # Start at 0 and increase dynamically
        "limit": 100,  # Max items per request
        "team": "21,112172,111235,110329,100409,10029,1831,1824,576,175,169,160,38,36,32,25,23,22"
    },
    "fields_to_keep": ["id", "rank", "overallRating", "firstName", "lastName", "birthdate", "height", "preferredFoot", "leagueName", "weight", "gender", "nationality", "team", "position", "[stats][dri]"]
}


def fetch_players_using_params():
    headers = {"User-Agent": "Mozilla/5.0"} 
    
    """Fetch all players from the API handling pagination."""
    all_players = []
    offset = API_CONFIG["params"]["offset"]
    limit = API_CONFIG["params"]["limit"]

    while True:
        API_CONFIG["params"]["offset"] = offset
        response = requests.get(API_CONFIG["base_url"], params=API_CONFIG["params"], headers=headers)
        #response = requests.get("https://drop-api.ea.com/rating/ea-sports-fc?locale=en&offset=20000&limit=10&team=21%2C112172%2C111235%2C110329%2C100409%2C10029%2C1831%2C1824%2C576%2C175%2C169%2C160%2C38%2C36%2C32%2C25%2C23%2C22", headers=headers)

        time.sleep(randint(1,5))  

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
        
        data = response.json()

        players = data.get("items", [])  # Ensure 'items' exists

        if not players:
            break  # Stop when no more data is returned

        total_items = data.get("totalItems", -1)
        print(f"{type(data)} :: {type(players[0])} :: {total_items}")
        

        # Filter relevant attributes
        # filtered_players = [
        #     {key: player.get(key, None) for key in API_CONFIG["fields_to_keep"]}
        #     for player in players
        # ]

        for player in players:
            filtered_player = _map_response_to_needed_attributes(player)
            print(f'{filtered_player}')

            all_players.append(filtered_player)

        offset += limit  # Move to the next batch
        

    return all_players

# provide a list with name, birthdate tuples and call API
# for each search a dict is returned, either with data or empty
def load_players_using_search(players_search:list):
    players = []

    for name, bod in players_search:
        players.append(load_player_using_search(name, bod))

    return players

# provide player name (first, last) and birth of date to find exactly one player
# return empty dict, or exactly one dict
def load_player_using_search(name:str, dateOfBirth:str):
    headers = {"User-Agent": "Mozilla/5.0"}     
    name = name.replace(" ", "+")
    url = f"https://drop-api.ea.com/rating/ea-sports-fc?locale=en&limit=100&search={name}"

    print(f"Searching for {url}...")
    response = requests.get(f"{url}", headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return {}
            
    data = response.json()
    players = data.get("items", [])  # Ensure 'items' exists

    if not players:
        print(f"Error: no players found.")
        return {}

    total_items = data.get("totalItems", -1)
    print(f"Found {total_items} player(s) with {name}.")

    # TODO iterate if > 1
    dob = players[0]["birthdate"].split(" ")
    date1 = datetime.strptime(dob[0], "%m/%d/%Y").date()
    date2 = datetime.strptime(dateOfBirth, "%Y-%m-%d").date()

    if (date1 == date2):
        return _map_response_to_needed_attributes(players[0])
    else:
        return {}

def load():
    # Fetch and save data
    players_data = fetch_players_using_params()

    # Save filtered data to a file
    with open("players_fifa.json", "w", encoding="utf-8") as file:
        json.dump(players_data, file, indent=4, ensure_ascii=False)

    print(f"Saved {len(players_data)} players to players.json")

def _map_response_to_needed_attributes(player:dict):
    filtered_player = {
                "id": player["id"],
                "rank": player["rank"],
                "overallRating": player["overallRating"],
                "firstName": player["firstName"],
                "lastName": player["lastName"],
                "birthdate": player["birthdate"],
                "height": player["height"],
                "preferredFoot": player["preferredFoot"],
                "leagueName": player["leagueName"],
                "weight": player["weight"],
                "nationality": player["nationality"]["label"],
                "team": player["team"]["label"],
                "position": player["position"]["label"],
                "stats": {key: player["stats"][key] for key in ["def", "dri", "pac", "pas", "phy", "sho"] if key in player["stats"]}
    }

    return filtered_player