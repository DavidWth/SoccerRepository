import pandas as pd
from rapidfuzz import process, fuzz
from difflib import SequenceMatcher

# Sample dictionaries (simulating data from 3 sources)
data1 = [
    {"id": "S1_001", "dateOfBirth": "1990-06-15", "normalized_name": "mario gomez", "firstName": "Mario", "lastName": "Gomez"},
    {"id": "S1_002", "dateOfBirth": "1985-02-23", "normalized_name": "philipp lahm", "firstName": "Philipp", "lastName": "Lahm"},
    {"id": "S1_003", "dateOfBirth": "1984-11-01", "normalized_name": "basti michael schweinsteiger", "firstName": "Bastian", "lastName": "Schweinsteiger"},
    {"id": "S1_004", "dateOfBirth": "1990-06-15", "normalized_name": "Peter Pacult", "firstName": "Peter", "lastName": "Pacult"},
    {"id": "S1_005", "dateOfBirth": "1990-06-15", "normalized_name": "xavi S", "firstName": "", "lastName": "Xavi"},
]

data2 = [
    {"id": "S2_001", "dateOfBirth": "1990-06-15", "normalized_name": "mario gómez", "firstName": "Mario", "lastName": "Gómez"},
    {"id": "S2_002", "dateOfBirth": "1984-11-01", "normalized_name": "bastian schweinsteiger", "firstName": "Bastian", "lastName": "Schweinsteiger"}
]

data3 = [
    {"id": "S3_001", "dateOfBirth": "1990-06-15", "normalized_name": "mario gomezz", "firstName": "M.", "lastName": "Gomez"},
    {"id": "S3_002", "dateOfBirth": "1985-02-23", "normalized_name": "ph. lahm", "firstName": "Ph.", "lastName": "Lahm"},
    {"id": "S3_003", "dateOfBirth": "1990-06-15", "normalized_name": "xavi", "firstName": "", "lastName": "Xavi"},
    {"id": "S3_004", "dateOfBirth": "1990-06-15", "normalized_name": "Peter Pacult", "firstName": "Peter", "lastName": "Pacult"},
]

# Convert to DataFrames
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)

# Merge using exact match on dateOfBirth
merged_df = pd.concat([df1, df2, df3], ignore_index=True)

# Fuzzy matching function
def fuzzy_match(df, threshold=70):
    grouped_players = []
    checked = set()

    for i, row in df.iterrows():
        if row["id"] in checked:
            continue

        potential_matches = df[df["dateOfBirth"] == row["dateOfBirth"]]
        best_matches = process.extract(row["normalized_name"], 
                                       potential_matches["normalized_name"], 
                                       scorer=fuzz.ratio, 
                                       limit=None)

        print(best_matches)
        #match_ids = [row["id"]]
        match_ids = []
        for match_name, score, idx in best_matches:
            if score >= threshold:
                match_ids.append(df.iloc[idx]["id"])
                checked.add(df.iloc[idx]["id"])

        grouped_players.append({
            "dateOfBirth": row["dateOfBirth"],
            "matched_ids": match_ids
        })

    return grouped_players

# Apply fuzzy matching
result = fuzzy_match(merged_df)

# Convert to DataFrame
final_df = pd.DataFrame(result)
print(final_df)