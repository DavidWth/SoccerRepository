import pandas as pd

def drop_columns_from_dataframe(data:pd.DataFrame, columns:list):
    print(f"Columns> {data.columns}< :: Columns>{columns}<")

    return data.drop(columns, axis='columns', errors='ignore')

def transform_to_datetime(data:pd.DataFrame, key:str):
    data[key] = pd.to_datetime(data[key], errors="coerce")
    return data

def remove_players_from_wrong_competition(data:pd.DataFrame, key:str):
    # Count occurrences of each club
    club_counts = data[key].value_counts()
    clubs_filtered=club_counts[club_counts<5].index.tolist()
    data_filtered = data[~data[key].isin(clubs_filtered)]
    return data_filtered

def transform_tuples(input_list):
    # Define the desired order of sources
    source_order = ['kicker', 'tf', 'fifa']
    
    # Convert list of tuples into a dictionary
    source_dict = dict(map(lambda x: (x[1], x[0]), input_list))
    # Create a list of values following the defined order, using "" if missing
    transformed_list = [source_dict.get(source, "") for source in source_order]
    
    return transformed_list
