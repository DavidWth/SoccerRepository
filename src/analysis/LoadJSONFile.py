import json
import os
import sys
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('./src/analysis'))
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

def load_JSON_file():
        # File paths
        file_path = 'bundesliga.json'
        output_file_path = 'PlayerNamesOutput.json'
        folder = Path.cwd() / "src/analysis"
        full = folder.joinpath(file_path)
        try:
            # Check if file exists
            if not os.path.exists(full):
                raise FileNotFoundError(f"File '{full}' not found.")
            
            # Open and read the file
            with open(full, 'r') as file:
                data = json.load(file)  # Try to load the JSON data
                # if not isinstance(data, list) or not all('name' in item for item in data):
                #     raise ValueError("Invalid JSON structure. Expected a list of dictionaries with 'name' key.")
                
                # # Extract names into a list
                # player_names = [item['name'] for item in data]
                # print(player_names)
                #df = pd.json_normalize(data["players"])
                print(json.dumps(data, indent=4))

                df = pd.DataFrame(data["players"])

                # Set 'id' as the index
                df.set_index("id", inplace=True)



                # Convert 'dateOfBirth' to datetime
                df['dateOfBirth'] = pd.to_datetime(df['dateOfBirth'])

                # Calculate age
                today = datetime.today()
                df['age'] = df['dateOfBirth'].apply(lambda x: today.year - x.year)
                print(df)

                # Compute average height and weight
                avg_height = df['height'].mean()
                avg_weight = df['weight'].mean()
                avg_age = df['age'].mean()

                print(f"Average Height: {avg_height:.2f} cm")
                print(f"Average Weight: {avg_weight:.2f} kg")
                print(f"Average Age: {avg_age}")

                # Plot histogram of ages
                plt.figure(figsize=(8, 4))
                sns.histplot(df['age'], bins=5, kde=True)
                plt.xlabel("Age")
                plt.ylabel("Count")
                plt.title("Histogram of Player Ages")
                plt.show()
        except FileNotFoundError as fnf_error:
            print(fnf_error)
        except json.JSONDecodeError as json_error:
            print(f"Error parsing JSON: {json_error}")
        except ValueError as val_error:
            print(val_error)