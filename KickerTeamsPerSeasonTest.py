import unittest
from KickerTeamsPerSeason import KickerTeamsPerSeason

class KickerTeamsPerSeasonTest(unittest.TestCase):
    def setUp(self):
        self.page = KickerTeamsPerSeason("chrome")


    def tearDown(self):
        self.page.quit()

    def test_load_page_success(self):
        self.page.visit("https://www.kicker.de")
        title = self.page.get_title()
        self.assertIn("Sportnachrichten", title, f"Wrong page opened {title}")

    def test_get_teams_for_season(self):
        self.page.visit("https://www.kicker.de/bundesliga/teams/2024-25")
        teams = self.page.get_teams_for_season()
        print(teams)
        self.assertIsInstance(teams, (list), "Teams object is not a list!")
        self.assertEqual(len(teams), 18, "Teams list must be 18!")

if __name__ == '__main__':
    unittest.main()