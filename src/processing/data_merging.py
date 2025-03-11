import pandas as pd
import numpy as np

# Merges two data frames and provides some reporting
# Precondition is merging is on same column names
def merge_dataframes(df1:pd.DataFrame, df2:pd.DataFrame, merge_on:list, how="outer"):
    # Merge DataFrames
    merged_df = pd.merge(df1, df2, how=how, left_on=merge_on, right_on=merge_on, indicator=True)

    # Count matches and non-matches
    matched_entries = merged_df["_merge"].value_counts().get("both", 0)
    unmatched_entries = merged_df["_merge"].value_counts().get("left_only", 0) + merged_df["_merge"].value_counts().get("right_only", 0)

    print(f"Total merged (found) entries: {matched_entries}")
    print(f"Total without hits: {unmatched_entries}")

    data = {
        "merged_df": merged_df,
        "matched": matched_entries,
        "unmatched": unmatched_entries
    }

    return data 

def match_on_additional_atributes(merged_df:pd.DataFrame):
    unmatched_df1 = merged_df[merged_df["_merge"] == "left_only"]
    unmatched_df2 = merged_df[merged_df["_merge"] == "right_only"]
    
    # Secondary matching on similar names but same date_of_birth
    index_list = []
    df_um = pd.DataFrame(columns=merged_df.columns)
    for index1, row1 in unmatched_df1.iterrows():
        for index2, row2 in unmatched_df2.iterrows():
            if row1["dateOfBirth"] == row2["dateOfBirth"]:
                # Check if names are similar
                norm1 = row1["normalized_name"]
                norm2 = row2["normalized_name"]
                if (norm1 in norm2 or norm2 in norm1
                    or is_similar(row1["firstName_x"], row2["firstName_y"])
                    or is_similar(row1["lastName_x"], row2["lastName_y"])
                    ):  # Basic substring match
                    
                    s1 = pd.Series(row1)
                    s2 = pd.Series(row2)
                    if np.isnan(df_um.index.max()):
                        df_um.loc[unmatched_df1.index.max() + 1] = s1.combine_first(s2)
                    else:
                        df_um.loc[df_um.index.max() + 1] = s1.combine_first(s2)

                    index_list.append(index1)
                    index_list.append(index2)
                    #print(row1)
    print(f"index list> {index_list}")
    print(f"merged_df count> {len(merged_df)}")
    merged_df.drop(index_list, inplace=True)
    print(f"merged_df count> {len(merged_df)}")
    
    #merged_df.iloc[index_list]["_merge"] = 'merged'
    df_um["_merge"]='both_'
    return df_um

# Check for near matches (only among unmatched)
def is_similar(name1, name2):
    print(f"{name1} :: {name2}")
    """Check if two names are similar by length difference and common substrings."""
    if not name1 or not name2:
        return False
    if not isinstance(name1, str) or not isinstance(name2, str):
        return False
    if abs(len(name1) - len(name2)) > 10:  # Allow minor length variations
        return False
    return name1 in name2 or name2 in name1  # Simple containment check