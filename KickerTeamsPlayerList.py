from KickerPlayerProfile import BasePage
from selenium.webdriver.common.by import By


class KickerTeamsPlayerList(BasePage):
    # def __init__(self, browser):
    #     super().__init__(browser)

    def get_team_players_list(self):
        #main_div=self.driver.find_element(*KickerPageLocators.teamPlayerList)
        return [team.get_attribute("href") for team in self.driver.find_elements(By.XPATH, "//main[@class='kick__data-grid__main ']//tr//a")]

class KickerPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    teamPlayerList = (By.CLASS_NAME, "kick__data-grid__main ")
