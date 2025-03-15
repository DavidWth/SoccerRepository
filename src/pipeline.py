""" 
1. load data sources from JSON files into data frames 
2. cleaning / transforming data
    drop columns not needed
    change data types
    rename columns to align all data frames to same column names
    add multiple columns eg name normalization and source
    remove rows which do not adhere to specific rules
    drop duplicate rows
3. merging and comparing data frames 1 and 2
    merge data frame 1 and 2 on dedicated column
    apply processing to apply further merging rules
    normalize resulting data frame by carrying out steps from 1 again on new df
3. merging and comparing data frames 1/2_merged and 3
    merge data frame 1/2_merged and 3 on dedicated column
    apply processing to apply further merging rules
    normalize resulting data frame by carrying out steps from 1 again on new df


"""
import pandas as pd
import os, sys
sys.path.append(os.path.abspath('../../src'))
from src.data_sources.file_loader import load_json_file_into_dataframe
from src.processing.normalization import normalize_name
from src.processing.transformation import remove_players_from_wrong_competition
from src.processing.data_merging import merge_dataframes, find_similar_entries

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

merged_df_info=merge_dataframes(kicker, tf, ["normalized_name","dateOfBirth"])
merged_df=merged_df_info["merged_df"]

# build up normalized data frame form unmatched entries 
df_left=merged_df[merged_df["_merge"]=="left_only"][["id_x", "dateOfBirth", "normalized_name", "firstName_x","lastName_x"]]
df_right=merged_df[merged_df["_merge"]=="right_only"][["id_y", "dateOfBirth","normalized_name", "firstName_y","lastName_y"]]
# Rename columns in df1 and df2 to match the final format
df_left = df_left.rename(columns={"id_x": "id", "firstName_x": "firstName", "lastName_x": "lastName"})
df_right = df_right.rename(columns={"id_y": "id", "firstName_y": "firstName", "lastName_y": "lastName"})
# Concatenate the two DataFrames
final_df = pd.concat([df_left, df_right], ignore_index=True)
final_df = final_df[["id", "firstName", "lastName", "normalized_name", "dateOfBirth"]]

# Group by 'dateOfBirth' and filter groups with more than two entries
grouped_df = final_df.groupby("dateOfBirth").filter(lambda x: len(x) > 1)
grouped_df=grouped_df[["id", "normalized_name","dateOfBirth", "firstName", "lastName"]].sort_values(by=['dateOfBirth'], ascending=False)
print(grouped_df)
print()

ids=find_similar_entries(grouped_df)
print(ids)
print(merged_df)

print(merged_df["normalized_name"].to_list())

for id in ids:
    print(type(id[0]))
    row_x = merged_df.loc[(merged_df["normalized_name"]) == id[0]]
    print(f"{row_x}")
    row_y = merged_df.loc[merged_df["normalized_name"] == id[1]]
    print(f"{row_y}")
    