import unittest
from KickerMatchDetails import KickerMatchDetailsPage

class KickerMatchDetailsTest(unittest.TestCase):
    def setUp(self):
        self.page = KickerMatchDetailsPage("chrome")

        self.test_cases = [            
            {
                "url": "            https://www.kicker.de/manuel-neuer/spieler/bundesliga/2024-25/fc-bayern-muenchen",
                "expected_data": {"title": "Manuel Neuer", "last_name": "Neuer", "first_name": "Manuel", "height": 198, "weight": 90 
                                  , "nations": ["Deutschland"]}
            },
            {
                "url": "https://www.kicker.de/nick-woltemade/spieler/bundesliga/2024-25/vfb-stuttgart",
                "expected_data": {"title": "Nick Woltemade", "last_name": "Woltemade", "first_name": "Nick", "height": 198, "weight": 90 
                                  , "nations": ["Deutschland"]}
            },
            {
                "url": "https://www.kicker.de/julian-chabot/spieler/bundesliga/2024-25/vfb-stuttgart",
                "expected_data": {"title": "Julian Chabot", "last_name": "Chabot", "first_name": "Julian", "height": 195, "weight": 95 
                                  , "nations": ["Deutschland", "Frankreich"]}
            },
            {
                "url": "https://www.kicker.de/tiago-tomas/spieler/bundesliga/2024-25/vfl-wolfsburg",
                "expected_data": {"title": "Tiago Tomas", "last_name": "Tiago Tomas", "first_name": "", "height": 180, "weight": 78 
                                  , "nations": ["Portugal"]}
            },
        ]


    def tearDown(self):
        self.page.quit()

    def test_load_page_success(self):
        self.page.visit("https://www.kicker.de")
        title = self.page.get_title()
        self.assertIn("Sportnachrichten", title, f"Wrong page opened {title}")

    def test_load_all_goals(self):
        self.page.visit("https://www.kicker.de/frankfurt-gegen-leipzig-2024-bundesliga-4862266/schema")
        goal_events = self.page.get_goal_events()
        self.assertTrue(len(goal_events), 8, f"Wring number of goals {len(goal_events)}")

    # def test_load_player_profile(self):
    #     for case in self.test_cases:
    #         with self.subTest(url=case["url"]):
    #             self.page.visit(case["url"])        

    #             title = self.page.get_title()
    #             player_profile = self.page.get_player_profile()
    #             last_name = player_profile.get_last_name()
    #             first_name = player_profile.get_first_name()
    #             height = player_profile.get_height()
    #             weight = player_profile.get_weight()
    #             nations = player_profile.get_nations()
    #             bd = player_profile.get_birthdate()

    #             ed = case["expected_data"]
    #             self.assertIn(ed["title"], title, f"Wrong page opened {title}")
    #             self.assertIsNotNone(player_profile, f"No player profile returned.")
    #             self.assertIn(ed["last_name"], last_name, f"Wrong player name  {last_name}")
    #             self.assertIn(ed["first_name"], first_name, f"Wrong player name  {first_name}")
    #             self.assertIsInstance(height, (int, float), "Height is not a number!")
    #             self.assertIsInstance(weight, (int, float), "Weight is not a number!")
    #             self.assertIsInstance(nations, (list), "Nations is not a list!")
    #             #self.assertIsInstance(bd, (datetime), "Birth date is not a date!")
    #             self.assertEqual(ed["height"], height)
    #             self.assertEqual(ed["weight"], weight)
    #             self.assertEqual(len(ed["nations"]), len(nations))


if __name__ == '__main__':
    unittest.main()