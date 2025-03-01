from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime
import re, json
from dataclasses import asdict
from src.dataclasses.Player import Player

class BasePage(object):
    timeoutSec = 5

    def __init__(self, browser="chrome"):
        self.driver = webdriver.Chrome()
        #self.visit(url)
        #self.wait = WebDriverWait(self.driver, self.timeoutSec)

    def setTimeoutSec(self, timeoutSec):
        self.timeoutSec = timeoutSec

    def visit(self, url):
        print(f"Talking to {url} using {self.driver}")
        self.driver.get(url)

    def get_title(self):
        if self.driver:
            return self.driver.title
        else:
            return None
    
    def find(self, element):
        return self.driver.find_element(By.XPATH, "//h1")
    
    def quit(self):
        if self.driver:
            print("Shuting down" + self.driver.title)
            self.driver.quit()

class KickerPlayerProfilePage(BasePage):
    # def __init__(self, browser):
    #     super().__init__(browser)

    def get_player_profile(self):
        return PlayerProfile(self.driver.find_element(*KickerPageLocators.playerProfileDiv))

class BasePageElement:
    def __init__(self, element):
        self.element = element

class PlayerProfile(BasePageElement):
    def __init__(self, element):
        super().__init__(element)
        self.__load_data(element)
        self.__load_data_dc(element)

    def get_last_name(self):
        return self.last_name
        
    def get_first_name(self):
        return self.first_name
    
    def get_height(self):
        return self.height
    
    def get_weight(self):
        return self.weight
    
    def get_nations(self):
        return self.nations
    
    def get_birthdate(self):
        return self.birthdate

    def __remove_parentheses(self, value):
        return re.sub(r"\(.*?\)", "", value).strip()

    def __load_data(self, element):
        self.first_name = self.__remove_parentheses(self.element.find_element(*KickerPageLocators.firstNameDiv).text)
        self.last_name = self.__remove_parentheses(self.element.find_element(*KickerPageLocators.lastNameDiv).text.replace(self.first_name, ""))
 
        # Extract Key-Value Details
        data = {}
        kv_pairs = element.find_elements(*KickerPageLocators.playerInfoDiv)

        for kv in kv_pairs:
            spans = kv.find_elements(By.TAG_NAME, "span")
            if spans:
                key = spans[0].text.strip().replace(":", "")
                value = kv.text.replace(spans[0].text, "").strip()
                print(f"{key} {value}")
                # Convert height and weight to integers
                if key == "Größe":
                    self.height = int(value.replace(" cm", ""))
                elif key == "Gewicht":
                    self.weight = int(value.replace(" kg", ""))
                elif key == "Geboren":
                    self.birthdate = datetime.strptime(value.split()[0], "%d.%m.%Y").date()
                elif key.startswith("Nation"):
                    self.nations = [nation.text.strip() for nation in kv.find_elements(*KickerPageLocators.nationsDv)]

                    key = "Nation"
                
                data[key] = value

    def __load_data_dc(self, element):
        data = {}
        
        data["last_name"] = self.__remove_parentheses(self.element.find_element(*KickerPageLocators.lastNameDiv).text.replace(self.get_first_name(), ""))
        data["first_name"] = self.__remove_parentheses(self.element.find_element(*KickerPageLocators.firstNameDiv).text)
        data["id"] = element.get_attribute('baseURI').split('/')[3]

        # Extract Key-Value Details
        kv_pairs = element.find_elements(*KickerPageLocators.playerInfoDiv)

        for kv in kv_pairs:
            spans = kv.find_elements(By.TAG_NAME, "span")
            if spans:
                key = spans[0].text.strip().replace(":", "")
                value = kv.text.replace(spans[0].text, "").strip()
                print(f"{key} {value}")
                # Convert height and weight to integers
                if key == "Größe":
                    data["height"] = int(value.replace(" cm", ""))
                elif key == "Gewicht":
                    data["weight"] = int(value.replace(" kg", ""))
                elif key == "Geboren":
                    data["date_of_birth"] = datetime.strptime(value.split()[0], "%d.%m.%Y").date().strftime("%Y-%m-%d")
                    data["age"] = datetime.today().year - datetime.strptime(value.split()[0], "%d.%m.%Y").date().year
                elif key.startswith("Nation"):
                    data["nations"] = [nation.text.strip() for nation in kv.find_elements(*KickerPageLocators.nationsDv)]
                else:                
                    data[key.lower()] = value 
        
        print(f"Data> {data}")
        self.player = Player(**data)
        print(json.dumps(asdict(self.player), indent=4, ensure_ascii=False))

    def get_player(self):
        return self.player
    
    def __str__(self):
        return f'fn:{self.first_name} ln:{self.self.last_name} h:{self.height} cm w:{self.weight} kg bd: {self.birthdate} n:{self.nations}'
    
class KickerPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    playerProfileDiv = (By.CLASS_NAME, "kick__vita__header__person-detail")
    firstNameDiv = (By.CSS_SELECTOR, ".kick__vita__header__person-name-medium-h1 span")
    lastNameDiv = (By.CSS_SELECTOR, ".kick__vita__header__person-name-medium-h1")
    nationsDv = (By.CLASS_NAME, "kick__vita__header__person-detail-kvpair--nation")
    playerInfoDiv = (By.CLASS_NAME, "kick__vita__header__person-detail-kvpair-info")
    teamPlayerList = (By.CLASS_NAME, "//main[@class='kick__data-grid__main ")
