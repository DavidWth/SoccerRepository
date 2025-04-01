import unittest
import sys,os

sys.path.append(os.path.abspath('../../src/'))

from data_sources import FifaAPIClient as fifa

class FifaAPIClientTest(unittest.TestCase):
    def setUp(self):
        self.namesAndDob = [("Donyell Malen", "1999-01-19"), ("Eljif Elmas", "1999-09-24"), ("Omar Marmoush", "1999-01-19"), ("Roland Sallai", "1999-01-19"), ("Jorge", "1974-01-19")]
        self.namesAndDobForMore = [
            ('Hermoso', '1995-06-18'), ('Buendia', '1996-12-25'), ('Buendia', '1997-12-25'), ('Sarco', '2006-01-06'), 
            ('Stepanov', '2007-08-10'), ('Tuta','1999-07-04'), ('Batshuayi', '1993-10-02'),
            ('Wahi', '2003-01-02'), ('Dal', '2006-01-26'), ('Da', '2006-01-26'),
        ]

    def tearDown(self):
        pass

    def test_load_players_using_search(self):
        players_searched = fifa.load_players_using_search(self.namesAndDob)

        empty_count = sum(1 for d in players_searched if not d)  # Empty dicts
        data_count = sum(1 for d in players_searched if d)  # Dicts with data

        self.assertIsInstance(players_searched, list)
        self.assertEqual(len(players_searched), 5)
        self.assertEqual(empty_count, 3)
        self.assertEqual(data_count, 2)

    def test_load_player_using_search_and_found_one_player(self):
        # Malen
        name = self.namesAndDob[0][0]
        bod = self.namesAndDob[0][1]
        
        player = fifa.load_player_using_search(name, bod)
        self.assertIsInstance(player, dict)
        self.assertEqual(player["lastName"], "Malen")
        self.assertEqual(player["team"], "Borussia Dortmund")
        self.assertEqual(player["position"], "Right Midfielder")
        self.assertEqual(player["nationality"], "Holland")
    
    def test_load_player_using_search_and_multiple_players_found(self):
        # Malen
        name = "erling"
        bod = "2000-07-21"
        
        player = fifa.load_player_using_search(name, bod)

        self.assertIsInstance(player, dict)
        self.assertEqual(player["lastName"], "Haaland")
        self.assertEqual(player["team"], "Manchester City")
        self.assertEqual(player["position"], "Striker")
        self.assertEqual(player["nationality"], "Norway")

    def test_load_players_using_search_and_multiple_players_found(self):
        players_searched = fifa.load_players_using_search(self.namesAndDobForMore)

        empty_count = sum(1 for d in players_searched if not d)  # Empty dicts
        data_count = sum(1 for d in players_searched if d)  # Dicts with data

        print(f"Searched {len(players_searched)} players. Empty count: {empty_count}, Data count: {data_count}")

        self.assertIsInstance(players_searched, list)
        self.assertEqual(len(players_searched), 5)
        self.assertEqual(empty_count, 3)
        self.assertEqual(data_count, 2)

    def test_load_player_using_search_and_multiple_players_found_no_dob(self):
        # Malen
        name = "aal"
        bod = "2100-07-21"
        
        player = fifa.load_player_using_search(name, bod)
        self.assertIsInstance(player, dict)
        self.assertEqual(player, {})
        

    def test_load_player_using_search_player_found_but_wrong_bod(self):
        # Omar
        name = self.namesAndDob[2][0]
        bod = self.namesAndDob[2][1]
        
        player = fifa.load_player_using_search(name, bod)
        self.assertIsInstance(player, dict)
        self.assertEqual(player, {})

    def test_load_player_using_search_no_player_found(self):
        # Jorge
        name = self.namesAndDob[4][0]
        bod = self.namesAndDob[4][1]
        
        player = fifa.load_player_using_search(name, bod)
        self.assertIsInstance(player, dict)
        self.assertEqual(player, {})

    # add tests for wrong url, missing values, typos, ...
if __name__ == '__main__':
    unittest.main()