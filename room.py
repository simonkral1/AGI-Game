"""
Room module for the game - handles all the places players can go to.
Has stuff like exits, items they can pickup, and NPCs to talk to.
"""

class Room:
    """
    A place in the game world. Has exits to other rooms and can contain
    items/puzzels/NPCs. Some rooms need keycards to get in.
    """

    def __init__(self, description, islocked=False, required_keycard_level=0):
        """
        Makes new room with given desc and security level.
        
        Args:
            description: what player sees when they enter
            islocked: if its locked at start
            required_keycard_level: security level needed (0-3)
        """
        self.description = description
        self.exits = {}  
        self.items = []
        self.puzzles = []
        self.npcs = []
        self.islocked = islocked or required_keycard_level > 0
        self.required_keycard_level = required_keycard_level

    def set_exit(self, direction, neighbour):
        """
        Adds exit to another room in given direction.
        direction = where to go (eg north)
        neighbour = connecting room
        """
        self.exits[direction] = neighbour

    def get_short_description(self):
        """Quick description of the room"""
        return self.description

    def get_long_description(self):
        """
        Detailed room info - shows description, available exits,
        and any NPCs 
        """
        base_desc = f'Location: {self.description}, Exits: {self.get_exits()}'
        
        locked_exits = []
        for direction, room in self.exits.items():
            if room.required_keycard_level > 0:
                locked_exits.append(f"{direction} (requires level {room.required_keycard_level} keycard)")
        if locked_exits:
            base_desc += "\nLocked exits: " + ", ".join(locked_exits)
        
        if self.npcs:  
            npc_descriptions = [f"{npc.name} - {npc.description}" for npc in self.npcs]
            base_desc += "\nPresent: " + "; ".join(npc_descriptions)
        return base_desc + "."

    def get_exits(self):
        """Lists exits you can use"""
        return list(self.exits.keys())

    def get_exit(self, direction):
        """Gets room in that direction (None if theres no exit)"""
        return self.exits.get(direction)

    def add_item(self, item: object):
        """Puts item in the room for player to find"""
        self.items.append(item)

    def add_puzzle(self, puzzle: object):
        """Adds puzzel to the room"""
        self.puzzles.append(puzzle)

    def add_npc(self, npc: object):
        """Puts NPC in the room"""
        self.npcs.append(npc)

    def show_items(self):
        """
        Shows what items are in room. Says if theres nothing here
        """
        if not self.items:
            return "You see no items in this room"
        return "You see: " + ", ".join([f"{item.name}, {item.description}" for item in self.items])
    
    def show_puzzles(self):
        """
        Lists any puzzels in the room, or tells u if none exist
        """
        if not self.puzzles:
            return "There are no puzzles in this room"
        return "You see: " + ", ".join([f"{puzzle.name}, {puzzle.description}" for puzzle in self.puzzles])

    def remove_item(self, item):
        """
        Takes item from room if its here. Returns None if cant find it
        """
        try:
            if item in self.items:
                self.items.remove(item)
                return item
            return None
        except ValueError:
            return None

    def get_locked_exits(self):
        """Shows which exits need keycard access"""
        return [room for direction, room in self.exits.items() if room.islocked]








