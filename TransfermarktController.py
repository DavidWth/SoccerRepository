from TransfermarktTeamsPerSeason import TransfermarktTeamsPerSeason
from TransfermarktTeamsPlayerList import TransfermarktTeamsPlayerList
from TransfermarktPlayerProfile import TransfermarktPlayerProfilePage
import json
from dataclasses import asdict

class TransfermarktController():
    def __init__(self):
        self.teams = TransfermarktTeamsPerSeason()
        self.players = TransfermarktTeamsPlayerList()
        self.player_profile = TransfermarktPlayerProfilePage("chrome")
    
    def get_all_player_profiles_for_season(self):
        i=0
        
        print("Calling https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2024")
        self.teams.visit("https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2024")
        teams = self.teams.get_teams_for_season("season")

        for url in teams:
            profiles = []
            i=i+1

            self.players.visit(url)
            players = self.players.get_team_players_list() 
            print(players)
            for player in players:
                self.player_profile.visit(player)
                profiles.append(self.player_profile.get_player_profile())
            self.save_profiles_to_file(profiles, profiles[0]["currentClub"].replace(" ", "_"))

        self.teams.quit()
        self.players.quit()
        self.player_profile.quit()

        return profiles
    
    def save_profiles_to_file(self, profiles, file="player_profiles.json"):
        
        # if(not isinstance(profiles, list)):
        #     players = [asdict(profile.get_player()) for profile in profiles]
        #     with open('output_tf.json', 'w', encoding='utf-8') as f:
        #         json.dump(players, f, indent=4, ensure_ascii=False)
        # else:
        #     with open(f"output_tf_{file}.json", 'w', encoding='utf-8') as f:
        #         json.dump(profiles, f, indent=4, ensure_ascii=False)
                
        with open(f"output_tf_{file}.json", 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=4, ensure_ascii=False)

    