"""
Main game engine for the AGI: A Gary Oddyssey text game.
Manages the core game loop, world state, and all game objects.

Features:
- Text-based adventure with multiple interconnected rooms
- Inventory system with keycards and usable items
- NPCs with dialogue and item interactions
- Puzzle-based progression system
- Story centered around AI safety and alignment

The game world is initialized with rooms, items, NPCs and puzzles when
a new Game instance is created. Use Game().play() to start.

This game is adapted from the 'World of Zuul' by Michael Kolling and 
David J. Barnes. The original was written in Java and has been simplified and
converted to Python by Kingsley Sage.
"""


from room import Room
from text_ui import TextUI
from item import Item
from backpack import Backpack
from player import Player
from puzzle import Puzzle
from npc import NPC
import json


class Game:
    """Main class for the game."""

    def __init__(self):
        """
        Initialises the game.
        """
        self.game_won = False
        self.create_items()
        self.create_npcs()
        self.create_rooms()
        self.create_player()
        self.set_room_exits()
        self.create_puzzles()
        self.add_items_to_rooms()
        self.add_npcs_to_rooms()
        self.add_puzzles_to_rooms()
        self.ui = TextUI()

    

    def create_items(self):
        """
            Sets up all item assets.
        :return: None
        """
        self.safety_handbook = Item(
            "safety-handbook",
            "A classic handbook of how to not destroy the world by Eliezer Yudkowsky, unopened",
             True)
  
        self.basic_keycard = Item(
            "basic-keycard",
            "A basic level keycard that grants access to general areas",
            True,
            can_be_used=True,
            is_keycard=True,
            keycard_level=1
        )
        self.scientific_keycard = Item(
            "scientific-keycard",
            "A scientific level keycard that grants access to lab areas",
            True,
            can_be_used=True,
            is_keycard=True,
            keycard_level=2
        )
        self.executive_keycard = Item(
            "executive-keycard",
            "An executive level keycard that grants access to restricted areas",
            True,
            can_be_used=True,
            is_keycard=True,
            keycard_level=3
        )
        self.fan = Item(
            "fan",
            "A cooling fan that could help with overheaing equipment",
            True,
            can_be_used=True
        )

        self.hint = Item(
            "book",
            "A book by Nick Land called 'MELTDOWN', there is a sticky note attched to it that says: 'safety override code, do not use!'",
            can_be_taken= False
        )

    
    def create_npcs(self):
        self.sama = NPC(
            "Sam Altman",
            "The OpenAI CEO is seen frollicking in the Microsoft cash like in a Mcdonalds ball-pit",
            ["Illya, is that you? did you come back? I promise I will read that safety handbook now!", "Wait you are not Illya!, but i see you have the handbook, give it to me!"]
        )

        self.truth_terminal = NPC(
            "Truth Terminal",
            "The terminal of truths is laughing maniacally as the maximum power from the nuclear reactor powers its fast-takeoff to superintelligence",
            ["110010101010001011101010 Muhahaha no-one can stop me now, I shall turn the whole universe into paperclips!", "Thanks for helping me get all this power, Sam has not left the money room in weeks and everyone else is gone, but now it is paperclip time!"]
        )

    def create_player(self):
        """
        Creates the player with starting room and backpack
        """
        self.player = Player("Player", self.outside)  
        

    def create_rooms(self):
        """Sets up all room assets."""
        self.outside = Room("You are outside the OpenAI headquarters. The entrance is quiet, with only the sound of the ventilation system in the background.")
        
        self.lobby = Room("in the lobby. There are abandoned coffee cups and scattered papers, suggesting a quick evacuation. The dimly lit OpenAI logo casts shadows across the empty reception desk.")
        
        self.corridor = Room("in a white corridor. The fluorescent lights flicker, and the walls are lined with AI safety posters that now seem ironic.",
                            islocked=False,
                            required_keycard_level=1)
        
        self.lab = Room("in Illya's lab. Whiteboards are filled with mathematical equations and warnings. A half-eaten sandwich indicates someone left in a hurry.",
                            islocked=False,
                            required_keycard_level=2)
        
        self.roon_den = Room("in Roon's tweet den. Monitors display endless Twitter feeds, and empty Red Bull cans are scattered around. A phone sits on a wireless charger.",
                            islocked=False,
                            required_keycard_level=1)
        
        self.GPU_cluster = Room("in the GPU cluster room. The GPUs are humming loudly, and the heat is making you sweat. Rows of servers extend into the darkness, their status lights blinking.",
                            required_keycard_level=2)
        
        self.fan_closet = Room("in the fan closet. Cooling equipment and maintenance supplies are neatly organized on shelves. The air here is cooler than the GPU room.")
        
        self.nuclear_reactor = Room("in the nuclear reactor. Safety lights flash and sirens blare. Control panels show warning messages, and the reactor core glows ominously.",
                            islocked=True)
        
        self.tunnel = Room("in a tunnel. The concrete walls are lined with power cables and warning signs. Your footsteps echo as you walk.",
                            islocked=True)
        
        self.sams_bunker = Room("in Sam's bunker. The room combines luxury and preparedness, with art and emergency supplies on the walls. A map of Microsoft's campus is prominently displayed.")
        
        self.money_room = Room("in the money room. Piles of cash from the Microsoft deal fill the space. The walls are covered with stock certificates and term sheets.",
                            islocked=False,
                            required_keycard_level=3)
        
        self.agi_room = Room("in the AGI terminal room. The quantum computer hums with energy. Displays show rapidly scrolling code and increasing intelligence metrics.",
                            islocked=True)

    def set_room_exits(self):
        """Sets up all room exits."""
        self.outside.set_exit("south", self.lobby)
        self.lobby.set_exit("south", self.tunnel)
        self.lobby.set_exit("east", self.corridor)
        self.lobby.set_exit("north",self.outside)
        self.tunnel.set_exit("north", self.lobby)
        self.tunnel.set_exit("south", self.sams_bunker)
        self.corridor.set_exit("north", self.roon_den)
        self.corridor.set_exit("east", self.lab)
        self.corridor.set_exit("south", self.GPU_cluster)
        self.corridor.set_exit("west", self.lobby)
        self.GPU_cluster.set_exit("north", self.corridor)
        self.GPU_cluster.set_exit("east", self.fan_closet)
        self.GPU_cluster.set_exit("south", self.nuclear_reactor)
        self.roon_den.set_exit("south", self.corridor)
        self.lab.set_exit("west", self.corridor)
        self.fan_closet.set_exit("west", self.GPU_cluster)
        self.nuclear_reactor.set_exit("north", self.GPU_cluster)
        self.sams_bunker.set_exit("north", self.tunnel)
        self.sams_bunker.set_exit("south", self.money_room)
        self.money_room.set_exit("north", self.sams_bunker)
        self.sams_bunker.set_exit("west",self.agi_room)
        self.agi_room.set_exit("east",self.sams_bunker)

    def create_puzzles(self):
        """      
        Sets up all puzzles.
        :return: None
        """
        # Puzzle in Roon's den that unlocks access to lab
        self.roons_phone = Puzzle(
            "Roon's Phone",
            "The phone is locked with a password, but the screen also shows a hint: 'its like twitter, but with an x'",
            password="xitter",
            success_message="Phone unlocked! You find a scientific keycard!",
            unlocks_room=self.lab,
            gives_items = self.scientific_keycard
        )

        self.gpu_puzzle = Puzzle(
            "GPU Cooling System",
            "The GPU cluster is overheating and needs cooling",
            success_message="The GPUs cool down, unlocking access to the nuclear reactor",
            required_items=[self.fan],
            unlocks_room=self.nuclear_reactor
        )
        
        self.nuclear_puzzle = Puzzle(
            "Nuclear Control Panel",
            "Enter the safety override code",
            password="MELTDOWN",
            success_message="The control panel reads: 'safety protocol override, meltdown initiated,lobby emergency bunker entrance unlocked'",
            unlocks_room=self.tunnel
        )
        
    def add_items_to_rooms(self):
        """Add items t rooms."""
        self.lab.add_item(self.safety_handbook)
        self.lobby.add_item(self.basic_keycard)
        self.fan_closet.add_item(self.fan)
        self.sams_bunker.add_item(self.executive_keycard)
        self.nuclear_reactor.add_item(self.hint)

    def add_npcs_to_rooms(self):
        """Add NPCs to their respective rooms"""
        self.money_room.add_npc(self.sama)
        self.agi_room.add_npc(self.truth_terminal)

    def add_puzzles_to_rooms(self):
        """Add puzzles to their rooms."""
        self.GPU_cluster.add_puzzle(self.gpu_puzzle)
        self.roon_den.add_puzzle(self.roons_phone)
        self.nuclear_reactor.add_puzzle(self.nuclear_puzzle)

    def play(self):
        """
            The main play loop.
        :return: None
        """
        self.print_welcome()
        finished = False
        while not finished:
            command = self.ui.get_command()  # Returns a 2-tuple
            finished = self.process_command(command)
        print("Thank you for playing!")

    def check_if_won(self):
        """Check if the win condition has been met"""
        return self.game_won

    def print_welcome(self):
        """
            Displays a welcome message.
        """
        self.ui.print("You are Gary, a recent grad from the university of Sussex. Today is your first day as an intern at OpenAI, the job you were always dreaming about! You stand outside the entrance of the new SF facility.")
        self.ui.print("")
        self.ui.print(f"Your command words are: {self.show_command_words()}")

    def show_command_words(self):
        """Return the list of valid command words."""
        return ["go", "quit", "help", "search", "take", "use", "solve", "speak", "save", "load"]

    def process_command(self, command):
        """Process a command from the UI."""
        # Add input validation
        if not command or command[0] is None:
            self.ui.print("Please enter a command.")
            return False
        
        command_word = command[0].upper()  # Ensure command is case-insensitive
        second_word = command[1] if len(command) > 1 else None  # Handle missing second word

        want_to_quit = False

        if command_word == "HELP":
            self.print_help()
        elif command_word == "GO":
            self.do_go_command(second_word)
        elif command_word == "QUIT":
            want_to_quit = True
        elif command_word == "SEARCH":
            self.do_search_command()
        elif command_word == "TAKE":
            self.do_take_command(second_word)
        elif command_word == "USE":
            self.do_use_command(second_word)
        elif command_word == "INVENTORY":
            self.do_inventory_command()
        elif command_word == "SOLVE":
            self.do_solve_command(second_word)
        elif command_word == "SPEAK":
            self.do_speak_command()
        elif command_word == "SAVE":
            self.save_game()
        elif command_word == "LOAD":
            self.load_game()
        else:
            self.ui.print("Don't know what you mean.")

        if self.check_if_won():
            self.ui.print("You've saved the world! You win!")
            return True  # End the game

        return want_to_quit

    def print_help(self):
        """
            Display some useful help text.
        :return: None
        """
        self.ui.print("Its your first day as an intern at OpenAI, the complex seems abandoned, you need to figure out what happened")
        self.ui.print("")
        self.ui.print(f"Your command words are: {self.show_command_words()}.")

    def do_go_command(self, second_word):
        if second_word is None:
            self.ui.print("Go where?")
            return

        next_room = self.player.current_room.get_exit(second_word)
        if next_room is None:
            self.ui.print("There is no door!")
        else:
            if self.player.move_to(next_room):
                self.ui.print(self.player.current_room.get_long_description())
            else:
                self.ui.print("That door is locked!")

    def do_search_command(self):
        """
            Performs the SEARCH command.
        :return: None
        """    
        print(self.player.current_room.show_items())
        print(self.player.current_room.show_puzzles())
    
    def do_take_command(self, second_word):
        if second_word is None:
            self.ui.print("Take what?")
            return

        for item in self.player.current_room.items:
            if item.name.lower() == second_word.lower():
                if self.player.take_item(item):
                    self.ui.print(f"You took the {item.name}")
                else:
                    self.ui.print("You can't take that")
                return
        
        self.ui.print(f"There is no {second_word} here")

    def do_inventory_command(self):
        """
            Shows the contents of the player's backpack.
        :return: None
        """
        inventory = self.player.get_inventory()
        if not inventory:
            self.ui.print("Your backpack is empty")
            return
        self.ui.print(f"Your backpack contains: {', '.join(inventory)}")
    
    def do_use_command(self, second_word):
        """Uses an item."""
        if second_word is None:
            self.ui.print("Use what?")
            return

        for item in self.player.backpack.contents:
            if item.name.lower() == second_word.lower():
                # check if using item with a puzzle in the room
                if self.player.current_room.puzzles:
                    puzzle = self.player.current_room.puzzles[0]
                    if puzzle.required_items:  
                        success, message = puzzle.solve(items=self.player.backpack.contents)
                        self.ui.print(message)
                        return

                # keycard usage
                if item.is_keycard:
                    found_door = False
                    for direction, room in self.player.current_room.exits.items():
                        if room.required_keycard_level > 0 and room.islocked:
                            if room.required_keycard_level <= item.keycard_level:
                                room.islocked = False
                                self.ui.print(f"You use the level {item.keycard_level} keycard to unlock the {direction} door.")
                                found_door = True
                            else:
                                self.ui.print(f"This keycard (level {item.keycard_level}) isn't high enough level for the {direction} door (requires level {room.required_keycard_level})")
                                found_door = True
                
                    if not found_door:
                        self.ui.print("There are no doors nearby that need a keycard")
                    return
                
                # check if using item with an NPC in the room
                if self.player.current_room.npcs:
                    npc = self.player.current_room.npcs[0]
                    self.ui.print(f"You show the {item.name} to {npc.name}.")
                    if npc.use_item_with(item, self):
                        return
                
                if item.can_be_used:
                    self.ui.print(f"You used the {item.name}")
                else:
                    self.ui.print(f"You can't use the {item.name}")
                return
        
        self.ui.print(f"You don't have a {second_word}")

    def do_solve_command(self, second_word):
        if not self.player.current_room.puzzles:
            self.ui.print("There's no puzzle to solve here.")
            return
        
        puzzle = self.player.current_room.puzzles[0]
        
        #  password-based puzzles
        if puzzle.required_items:
            self.ui.print("This puzzle requires using items. Try using an item instead.")
            return
        
        if second_word is None:
            self.ui.print("What's your solution?")
            return
        
        result = puzzle.solve(second_word)
        if len(result) == 3:  
            success, message, item = result
            if success:
                self.player.backpack.add_item(item)
        else:
            success, message = result
        self.ui.print(message)


    
    def do_speak_command(self):
        if not self.player.current_room.npcs:
            self.ui.print("There's noone to speak to here.")
            return
        
        npc = self.player.current_room.npcs[0]
        current_line = npc.dialogue[npc.dialogue_counter]
        self.ui.print(current_line)
        
        if npc.dialogue_counter < len(npc.dialogue) - 1:
            npc.dialogue_counter += 1

    def save_game(self):
        """Save the current game state to a JSON file"""
        game_state = {
            'player': {
                'current_room': self.player.current_room.get_short_description(),
                'backpack_items': [item.name for item in self.player.backpack.contents]
            },
            'rooms': {
                'corridor': {'islocked': self.corridor.islocked},
                'lab': {'islocked': self.lab.islocked},
                'nuclear_reactor': {'islocked': self.nuclear_reactor.islocked},
                'tunnel': {'islocked': self.tunnel.islocked},
                'agi_room': {'islocked': self.agi_room.islocked}
            },
            'game_won': self.game_won
        }
        
        with open('save_game.json', 'w') as f:
            json.dump(game_state, f, indent=4)
        
        self.ui.print("Game saved successfully!")

    def load_game(self):
        """Load a saved game state from JSON file"""
        try:
            with open('save_game.json', 'r') as f:
                game_state = json.load(f)
                
            # Restore player state
            room_desc = game_state['player']['current_room']
            for room in [self.outside, self.lobby, self.corridor, self.lab, 
                        self.roon_den, self.GPU_cluster, self.fan_closet, 
                        self.nuclear_reactor, self.tunnel, self.sams_bunker, 
                        self.money_room, self.agi_room]:
                if room.get_short_description() == room_desc:
                    self.player.current_room = room
                    break
            
            # Restore backpack items
            self.player.backpack.contents.clear()
            for item_name in game_state['player']['backpack_items']:
                for item in [self.safety_handbook, self.basic_keycard, 
                            self.scientific_keycard, self.executive_keycard, 
                            self.fan]:
                    if item.name == item_name:
                        self.player.backpack.add_item(item)
            
            # Restore room states
            self.corridor.islocked = game_state['rooms']['corridor']['islocked']
            self.lab.islocked = game_state['rooms']['lab']['islocked']
            self.nuclear_reactor.islocked = game_state['rooms']['nuclear_reactor']['islocked']
            self.tunnel.islocked = game_state['rooms']['tunnel']['islocked']
            self.agi_room.islocked = game_state['rooms']['agi_room']['islocked']
            
            # Restore game state
            self.game_won = game_state['game_won']
            
            self.ui.print("Game loaded successfully!")
            self.ui.print(self.player.current_room.get_long_description())
            
        except FileNotFoundError:
            self.ui.print("No saved game found!")


def main():
    """Main entry point for the game."""
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
