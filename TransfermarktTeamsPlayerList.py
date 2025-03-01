from KickerPlayerProfile import BasePage
from selenium.webdriver.common.by import By


class TransfermarktTeamsPlayerList(BasePage):
    def get_team_players_list(self):
        return [team.get_attribute("href") for team in self.driver.find_elements(By.XPATH, "//table[@class='items']/tbody/descendant::td[@class='hauptlink']/child::a")]
