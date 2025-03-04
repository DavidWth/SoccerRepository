import unittest
from KickerController import KickerController
from TransfermarktController import TransfermarktController

class KickerRepostioryManagerTest(unittest.TestCase):
    def setUp(self):
        self.controller = KickerController()
        
    def tearDown(self):
        pass

    def ttest_load_teams_and_player_profiles_for_202425(self):
        player_profiles = self.controller.get_all_player_profiles_for_season()

        self.assertIsInstance(player_profiles, (list), "Player profiles is not a list!")

    def ttest_save_profiles_to_file(self):
        # Navigate to the Kicker Clubs Overview page and select the appropiate sesaon year (eg 2024/25) > (https://www.kicker.de/bundesliga/teams/2024-25)
        # The page pops up and shows all clubs of that season's Bundesliga competition
        # There we will get all club names and the corresponding links to their squads (club name: Bayern München, link to squad: https://www.kicker.de/fc-bayern-muenchen/kader/bundesliga/2024-25)
        # Now we open all links, starting with first one. The page is showing all players belonging to that club in that season.
        self.controller.save_profiles_to_file(self.controller.get_all_player_profiles_for_season())

class TransfermarktRepostioryManagerTest(unittest.TestCase):
    def setUp(self):
        self.controller = TransfermarktController()
        
    def tearDown(self):
        pass

    def ttest_load_teams_and_player_profiles_for_202425(self):
        player_profiles = self.controller.get_all_player_profiles_for_season()

        self.assertIsInstance(player_profiles, (list), "Player profiles is not a list!")

    def test_save_profiles_to_file(self):
        # Navigate to the Kicker Clubs Overview page and select the appropiate sesaon year (eg 2024/25) > (https://www.kicker.de/bundesliga/teams/2024-25)
        # The page pops up and shows all clubs of that season's Bundesliga competition
        # There we will get all club names and the corresponding links to their squads (club name: Bayern München, link to squad: https://www.kicker.de/fc-bayern-muenchen/kader/bundesliga/2024-25)
        # Now we open all links, starting with first one. The page is showing all players belonging to that club in that season.
        self.controller.save_profiles_to_file(self.controller.get_all_player_profiles_for_season())

if __name__ == '__main__':
    unittest.main()

