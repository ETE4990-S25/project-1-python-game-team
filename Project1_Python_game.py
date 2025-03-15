import json

#inventory dataset import
import json

with open('ItemData.json') as f:
    items = json.load (f)

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


#Default values for the player
class Player:
    def __init__(self, name, character_type):
        self.name = name
        self.character_type = character_type
        self.level = 100
        self.inventory = []
        self.set_attributes()
        self.health = 100
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

def add_to_inventory(self, item_name):
    found = False
    for category, item_list in items.items():
        for item_data in item_list:
            if item_data.get("name") == item_name:
                self.inventory.append(item_name)
                print(f"{item_name} has been added to your inventory.")
                found = True
                break
        if found:
            break
    if not found:
        print(f"{item_name} not found.")

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

#creates player instance and displays stats
player = Player(player_name, player_class)
player.display_stats()

#inventory
while True:
    command = input("Enter a command (add, view, save, exit): ")
    command_parts = command.split()

    if command_parts[0].lower() == 'add':
        if len(command_parts) >1:
            item_to_add = " ".join(command_parts[1:])
            player.add_to_inventory(item_to_add)
            player.display_stats()
        else:
            print("Please provide an item name.")
    elif command_parts[0].lower() == 'view':
        player.view_inventory()
    elif command_parts[0].lower() == 'save':
        player.save()
        break
    elif command_parts[0].lower() == 'exit':
        break
    else:
        print("Incorrect command.")