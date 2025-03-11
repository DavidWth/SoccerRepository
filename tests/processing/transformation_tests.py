import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src'))

from processing import transformation

import pandas as pd

class TransformationTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame([['eric-ebimbe', 'Eric Junior', 'Dina Ebimbe', 'Eintracht Frankfurt', 183],
                   ['oscar-hoejlund', 'Oscar', 'Höjlund', 'Eintracht Frankfurt', 179],
                   ['hyunseok-hong', 'Hyunseok', 'Hong', '1. FSV Mainz 05', 173],
                   ['xavi-simons', '', 'Xavi', 'RB Leipzig', 175]])
        self.df.columns = ['id', 'firstname', 'lastname', 'club', 'height']

    def tearDown(self):
        pass

    def test_drop_column_from_df(self):
        columns_size = len(self.df.columns)
        columns_to_drop=["club"]
        df_updated = transformation.drop_columns_from_dataframe(self.df, columns_to_drop)
        columns_size_updated = len(df_updated.columns)

        self.assertIsInstance(self.df, pd.DataFrame)
        self.assertGreater(columns_size, columns_size_updated)

    def test_drop_column_from_df_with_non_existing_column(self):
        columns_to_drop= ["not_existing"]
        df_updated = transformation.drop_columns_from_dataframe(self.df, columns_to_drop)
        
        self.assertIsInstance(self.df, pd.DataFrame)
        self.assertEqual(len(self.df.columns), len(df_updated.columns))
        self.assertListEqual(self.df.columns.values.tolist(), df_updated.columns.values.tolist())

    def test_drop_column_from_df_with_mix(self):
        columns_to_drop= ["not_existing", "club"]
        df_updated = transformation.drop_columns_from_dataframe(self.df, columns_to_drop)
        
        self.assertIsInstance(self.df, pd.DataFrame)
        self.assertEqual(len(self.df.columns), len(df_updated.columns))

    # Analyse the amount of values beloning to a specific attribute
    # 
    def remove_players_from_wrong_competition(data:pd.DataFrame, key:str):
        # Count occurrences of each club
        club_counts = data[key].value_counts()
        clubs_filtered=club_counts[club_counts<5].index.tolist()
        data_filtered = data[~data[key].isin(clubs_filtered)]
        print(f"From {len(data)} are {len(data_filtered)} left > {len(data)-len(data_filtered)} removed.")
        return data_filtered