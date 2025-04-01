import unittest
import sys, os
import pandas as pd  # Added pandas import
sys.path.append(os.path.abspath('../../src/'))
from src.data_sources.file_loader import load_json_file_into_dataframe
from data_sources import FifaAPIClient as fifa

class FifaExtractDataTest(unittest.TestCase):
    def setUp(self):
        # prepare extract of the three sources
        KICKER_FILE='D:\\DevOps\\python_work\\venv\\demoenv\\resources\\output_k.json'
        TF_FILE='D:\\DevOps\\python_work\\venv\\demoenv\\resources\\output_tf.json'
        FIFA_FILE='D:\\DevOps\\python_work\\venv\\demoenv\\resources\\players_fifa.json'

        self.kicker=load_json_file_into_dataframe(KICKER_FILE)
        self.tf=load_json_file_into_dataframe(TF_FILE)
        self.fifa=load_json_file_into_dataframe(FIFA_FILE)

        # load csv file with missing players
        csv_file_path = os.path.abspath('D:/DevOps/python_work/venv/demoenv/resources/missing_players.csv')
        self.csv_data = pd.read_csv(csv_file_path)  # Use pandas to read the CSV file into a DataFrame
        
    def tearDown(self):
        print("Cleaning up after test...")

    def test_load_missing_players_using_file(self):
        print(self.csv_data.head())  # Display the first few rows of the DataFrame

        # load csv file with missing players ()

    def test_search_players_from_missing_list(self):
        # Transform matched_ids column from string to list
        self.csv_data['matched_ids'] = self.csv_data['matched_ids'].apply(eval)  # Convert string to list using eval

        # Filter matched_ids to remove lists where the third element is not empty
        filtered_matched_ids = [
            item for item in self.csv_data['matched_ids'] if len(item) > 2 and item[2] == ''
        ]

        #  [...,('budu-zivzivadze', 'kicker'), ('810826', 'tf'),...]
        missing_list = [(sublist[0], 'kicker') if sublist[0] else (sublist[1], 'tf') for sublist in filtered_matched_ids]       

        ids_kicker = [ids[0] for ids in missing_list if ids[1] == 'kicker']
        ids_tf = [int(ids[0]) for ids in missing_list if ids[1] == 'tf']
        print(f"{len(ids_kicker)} ids found in kicker missing list") 
        print(f"{len(ids_tf)} ids found in tf missing list") 

        # kicker
        player_search=self.kicker[self.kicker['id'].isin(ids_kicker)][['lastName', 'dateOfBirth']]
        search_list=[(player['lastName'], player['dateOfBirth']) for player in player_search.to_dict(orient='records')]

        players_searched = fifa.load_players_using_search(search_list)
        empty_count = sum(1 for d in players_searched if not d)  # Empty dicts
        data_count = sum(1 for d in players_searched if d)  # Dicts with data

        print(f"Searched kicker {len(players_searched)} players. Empty count: {empty_count}, Data count: {data_count}")

        print(self.tf.info())  # Check if the IDs are present in the DataFrame
        print(self.kicker.info())  # Check if the IDs are present in the DataFrame
        # tf
        player_search_tf=self.tf[self.tf['id'].isin(ids_tf)][['last_name', 'dateOfBirth']]
        search_list_tf=[(player['last_name'], player['dateOfBirth']) for player in player_search_tf.to_dict(orient='records')]
        print(player_search_tf)

        players_searched_tf = fifa.load_players_using_search(search_list_tf)
        empty_count_tf = sum(1 for d in players_searched_tf if not d)  # Empty dicts
        data_count_tf = sum(1 for d in players_searched_tf if d)  # Dicts with data

        print(f"Searched tf {len(players_searched_tf)} players. Empty count: {empty_count_tf}, Data count: {data_count_tf}")

        # Search for the ID in the appropriate DataFrame and return the corresponding row
        # for player_id, source in missing_list:
        #     if source == 'kicker':
        #         row = self.kicker[self.kicker['id'] == player_id]
        #         ln=row['lastName']
        #         print(f"name> {ln.iloc[0]}")
        #         #print(f"From kicker: {row['lastName']} ::  {type(row['lastName'])}>>")
        #         print()
        #     elif source == 'tf':
        #         row = self.tf[self.tf['id'] == player_id]
        #         ln=row['last_name']
        #         print(f"name> {ln.iloc[0]}")
        #         #print(f"From tf: {row['last_name'].values} ::  {type(row)} >>")
            

        # ...process csv_data...
        # file contains birthdata and ids of players from different sources
        # open output JSON files from dedicated sources and search for names 
        # use names and birthdate to search for players in FIFA API
        


if __name__ == '__main__':
    unittest.main()

