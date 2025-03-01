from KickerTeamsPerSeason import KickerTeamsPerSeason
from KickerTeamsPlayerList import KickerTeamsPlayerList
from KickerPlayerProfile import KickerPlayerProfilePage
import json
from dataclasses import asdict

class KickerController():
    def __init__(self):
        self.teams = KickerTeamsPerSeason()
        self.players = KickerTeamsPlayerList()
        self.player_profile = KickerPlayerProfilePage("chrome")
    
    def get_all_player_profiles_for_season(self):
        profiles = []
        
        self.teams.visit("https://www.kicker.de/bundesliga/teams/2024-25")
        teams = self.teams.get_teams_for_season("season")

        for url in teams[:1]:
            self.players.visit(url.replace("info", "kader"))
            players = self.players.get_team_players_list() 
            for player in players:
                self.player_profile.visit(player)
                profiles.append(self.player_profile.get_player_profile())

        self.teams.quit()
        self.players.quit()
        self.player_profile.quit()

        return profiles
    
    def save_profiles_to_file(self, profiles, file="player_profiles.json"):
        players = [asdict(profile.get_player()) for profile in profiles]
        with open('output_k.json', 'w', encoding="utf-8") as f:
            json.dump(players, f, indent=4, ensure_ascii=False)

                

    