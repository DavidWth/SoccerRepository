from KickerPlayerProfile import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import asdict
from src.dataclasses.Player import Player
import re


class TransfermarktPlayerProfilePage(BasePage):
    def get_player_profile(self):
        name = PlayerName(self.driver.find_element(By.CLASS_NAME, "data-header__headline-wrapper"))
        data = PlayerData(self.driver.find_element(By.XPATH, "//DIV[@class='large-6 large-pull-6 columns print spielerdatenundfakten']"))
        mv = PlayerMarketValue(self.driver)

        result = {}
        name_dict = name.get_name()
        data_dict = data.get_player()
        mv_dict = mv.get_data()
        result  = {**name_dict, **data_dict, **mv_dict}

        print(result)
        return result

class BasePageElement:
    def __init__(self, element):
        self.element = element

class PlayerName(BasePageElement):
    def __init__(self, element):
        super().__init__(element)
        self.__load_data(element)
                 
    def __load_data(self, element):
        self.data = {}
        self.data["id"] = element.get_attribute('baseURI').split('/')[-1]
        self.data["slug"] = element.get_attribute('baseURI').split('/')[3]
        self.data["last_name"] = element.find_element(By.XPATH, "strong").text.strip()
        self.data["first_name"] = element.text.replace(self.data["last_name"], "").partition(' ')[2].strip()
        return self.data
    
    def get_name(self):
        return self.data
    
class PlayerProfile(BasePageElement):
    def __init__(self, element):
        super().__init__(element)
        self.__load_data(element)

    def __load_data(self, element):
        data = {}
        
class PlayerData(BasePageElement):
    # Dictionary mapping original keys to new keys
    key_map = {
        "Name in home country:": "nativeName",
        "Date of birth/Age:": "dateOfBirth",
        "Place of birth:": "placeOfBirth",
        "Height:": "height",
        "Citizenship:": "citizenship",
        "Position:": "position",
        "Foot:": "foot",
        "Current club:": "currentClub",
        "Joined:": "joined",
        "Contract expires:": "expires",
        "Outfitter:": "Outfitter"
    }

    def __init__(self, element):
        super().__init__(element)
        self.__load_data(element)

    def __load_data(self, element):        
        # Initialize transformed dictionary
        self.transformed = {}

        kv_pairs = element.find_elements(By.XPATH, "descendant::span[contains(@class, 'info-table__content')]")
        values = [value.get_attribute("innerText") for value in kv_pairs]
        result = list(zip(values[::2], values[1::2]))

        for key, value in result:
            if key not in PlayerData.key_map or not value.strip():  # Ignore empty values and unmapped keys
                continue
    
            new_key = PlayerData.key_map[key]
            # Special processing
            if new_key == "dateOfBirth":
                value = value.split(" (")[0]  # Remove age in parentheses
            elif new_key == "placeOfBirth":
                value = value.strip()  # Remove extra spaces
            elif new_key == "height":
                value = int(re.sub(r"[^\d]", "", value))  # Extract numeric part only
            elif new_key == "citizenship":
                value = [x.strip() for x in value.split("\n") if x.strip()]  # Split and clean up citizenships

            self.transformed[new_key] = value
        print(self.transformed)
        #self.player = Player(**data)
        #print(json.dumps(asdict(self.player), indent=4, ensure_ascii=False))

    def get_player(self):
        return self.transformed
    
 #   def __str__(self):
 #       return f'fn:{self.first_name} ln:{self.self.last_name} h:{self.height} cm w:{self.weight} kg bd: {self.birthdate} n:{self.nations}'

class PlayerMarketValue(BasePageElement):
    def __init__(self, element):
        super().__init__(element)
        self.__load_data(element)
                 
    def __load_data(self, element):
        self.data = {}

        try:
            iframe = WebDriverWait(element, 2).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='Iframe title']"))
            )
        except:
            print("iFrame timeout.")
            iframe = False
        finally:
            print("Frame focused.")

            if iframe:
                b=element.find_element(By.XPATH, "//button[@title='Accept & continue']")
                b.click()

        element.execute_script("window.scrollBy(0,1000)")

        current = max = 0
        try:
            current = WebDriverWait(element, 4).until(
                EC.visibility_of_element_located((By.XPATH, "//DIV[@class='current-value svelte-gfmgwx']"))
            )

            max = WebDriverWait(element, 4).until(
                EC.visibility_of_element_located((By.XPATH, "//DIV[@class='max-value svelte-gfmgwx']"))
        )
        except:
            print("MV timeout.")
        finally:
            print("MV focused.")

        c = {}
        if current and max:
            print(f"{current.get_attribute('innerText')} :: {max.get_attribute('innerText')}")
            c["current"] = self._convert_money(current.get_attribute('innerText'))
            c["highest"] = self._convert_money(max.get_attribute('innerText'))
        else:
            c["current"] = 0.0
            c["highest"] = 0.0
        self.data["marketValue"] = c

        return self.data
    
    def get_data(self):
        return self.data

    def _convert_money(self, money_str):
        money_str = money_str.replace("€", "").lower().strip()  # Remove € symbol and normalize
        if "m" in money_str:
            return float(money_str.replace("m", "")) * 1_000_000  # Convert millions
        elif "k" in money_str:
            return float(money_str.replace("k", "")) * 1_000  # Convert thousands
        return float(money_str)  # If no suffix, return as is

class TransfermarktPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    playerDataDiv = (By.CLASS_NAME, "large-6 large-pull-6 columns print spielerdatenundfakten")
    firstNameDiv = (By.CSS_SELECTOR, ".kick__vita__header__person-name-medium-h1 span")
    lastNameDiv = (By.CSS_SELECTOR, ".kick__vita__header__person-name-medium-h1")
    nationsDv = (By.CLASS_NAME, "kick__vita__header__person-detail-kvpair--nation")
    playerInfoDiv = (By.CLASS_NAME, "kick__vita__header__person-detail-kvpair-info")
    teamPlayerList = (By.CLASS_NAME, "//main[@class='kick__data-grid__main ")
    MAIN_NAME_DIV = (By.CLASS_NAME, "data-header__headline-wrapper")
    PLAYER_DATA_DIV = (By.CLASS_NAME, "large-6 large-pull-6 columns print spielerdatenundfakten")
