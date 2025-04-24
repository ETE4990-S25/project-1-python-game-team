# Imports moved to top as per feedback to avoid duplication
import json
import random  #comment: moved import to the top with others to avoid duplication

try:
    with open('ItemData.json') as f:
        items = json.load(f)
    # Added consistency check for item structure
    if not all("name" in item for lst in items.values() for item in lst):  #comment: added structure validation for 'name' field in items
        print("Warning: Some items in the JSON may not have a 'name' field.")  #comment: validation for missing 'name' field in items
except FileNotFoundError:
    print("Json file not found")
    items = {}  #comment: aligned items = {} with the print line for better formatting

def setting_up():
    # setting up the character based on player answers
    name = input("What is your name? ")
    classes = ["wizard", "knight", "assassin"]  #comment: converted class names to lowercase for more forgiving input matching
    valid_class = False
    character_type = ''  #comment: corrected spelling and cleaned up initialization of character_type
    while not valid_class:
        character_type = input("What class would you like to be? (Wizard, Knight, Assassin) ").lower().strip()  #comment: made input lowercase and stripped spaces
        if character_type in classes:
            valid_class = True
        else:
            print("Invalid class, please try again.")
    return (name, character_type)

player_name, player_class = setting_up()
print(f"Welcome, {player_name}! You are a {player_class.capitalize()}.")

# Player class with corrected capitalization and indentation
class Player:  #comment: capitalized class name to follow standard naming conventions (PEP 8)
    def __init__(self, name, character_type):
        self.name = name
        self.character_type = character_type
        self.level = 100
        self.inventory = []
        self.set_attributes()
        self.health = 100

    def set_attributes(self):
        # Types of different characters
        if self.character_type == "wizard":
            self.strength = 5
            self.magic = 10
            self.defense = 3
        elif self.character_type == "knight":
            self.strength = 10
            self.magic = 2
            self.defense = 10
        elif self.character_type == "assassin":
            self.strength = 100
            self.magic = 3
            self.defense = 1

    # Displaying the stats
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

    def view_inventory(self):
        print("Inventory: ")
        for item in self.inventory:
            print(f"- {item}")

# Enemy class with corrected capitalization and indentation
class Enemy:  #comment: capitalized class name to follow standard naming conventions (PEP 8)
    def __init__(self, name, strength, magic, defense):
        self.name = name
        self.strength = strength
        self.magic = magic
        self.defense = defense
        self.health = 10

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

# Enemy instance with chance of appearance
enemy_types = [
    (Enemy("Goblin", 5, 5, 2), 0.5),  # 50% chance
    (Enemy("mega goblin", 20, 15, 10), 0.3),  # 30% chance
    (Enemy("giga goblin", 30, 20, 5), 0.2)  # 20% chance
]

# Choosing the enemy
def choose_enemy():
    return random.choices([enemy[0] for enemy in enemy_types], weights=[enemy[1] for enemy in enemy_types])[0]

# Battle function
def battle(player, enemy):
    print(f"A wild {enemy.name} appears!")
    battle_active = True

    while battle_active:
        print("\nYour Turn (Type the number with the corresponding actions):")
        print("1. Attack")
        print("2. Heal")
        print("3. Run")
        choice = input("Choose an action: ")

        player_turn = True
        enemy_turn = False
        battle_end = False

        if choice == "1":
            damage = max(player.strength - enemy.defense, 1)
            enemy.take_damage(damage)
            print(f"You attacked {enemy.name} for {damage} damage!")
            if enemy.health <= 0:
                battle_end = True
            else:
                enemy_turn = True
        elif choice == "2":
            heal_items = [item for item in player.inventory if item.category in ["Healing", "Food"]]
            if heal_items:
                print("Choose an item to heal:")
                for idx, item in enumerate(heal_items, start=1):
                    print(f"{idx}. {item.name}")
                item_choice = int(input("Select an item: ")) - 1
                if 0 <= item_choice < len(heal_items):
                    chosen_item = heal_items[item_choice]
                    player.health += 10  # Adjust healing value as necessary
                    player.inventory.remove(chosen_item)
                    print(f"You used {chosen_item.name} and healed for 10 HP!")
                else:
                    print("Invalid choice, turn skipped!")
            else:
                print("You have no healing items!")
            enemy_turn = True
        elif choice == "3":
            print("You ran away!")
            battle_active = False
        else:
            print("Invalid choice, turn skipped!")
            enemy_turn = True

        if battle_end:
            print(f"You defeated {enemy.name}!")
            player.gain_exp(10)
            receive_loot(player)
            battle_active = False
            continue

        if enemy_turn:
            enemy_damage = max(enemy.strength - player.defense, 1)
            player.health -= enemy_damage
            print(f"{enemy.name} attacked you for {enemy_damage} damage!")
            if player.health <= 0:
                print("You were defeated...")
                print("Game over.")
                exit()

def gain_exp(self, amount):
    self.level += amount // 10  # Increase level every 10 XP
    self.strength += amount // 200  # Increase strength gradually
    self.magic += amount // 255  # Increase magic
    self.defense += amount // 300  # Increase defense
    print(f"You gained {amount} XP! Level: {self.level}, Strength: {self.strength}, Magic: {self.magic}, Defense: {self.defense}")

Player.gain_exp = gain_exp

# Receive random loot
def receive_loot(player):
    loot_received = False  # Flag to check if loot is given
    if items:  # Ensure items data is available
        category = random.choice(list(items.keys()))  # Pick a random category
        item = random.choice(items[category])  # Pick a random item

        loot_received = "name" in item  # Check if item has a name

        if loot_received:
            player.inventory.append(item["name"])
            print(f"You received a {item['name']}!")

    if not loot_received:
        print("No loot received.")  # Fallback message if loot is empty or incorrect

# Inventory and game loop (lambda functions provided by copilot)
# Initialize player instance
player_instance = Player("Hero", "knight")  # You can customize name and class

# Inventory and game loop (lambda functions provided by copilot, now corrected)
def save_game():
    player_instance.save()
    "save": lambda _: save_game(),

commands = {
    "view": lambda _: player_instance.view_inventory(),
    "save": lambda _: (player_instance.save(), print("Game saved. You can now enter battle.")),
    "battle": lambda _: battle(player_instance, choose_enemy()),
    "exit": lambda _: exit()
}

# Main game loop
while True:
    command_input = input("Enter a command (add, view, save, battle, exit): ").split()
    if not command_input:
        continue
    command = command_input[0].lower()
    args = command_input[1:]
    commands.get(command, lambda _: print("Incorrect command."))(args)