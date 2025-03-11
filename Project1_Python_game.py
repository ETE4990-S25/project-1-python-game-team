import json

def setting_up():
#setting up the character based on player answers
    name = input("What is your name? ")
    classes = ["Wizard", "Knight", "Assassin"]
    valid_class = False 
    charcater_type = ""
    while not valid_class:
        charcater_type = input("What class would you like to be? (Wizard, Knight, Assassin) ")
        if charcater_type in classes:
            valid_class = True
        else:
            print("Invalid class, please try again.")
    return (name, charcater_type)
player_name, player_class = setting_up()
print(f"Welcome, {player_name}! You are a {player_class.capitalize()}.")


#Defualt values for the player
class Player:
    def __init__(self, name, character_type):
        self.name = name
        self.character_type = character_type
        self.level = 100
        self.inventory = []
        self.set_attributes()
        pass

    def set_attributes(self):
        #types of different characters
        if self.character_type == "Wizard":
            self.strength = 1
            self.magic = 10
            self.defense = 3
        elif self.character_type == "Knight":
            self.strength = 5
            self.magic = 2
            self.defense = 10
        elif self.character_type == "Assassin":
            self.strength = 10
            self.magic = 3
            self.defense = 1

    #displaying the stats
    def display_stats(self):
        print(f"Name: {self.name}")
        print(f"Class: {self.character_type}")
        print(f"Level: {self.level}")
        print(f"Strength: {self.strength}")
        print(f"Magic: {self.magic}")
        print(f"Defense: {self.defense}")
        print(f"Inventory: {self.inventory}")

    #i dont know if we need this but this is from copilot
    def save(self, filename="player_data.json"):
        """Save player data to a JSON file."""
        data = {
            "name": self.name,
            "character_type": self.character_type,
            "level": self.level,
            "health": self.health,
            "strength": self.strength,
            "magic": self.magic,
            "defense": self.defense,
            "inventory": self.inventory
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Player data saved to {filename}")

    @classmethod
    def load(cls, filename="player_data.json"):
        """Load player data from a JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                player = cls(data["name"], data["character_type"])
                player.level = data["level"]
                player.health = data["health"]
                player.strength = data["strength"]
                player.magic = data["magic"]
                player.defense = data["defense"]
                player.inventory = data["inventory"]
                return player
        except FileNotFoundError:
            print("No save file found.")
            return None