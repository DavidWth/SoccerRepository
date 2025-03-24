""" 
1. load data sources from JSON files into data frames 
2. cleaning / transforming data - Bring data sources to same columns as much as possible
    drop columns not needed
    change data types
    rename columns to align all data frames to same column names
    add multiple columns eg name normalization and source
    remove rows which do not adhere to specific rules
    drop duplicate rows
3. merge all three data sources to a single data frame using concat
4. build up list with tuples having (kicker, tf, fifa) players grouped by bod
   4.1 use several algorithm to find best matching percentagt
5. load missing players from fifa using search api
6. navigate through overall list tuples and map data accordingly to predefined mappings
"""
import pandas as pd
import os, sys
sys.path.append(os.path.abspath('../../src'))
from src.data_sources.file_loader import load_json_file_into_dataframe
from src.processing.normalization import normalize_name
from src.processing.transformation import remove_players_from_wrong_competition, transform_tuples
from src.processing.data_merging import merge_dataframes, merge_similar_entries, has_intersection, extract
import json
from rapidfuzz import process, fuzz


# prepare extract of the three sources
KICKER_FILE='D:\\DevOps\\python_work\\venv\\demoenv\\resources\\output_k.json'
TF_FILE='D:\\DevOps\\python_work\\venv\\demoenv\\resources\\output_tf.json'
FIFA_FILE='D:\\DevOps\\python_work\\venv\\demoenv\\resources\\players_fifa.json'

kicker=load_json_file_into_dataframe(KICKER_FILE)
tf=load_json_file_into_dataframe(TF_FILE)
fifa=load_json_file_into_dataframe(FIFA_FILE)

# drop/transform columns
kicker=kicker.drop(["geburtsname", "namensverlauf"], axis='columns')
tf=tf.drop(["Outfitter", "nativeName"], axis='columns')

tf=tf.rename(columns={"first_name":"firstName", "last_name":"lastName"})
fifa=fifa.rename(columns={"birthdate":"dateOfBirth"})

print(f"{fifa.info()}")
# transform to date type 
kicker["dateOfBirth"]=pd.to_datetime(kicker["dateOfBirth"], format="%Y-%m-%d")
tf["dateOfBirth"]=pd.to_datetime(tf["dateOfBirth"], format="%b %d, %Y")
fifa["dateOfBirth"]=pd.to_datetime(fifa["dateOfBirth"], errors="coerce")

# Apply name normalization
kicker["normalized_name"] = kicker.apply(lambda row: normalize_name(row["firstName"], row["lastName"]), axis=1)
tf["normalized_name"] = tf.apply(lambda row: normalize_name(row["firstName"], row["lastName"]), axis=1)
fifa["normalized_name"] = fifa.apply(lambda row: normalize_name(row["firstName"], row["lastName"]), axis=1)

kicker=remove_players_from_wrong_competition(kicker, "currentClub")
tf=remove_players_from_wrong_competition(tf, "currentClub")
fifa=remove_players_from_wrong_competition(fifa, "team")

kicker=kicker.drop_duplicates(subset=["normalized_name", "dateOfBirth"])

kicker["source"] = "kicker"
tf["source"] = "tf"
fifa["source"] = "fifa"

tf["id"] = tf["id"].apply(lambda x: str(x) if pd.notna(x) else "")

path="D:\\DevOps\\python_work\\venv\\demoenv\\resources"
print(f"Writing to {path}\\output_tf_kicker_cleansed.json")
with open(f"{path}\\output_tf_kicker_cleansed.json", 'w', encoding='utf-8') as f:
            json.dump(kicker.to_json(orient="records", force_ascii=False), f, indent=4, ensure_ascii=False)

kicker.to_csv("D:\\DevOps\\python_work\\venv\\demoenv\\resources\\output_kicker_cleansed.csv", index=False)
tf.to_csv("D:\\DevOps\\python_work\\venv\\demoenv\\resources\\output_tf_cleansed.csv", index=False)
fifa.to_csv("D:\\DevOps\\python_work\\venv\\demoenv\\resources\\output_fifa_cleansed.csv", index=False)

with open(f"{path}\\output_tf_tf_cleansed.json", 'w', encoding='utf-8') as f:
            json.dump(tf.to_json(), f, indent=4, ensure_ascii=False)
with open(f"{path}\\output_tf_fifa_cleansed.json", 'w', encoding='utf-8') as f:
            json.dump(fifa.to_json(), f, indent=4, ensure_ascii=False)

# Merge using exact match on dateOfBirth
merged_df_fuzzy = pd.concat([kicker, tf, fifa], ignore_index=True)
merged_df_fuzzy.to_csv("D:\\DevOps\\python_work\\venv\\demoenv\\resources\\output_merged_df_fuzzy.csv", index=False)

grouped_players = []
checked = set()

for i, row in merged_df_fuzzy.iterrows():
    if row["id"] in checked:
        continue

    potential_matches = merged_df_fuzzy[merged_df_fuzzy["dateOfBirth"] == row["dateOfBirth"]]
    print(f'>>{row[["id", "normalized_name", "source"]]} :: {potential_matches[["id", "normalized_name", "source"]]}<<')
    #print(potential_matches[["lastName", "source"]])
    matched = extract(
        row, 
        potential_matches,
        ["normalized_name", "lastName", "firstName", "source"]
    )
    
    print(f'{row.loc[["normalized_name", "lastName"]].tolist()} :: {matched}')
    print()

    match_ids = []
    for match_name, score, idx, source in matched: 
        if score:
            match_ids.append((merged_df_fuzzy.loc[idx]["id"], merged_df_fuzzy.loc[idx]["source"]))
            checked.add(merged_df_fuzzy.loc[idx]["id"])

    grouped_players.append({
        "dateOfBirth": row["dateOfBirth"],
        "matched_ids": transform_tuples(match_ids)
     })
    
all=pd.DataFrame(grouped_players)
print(pd.DataFrame(grouped_players))
all.to_csv("D:\\DevOps\\python_work\\venv\\demoenv\\resources\\all.csv", encoding='utf-8', index=False)