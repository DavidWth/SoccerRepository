import unittest
from TransfermarktTeamsPerSeason import TransfermarktTeamsPerSeason

class TransfermarktTeamsPerSeasonTest(unittest.TestCase):
    def setUp(self):
        self.page = TransfermarktTeamsPerSeason("chrome")


    def tearDown(self):
        self.page.quit()

    def test_load_page_success(self):
        self.page.visit("https://www.transfermarkt.com")
        title = self.page.get_title()
        self.assertIn("Transfermarkt", title, f"Wrong page opened {title}")

    def test_get_teams_for_season(self):
        self.page.visit("https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2024")
        teams = self.page.get_teams_for_season()

        self.assertIsInstance(teams, (list), "Teams object is not a list!")
        self.assertEqual(len(teams), 18, "Teams list must be 18!")

if __name__ == '__main__':
    unittest.main()