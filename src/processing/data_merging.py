import pandas as pd
import numpy as np
import itertools

# Merges two data frames and provides some reporting
# Precondition is merging is on same column names
def merge_dataframes(df1:pd.DataFrame, df2:pd.DataFrame, merge_on:list, how="outer"):
    # Merge DataFrames
    merged_df = pd.merge(df1, df2, how=how, left_on=merge_on, right_on=merge_on, indicator=True)

    # Count matches and non-matches
    matched_entries = merged_df["_merge"].value_counts().get("both", 0)
    unmatched_entries = merged_df["_merge"].value_counts().get("left_only", 0) + merged_df["_merge"].value_counts().get("right_only", 0)

    print(f"Total matched entries  : {matched_entries}")
    print(f"Total unmatched entries: {unmatched_entries}")

    data = {
        "merged_df": merged_df,
        "matched": matched_entries,
        "unmatched": unmatched_entries
    }

    return data 
    
# Takes a previously merged data frame having dedicated columns (merge_, ..._x, ..._y)
def merge_on_additional_attributes(merged_df:pd.DataFrame):
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
    
    merged_df.drop(index_list, inplace=True)
    df_um["_merge"]='both_'
    
    return df_um

# Takes a dataframe and checks rows with same dob on similarities on some name columns 
# Expected column(s): for grouping> dateOfBirth; for similarity> lastName, firstName, normalized_name
# return a list of tuples having (id1, id2)
def merge_similar_entries(df:pd.DataFrame):    
    # Group by 'dateOfBirth' and filter groups with more than two entries
    grouped_df = df.groupby("dateOfBirth").filter(lambda x: len(x) > 1)
    
    # Iterate over each group
    merged_df_new=pd.DataFrame()
    for date, group in grouped_df.groupby("dateOfBirth"):
        print(f"\nChecking group with dateOfBirth: {date}")
        
        # Compare names within the group
        for (idx1, row1), (idx2, row2) in itertools.combinations(group.iterrows(), 2):

            if is_similar(row1["lastName"], row2["lastName"]):
                df_new=merge_dataframes(pd.DataFrame([row1], columns=df.columns), pd.DataFrame([row2], columns=df.columns), ['dateOfBirth'])    
                df_from_dict=(df_new["merged_df"])

                merged_df_new=pd.concat([merged_df_new, df_from_dict])
                break
            if is_similar(row1["firstName"], row2["firstName"]):
                df_new=merge_dataframes(pd.DataFrame([row1], columns=df.columns), pd.DataFrame([row2], columns=df.columns), ['dateOfBirth'])    
                df_from_dict=(df_new["merged_df"])
                merged_df_new=pd.concat([merged_df_new, df_from_dict])
                break
            if is_similar(row1["normalized_name"], row2["normalized_name"]):
                df_new=merge_dataframes(pd.DataFrame([row1], columns=df.columns), pd.DataFrame([row2], columns=df.columns), ['dateOfBirth'])    
                df_from_dict=(df_new["merged_df"])
                merged_df_new=pd.concat([merged_df_new, df_from_dict])
                break

    return merged_df_new

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