from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class Player:
    id: str
    firstName: str
    lastName: str
    currentClub: str
    dateOfBirth: str  # Keep as string for JSON serialization
    height: int = 0
    weight: int = 0
    position: str = ''
    nations: List[str] = None
    age: int = 0
    geburtsname: str = ''
    namensverlauf: str = ''

    def calc_age(self) -> int:
        """Calculate the player's age based on the dateOfBirth."""
        birth_date = datetime.strptime(self.dateOfBirth, "%Y-%m-%d")
        today = datetime.today()
        return today.year - birth_date.year