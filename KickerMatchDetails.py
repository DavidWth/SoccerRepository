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

class KickerMatchDetailsPage(BasePage):
    # def __init__(self, browser):
    #     super().__init__(browser)

    def get_goal_events(self):
        return GoalEvents(self.driver.find_element(*KickerPageLocators.matchEvents))

class BasePageElement:
    def __init__(self, element):
        self.element = element

class GoalEvents(BasePageElement):
    def __init__(self, element):
        super().__init__(element)
        self.__load_data(element)
        # self.__load_data_dc(element)

    def get_last_name(self):
        return self.lastName
        
    def get_first_name(self):
        return self.firstName
    
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
        goals_elem= element.find_elements(*KickerPageLocators.goals)

        print(f"Found {len(goals_elem)} goals")

        goals=[]
        for goal_elem in goals_elem:
            goal_events = goal_elem.find_elements(*KickerPageLocators.children)
            player_id = goal_elem.find_element(By.XPATH, ".//a[@href]").get_attribute('href').split('/')[3]
            print(f"Player ID: {player_id}")
            goal=[]
            goal.append(player_id)
            for e in goal_events:
                # remove whitespace and new line characters from e
                goal.append(e.text.strip())

            goals.append(goal)    
        print(f"Goal> {self._parse_goal_events(goals)}")

    def __load_data_dc(self, element):
        data = {}
        
        data["id"] = element.get_attribute('baseURI').split('/')[3]
        data["lastName"] = self.__remove_parentheses(self.element.find_element(*KickerPageLocators.lastNameDiv).text.replace(self.get_first_name(), ""))
        data["firstName"] = self.__remove_parentheses(self.element.find_element(*KickerPageLocators.firstNameDiv).text)
        data["currentClub"] = self.element.find_element(*KickerPageLocators.currentClub).text

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
                    data["dateOfBirth"] = datetime.strptime(value.split()[0], "%d.%m.%Y").date().strftime("%Y-%m-%d")
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
    
    def _parse_goal_events(self, data_lists):
        print(data_lists)
        result = []

        for entry in data_lists:
            # Unpack list safely
            player_id, scorer_info, minute, score_raw, alt_minute, alt_info = entry

            # Determine where scoring info is
            info = scorer_info if scorer_info else alt_info
            scoring_minute = minute if minute else alt_minute
            score = score_raw.replace('\n', '').replace(':', ':')

            # Extract name, penalty, action, assist
            lines = info.split('\n')
            name_line = lines[0] if lines else ''
            is_penalty = '(Elfmeter)' in name_line

            # Get name (remove (Elfmeter) if exists)
            name = name_line.replace('(Elfmeter)', '').strip()

            # Action and assist (if exists)
            action = lines[1].split(',')[0].strip() if len(lines) > 1 else ''
            assist = lines[1].split(',')[1].strip() if len(lines) > 1 and ',' in lines[1] else ''

            result.append({
                "player_id": player_id,
                "name": name,
                "is_penalty": is_penalty,
                "action": action,
                "scoring_minute": scoring_minute,
                "assist": assist,
                "score": score
            })

        return result
    
    def __str__(self):
        return f'fn:{self.firstName} ln:{self.self.lastName} h:{self.height} cm w:{self.weight} kg bd: {self.birthdate} n:{self.nations}'
    
    class LineUp(BasePageElement):
        def __init__(self, element):
            super().__init__(element)
            self.__load_data(element)
            # self.__load_data_dc(element)

        def get_last_name(self):
            return self.lastName
            
        def get_first_name(self):
            return self.firstName
        
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
            goals_elem= element.find_elements(*KickerPageLocators.goals)

            print(f"Found {len(goals_elem)} goals")

            goals=[]
            for goal_elem in goals_elem:
                goal_events = goal_elem.find_elements(*KickerPageLocators.children)
                player_id = goal_elem.find_element(By.XPATH, ".//a[@href]").get_attribute('href').split('/')[3]
                print(f"Player ID: {player_id}")
                goal=[]
                goal.append(player_id)
                for e in goal_events:
                    # remove whitespace and new line characters from e
                    goal.append(e.text.strip())

                goals.append(goal)    
            print(f"Goal> {self._parse_goal_events(goals)}")

        def __load_data_dc(self, element):
            data = {}
            
            data["id"] = element.get_attribute('baseURI').split('/')[3]
            data["lastName"] = self.__remove_parentheses(self.element.find_element(*KickerPageLocators.lastNameDiv).text.replace(self.get_first_name(), ""))
            data["firstName"] = self.__remove_parentheses(self.element.find_element(*KickerPageLocators.firstNameDiv).text)
            data["currentClub"] = self.element.find_element(*KickerPageLocators.currentClub).text

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
                        data["dateOfBirth"] = datetime.strptime(value.split()[0], "%d.%m.%Y").date().strftime("%Y-%m-%d")
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
        
        def _parse_goal_events(self, data_lists):
            print(data_lists)
            result = []

            for entry in data_lists:
                # Unpack list safely
                player_id, scorer_info, minute, score_raw, alt_minute, alt_info = entry

                # Determine where scoring info is
                info = scorer_info if scorer_info else alt_info
                scoring_minute = minute if minute else alt_minute
                score = score_raw.replace('\n', '').replace(':', ':')

                # Extract name, penalty, action, assist
                lines = info.split('\n')
                name_line = lines[0] if lines else ''
                is_penalty = '(Elfmeter)' in name_line

                # Get name (remove (Elfmeter) if exists)
                name = name_line.replace('(Elfmeter)', '').strip()

                # Action and assist (if exists)
                action = lines[1].split(',')[0].strip() if len(lines) > 1 else ''
                assist = lines[1].split(',')[1].strip() if len(lines) > 1 and ',' in lines[1] else ''

                result.append({
                    "player_id": player_id,
                    "name": name,
                    "is_penalty": is_penalty,
                    "action": action,
                    "scoring_minute": scoring_minute,
                    "assist": assist,
                    "score": score
                })

            return result
        
        def __str__(self):
            return f'fn:{self.firstName} ln:{self.self.lastName} h:{self.height} cm w:{self.weight} kg bd: {self.birthdate} n:{self.nations}'
    
class KickerPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    # playerProfileDiv = (By.CLASS_NAME, "kick__vita__header__person-detail")
    # firstNameDiv = (By.CSS_SELECTOR, ".kick__vita__header__person-name-medium-h1 span")
    # lastNameDiv = (By.CSS_SELECTOR, ".kick__vita__header__person-name-medium-h1")
    # nationsDv = (By.CLASS_NAME, "kick__vita__header__person-detail-kvpair--nation")
    # playerInfoDiv = (By.CLASS_NAME, "kick__vita__header__person-detail-kvpair-info")
    # teamPlayerList = (By.CLASS_NAME, "//main[@class='kick__data-grid__main ")
    # currentClub = (By.XPATH, "//div[@class='kick__vita__header__team-info']/descendant::a")
    matchEvents=(By.XPATH, "//div[@class='kick__card ']/div[@class='kick__site-padding']")
    goals=(By.XPATH, "//div[@class='kick__goals kick__goals--ingame ']/child::div")
    children=((By.XPATH, "./*"))
    href=(By.XPATH, ".//a[@href]")