"""
Player class - the main character that moves around,
picks up stuff and carries it in their backpack
"""

from backpack import Backpack

class Player:
    """
    The player in the game.
    Can walk between rooms and keep items in backpack.
     handles everything the player can do.
    """
    
    def __init__(self, name, current_room, backpack_capacity=5):
        """
        Makes a new player character.
        
        Args:
            name: what to call them
            current_room: where they start
            backpack_capacity: how much they can carry (usually 5)
        """
        self.name = name
        self.current_room = current_room
        self.backpack = Backpack(backpack_capacity)

    def move_to(self, room):
        """
        Try going into a room.
        Returns True if u got in, False if its locked
        """
        if room.islocked:
            return False
        self.current_room = room
        return True

    def take_item(self, item):
        """
        Try picking up something.
        Returns True if u got it, False if cant pick up/backpack full
        """
        if not item.can_be_taken:
            return False
        return self.backpack.add_item(item)

    def drop_item(self, item):
        """
        Put an item down in current room.
        Returns True if dropped ok
        """
        try:
            self.backpack.remove_item(item)
            self.current_room.add_item(item)
            return True
        except:
            return False

    def has_item(self, item_name):
        """
        See if something is in youur backpack.
        Returns True if its there
        """
        for item in self.backpack.contents:
            if item.name.lower() == item_name.lower():
                return True
        return False

    def get_item(self, item_name):
        """
        Find item in backpack by name.
        Returns the item or None if not found
        """
        for item in self.backpack.contents:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def get_inventory(self):
        """Shows everything in ur backpack"""
        return [item.name for item in self.backpack.contents]
