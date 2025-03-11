import unittest
import sys,os
from FifaAPIClient import *

sys.path.append(os.path.abspath('./src/'))

class FifaAPIClientTest(unittest.TestCase):
    def setUp(self):
        self.names = [("Donyell Malen", "1999-01-19"), ("Eljif Elmas", "1999-09-24"), ("Omar Marmoush", "1999-01-19"), ("Roland Sallai", "1999-01-19"), ("Jorge", "1974-01-19")]

    def tearDown(self):
        pass

    def test_load_players_using_search(self):
        players_found = load_players_using_search(self.names)

        empty_count = sum(1 for d in players_found if not d)  # Empty dicts
        data_count = sum(1 for d in players_found if d)  # Dicts with data

        self.assertIsInstance(players_found, list)
        self.assertEqual(len(players_found), 5)
        self.assertEqual(empty_count, 3)
        self.assertEqual(data_count, 2)

    def test_load_player_using_search_and_found_one_player(self):
        # Malen
        name = self.names[0][0]
        bod = self.names[0][1]
        
        player = load_player_using_search(name, bod)
        self.assertIsInstance(player, dict)
        self.assertEqual(player["lastName"], "Malen")
        self.assertEqual(player["team"], "Borussia Dortmund")
        self.assertEqual(player["position"], "Right Midfielder")
        self.assertEqual(player["nationality"], "Holland")
    

    def test_load_player_using_search_player_found_but_wrong_bod(self):
        # Omar
        name = self.names[2][0]
        bod = self.names[2][1]
        
        player = load_player_using_search(name, bod)
        self.assertIsInstance(player, dict)
        self.assertEqual(player, {})

    def test_load_player_using_search_no_player_found(self):
        # Jorge
        name = self.names[4][0]
        bod = self.names[4][1]
        
        player = load_player_using_search(name, bod)
        self.assertIsInstance(player, dict)
        self.assertEqual(player, {})

    # add tests for wrong url, missing values, typos, ...
if __name__ == '__main__':
    unittest.main()