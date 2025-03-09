import unittest
from TransfermarktPlayerProfile import TransfermarktPlayerProfilePage
from selenium.webdriver.common.by import By

class SoccerRepositoryAnalyticsTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_page_success(self):
        self.page.visit("https://www.transfermarkt.com")
        title = self.page.get_title()

        h1 = self.page.find((By.XPATH, "//h1"))

        self.assertIn("Transfermarkt", title, f"Wrong page opened {title}")
        self.assertEqual(h1.get_attribute("innerText"), "Transfermarkt - The football portal with transfers, market values, rumours and statistics")

    def test_load_player_profile(self):
        for case in self.test_cases:
            with self.subTest(url=case["url"]):
                self.page.visit(case["url"])        

                title = self.page.get_title()
                player_profile = self.page.get_player_profile()
                self.assertIsInstance(player_profile, (dict), "Player profile is not a dict!")
    #             last_name = player_profile.get_last_name()
    #             first_name = player_profile.get_first_name()
    #             height = player_profile.get_height()
    #             weight = player_profile.get_weight()
    #             nations = player_profile.get_nations()
    #             bd = player_profile.get_birthdate()

    #             ed = case["expected_data"]
                self.assertIn("Alphonso Davies", title, f"Wrong page opened {title}")
                self.assertIsNotNone(player_profile, f"No player profile returned.")
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