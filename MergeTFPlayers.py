import json
import glob

# Define the pattern to match all relevant JSON files
json_files = glob.glob("output_tf_*.json")  # Matches files like output_Bayern_Munich.json

# Initialize an empty list to store all players
all_players = []

# Iterate through each file and load its content
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        players = json.load(f)  # Each file contains a list of players
        all_players.extend(players)  # Add the players to the main list

# Save the merged data into a new JSON file
with open("merged_players.json", "w", encoding="utf-8") as f:
    json.dump(all_players, f, indent=4, ensure_ascii=False)

print(f"Merged {len(json_files)} files into merged_players.json with {len(all_players)} players.")
