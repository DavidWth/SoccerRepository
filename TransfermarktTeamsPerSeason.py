from KickerPlayerProfile import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TransfermarktTeamsPerSeason(BasePage):
    def get_teams_for_season(self, season="2024/25"):
        rows = self.driver.find_elements(By.XPATH, "//div[@class='responsive-table']/descendant::table[@class='items']/tbody/descendant::td[@class='hauptlink no-border-links']/descendant::a")
        return [row.get_attribute("href") for row in rows if "verein" in row.get_attribute("href")]