import json
import glob
import pandas as pd
import unicodedata
import re
import numpy as np

def merge_json_files(output_file="merged_players.json", file_prefix="output_tf_"):
    # Define the pattern to match all relevant JSON files
    json_files = glob.glob(f"{file_prefix}*.json")  # Matches files like output_Bayern_Munich.json

    # Initialize an empty list to store all players
    all_items = []

    # Iterate through each file and load its content
    for file in json_files:
        with open(file, "r", encoding="utf-8") as f:
            items = json.load(f)  # Each file contains a list of players
            all_items.extend(items)  # Add the players to the main list

    # Save the merged data into a new JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_items, f, indent=4, ensure_ascii=False)

    print(f"Merged {len(json_files)} files into {output_file} with {len(all_items)} items.")

# Function to normalize names
def normalize_name(first_name, last_name):
    # Convert None to empty string
    first_name = first_name or ""
    last_name = last_name or ""
    
    # Convert to lowercase
    full_name = f"{first_name} {last_name}".strip().lower()
    
    # Remove accents and special characters
    full_name = ''.join(
        c for c in unicodedata.normalize("NFKD", full_name) if unicodedata.category(c) != "Mn"
    )
    
    # Replace spaces with underscores
    full_name = re.sub(r"\s+", "_", full_name)
    
    return full_name


def prepare_data():
    # Load JSON file into a DataFrame
    kicker = pd.read_json("D:\\DevOps\\python_work\\venv\\demoenv\\output_k.json")
    # Load JSON file into a DataFrame
    tf = pd.read_json("D:\\DevOps\\python_work\\venv\\demoenv\\output_tf.json")

    # Standardize date format
    tf["dateOfBirth"] = pd.to_datetime(tf["dateOfBirth"], errors="coerce")
    kicker["dateOfBirth"] = pd.to_datetime(kicker["dateOfBirth"], errors="coerce")

    # Apply name normalization
    tf["normalized_name"] = tf.apply(lambda row: normalize_name(row["first_name"], row["last_name"]), axis=1)
    kicker["normalized_name"] = kicker.apply(lambda row: normalize_name(row["firstName"], row["lastName"]), axis=1)

    # Merge DataFrames
    merged_df = pd.merge(tf, kicker, how="outer", left_on=["normalized_name", "dateOfBirth"], right_on=["normalized_name", "dateOfBirth"], indicator=True)

    # Count matches and non-matches
    matched_entries = merged_df["_merge"].value_counts().get("both", 0)
    unmatched_entries = merged_df["_merge"].value_counts().get("left_only", 0) + merged_df["_merge"].value_counts().get("right_only", 0)

    print(f"Total merged (found) entries: {matched_entries}")
    print(f"Total without hits: {unmatched_entries}")

    # Show only the unmatched entries
    unmatched_df = merged_df[merged_df["_merge"] != "both"][["last_name", "first_name", "dateOfBirth", "lastName", "firstName"]]
    print("\nEntries without a match:\n", unmatched_df)

    # Save the merged data into a new JSON file
    unmatched_df.to_csv("players.csv", index=False)

# Step 5: Check for near matches (only among unmatched)
def is_similar(name1, name2):
    #print(f"{name1} :: {name2}")
    """Check if two names are similar by length difference and common substrings."""
    if name1 is None or name2 is None:
        return False
    if not isinstance(name1, str) or not isinstance(name2, str):
        return False
    if abs(len(name1) - len(name2)) > 10:  # Allow minor length variations
        return False
    return name1 in name2 or name2 in name1  # Simple containment check

def process_unmatched(merged_df):
    unmatched_df1 = merged_df[merged_df["_merge"] == "left_only"]
    unmatched_df2 = merged_df[merged_df["_merge"] == "right_only"]
    
    # Secondary matching on similar names but same date_of_birth
    potential_matches = []
    df_um = pd.DataFrame(columns=unmatched_df1.columns)
    for _, row1 in unmatched_df1.iterrows():
        for _, row2 in unmatched_df2.iterrows():
            if row1["dateOfBirth"] == row2["dateOfBirth"]:
                # Check if names are similar
                norm1 = row1["normalized_name"]
                norm2 = row2["normalized_name"]
                if (norm1 in norm2 or norm2 in norm1
                    or is_similar(row1["first_name"], row2["firstName"])
                    or is_similar(row1["last_name"], row2["lastName"])
                    ):  # Basic substring match
                    potential_matches.append((row1, row2))
                    
                    s1 = pd.Series(row1)
                    s2 = pd.Series(row2)
                    if np.isnan(df_um.index.max()):
                        df_um.loc[unmatched_df1.index.max() + 1] = s1.combine_first(s2)
                    else:
                        df_um.loc[df_um.index.max() + 1] = s1.combine_first(s2)