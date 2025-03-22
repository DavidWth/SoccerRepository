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

        self.similar_names = [
            ("eric_junior_dina_ebimbe","junior_dina_ebimbe",True),
            ("","Simons",False),
            ("Östigaard","Østigård",False),     
            ("Leonardo", "Leo", True),
            ("leonardo_scienza", "leo_scienza", False),
        ]

        self.players = {"lastName_x":{"0":"Wirtz","1":"Kane","2":"Frimpong","3":"Muller"},
                        "age_x":{"0":22,"1":31,"2":27,"3":33},
                        "team_x":{"0":"Leverkusen","1":"Bayern Munich","2":"Leverkusen","3":"Bayern Munich"},
                        "normalized_name":{"0":"florian_wirtz","1":"harry_kane","2":"jeremie_frimpong","3":"thomas_muller"},
                        "lastName_y":{"0":"Wirtz","1":"Kane","2":"Frimpong","3":"Muller"},
                        "age_y":{"0":22,"1":31,"2":27,"3":33},
                        "team_y":{"0":"Leverkusen","1":"Bayern Munich","2":"Leverkusen","3":"Bayern Munich"},
                        "_merge":{"0":"both","1":"both","2":"both","3":"both"}}
        
        self.players_for_similar_entries = pd.read_json("D:\\DevOps\\python_work\\venv\\demoenv\\resources\\testdata_players_names_and_dob.json")
        

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
        for name1, name2, expected in self.similar_names:
            with self.subTest(first_name=name1, last_name=name2):
                is_similar = data_merging.is_similar(name1, name2)
                print(f"{name1} :: {name2} :: {is_similar}")
                self.assertEqual(is_similar, expected)

    def test_merge_on_additional_attributes(self):
        print(f"merged> {pd.DataFrame(self.players)}")
        merged_df = data_merging.merge_similar_entries(self.players_for_similar_entries)

        print(f"merged> {merged_df}")

    def test_merge_on_additional_attributes_with_groups_gt_2(self):
        print(f"merged> {pd.DataFrame(self.players)}")
        merged_df = data_merging.merge_similar_entries(self.players_for_similar_entries)

        print(f"merged> {merged_df}")

    