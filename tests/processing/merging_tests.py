import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src'))

from processing import data_merging

import pandas as pd

class MergingTests(unittest.TestCase):
    def setUp(self):
        # Sample DataFrame
        self.df1 = pd.DataFrame({
            "firstName": ["Florian", "Harry", "Jeremie"],
            "lastName": ["Wirtz", "Kane", "Frimpong"],
            "team": ["Leverkusen", "Bayern Munich", "Leverkusen"],
            "normalized_name": ["florian_wirtz", "harry_kane", "jeremie_frimpong"]
        })
        self.df2 = pd.DataFrame({
            "lastName": ["Wirtz", "Kane", "Müller", "Frimpong"],
            "age": [22, 31, 33, 27],
            "team": ["Leverkusen", "Bayern Munich", "Bayern Munich", "Leverkusen"],
            "normalized_name": ["florian_wirtz", "harry_kane", "thomas_muller", "jeremie_frimpong"]
        })

        self.names = [("","",True)]

    def tearDown(self):
        pass

    def test_merge_two_data_frames_which_are_same(self):
        merge_result = data_merging.merge_dataframes(self.df2, self.df2, ["normalized_name"])
        df_merged = merge_result["merged_df"]

        self.assertIsInstance(merge_result, dict)
        self.assertIsInstance(df_merged, pd.DataFrame)
        self.assertEqual(merge_result["matched"], 4)
        self.assertEqual(merge_result["unmatched"], 0)

    def test_merge_two_data_frames(self):
        merge_result = data_merging.merge_dataframes(self.df1, self.df2, ["normalized_name"])
        df_merged = merge_result["merged_df"]

        self.assertIsInstance(merge_result, dict)
        self.assertIsInstance(df_merged, pd.DataFrame)
        self.assertEqual(merge_result["matched"], 3)
        self.assertEqual(merge_result["unmatched"], 1)

    def test_merge_data_frames_with_wrong_keys(self):
        with self.assertRaises(KeyError):
            df_merged = data_merging.merge_dataframes(self.df1, self.df2, ["lastName", "not_existing"])

    def test_is_similar_names_with_one_empty_string(self):
        is_similar = data_merging.is_similar("d","")

        self.assertTrue(is_similar)

    def test_is_similar_names_with_different_names(self):
        is_similar = data_merging.is_similar("d","")

        self.assertTrue(is_similar)
