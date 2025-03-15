import os
import pandas as pd

def load_json_file_into_dataframe(file:str):
    try:
        # Check if file exists
        if not os.path.exists(file):
            raise FileNotFoundError(f"File '{file}' not found.")

        df = pd.read_json(file)
        print(f"Reading json file> {file}. Size> {df.size} entries.")
        # Load JSON file into a DataFrame
        return pd.read_json(file)
    except FileNotFoundError as fnf_error:
            print(fnf_error)
            return []