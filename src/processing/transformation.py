import pandas as pd

def drop_columns_from_dataframe(data:pd.DataFrame, columns:list):
    print(f"Columns> {data.columns}< :: Columns>{columns}<")

    return data.drop(columns, axis='columns', errors='ignore')

def transform_to_datetime(data:pd.DataFrame, key:str):
    data[key] = pd.to_datetime(data[key], errors="coerce")
    return data

