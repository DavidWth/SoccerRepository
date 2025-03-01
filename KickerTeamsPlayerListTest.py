import unittest
from KickerTeamsPlayerList import KickerTeamsPlayerList

class KickerTeamsPlayerListTest(unittest.TestCase):
    def setUp(self):
        self.page = KickerTeamsPlayerList("chrome")


    def tearDown(self):
        self.page.quit()

    def test_load_page_success(self):
        self.page.visit("https://www.kicker.de")
        title = self.page.get_title()
        self.assertIn("Sportnachrichten", title, f"Wrong page opened {title}")

    def test_get_player_list(self):
        self.page.visit("https://www.kicker.de/1-fc-union-berlin/kader/bundesliga/2024-25")

        title = self.page.get_title()
        self.assertIn("FC Union Berlin", title, f"Wrong page opened {title}")

    def test_get_team_players_list(self):
        self.page.visit("https://www.kicker.de/1-fc-union-berlin/kader/bundesliga/2024-25")
        players = self.page.get_team_players_list()

        self.assertIsInstance(players, (list), "Players object is not a list!")
        self.assertEqual(len(players), 30, "Players list must be 30!")

if __name__ == '__main__':
    unittest.main()