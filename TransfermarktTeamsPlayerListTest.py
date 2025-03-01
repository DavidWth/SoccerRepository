import unittest
from TransfermarktTeamsPlayerList import TransfermarktTeamsPlayerList

class TransfermarktTeamsPlayerListTest(unittest.TestCase):
    def setUp(self):
        self.page = TransfermarktTeamsPlayerList("chrome")


    def tearDown(self):
        self.page.quit()

    def test_load_page_success(self):
        self.page.visit("https://www.transfermarkt.com")
        title = self.page.get_title()
        self.assertIn("Football transfers", title, f"Wrong page opened {title}")

    def test_get_player_list(self):
        self.page.visit("https://www.transfermarkt.com/bayern-munich/kader/verein/27/plus/0/galerie/0?saison_id=2024")

        title = self.page.get_title()
        self.assertIn("Bayern Munich", title, f"Wrong page opened {title}")

    def test_get_team_players_list(self):
        self.page.visit("https://www.transfermarkt.com/bayern-munich/kader/verein/27/plus/0/galerie/0?saison_id=2024")
        players = self.page.get_team_players_list()
        print(players)
        self.assertIsInstance(players, (list), "Players object is not a list!")
        self.assertEqual(len(players), 26, "Players list must be 30!")

if __name__ == '__main__':
    unittest.main()