from KickerPlayerProfile import BasePage
from selenium.webdriver.common.by import By


class KickerTeamsPerSeason(BasePage):
    # def __init__(self, browser):
    #     super().__init__(browser)

    def get_teams_for_season(self, season="2024/25"):
        #main_div=self.driver.find_element(*KickerPageLocators.teamPlayerList)
        rows = self.driver.find_elements(By.XPATH, "//main[@class='kick__data-grid__main ']//tr")
 
        return [row.find_element(By.XPATH, "td//a").get_attribute("href") for row in rows]

class KickerPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    teamPlayerList = (By.CLASS_NAME, "kick__data-grid__main ")
