"""
Items that players can find and use in the game - like keycards and tools!
"""

class Item:
    """
    Something players can pick up and use.
    Can be a regular item or a keycard that unlocks rooms.
    
    Attributes:
        name: What the item is called
        description: What it looks like/does
        can_be_taken: If player can pick it up
        can_be_used: If player can use it
        is_keycard: If it's a keycard for locked rooms
        keycard_level: Security level (0-3) if it's a keycard
    """
    def __init__(self, name, description, can_be_taken, can_be_used=True, unlocks=None, is_keycard=False, keycard_level=0):
        """
        Makes a new item.
        
        Args:
            name: Item's name
            description: What it looks like/does
            can_be_taken: If it can be picked up
            can_be_used: If it can be used (default: True)
            unlocks: What this item unlocks (optional)
            is_keycard: If it's a keycard (default: False)
            keycard_level: Keycard security level (default: 0)
        """
        self.name = name
        self.description = description
        self.can_be_taken = can_be_taken
        self.can_be_used = can_be_used
        self.unlocks = unlocks
        self.is_keycard = is_keycard
        self.keycard_level = keycard_level

    def get_description(self):
        """Gets what the item looks like/does"""
        return self.description

    def __str__(self):
        """Returns item's name when printed"""
        return self.name

    def use_item(self):
        """
        Try to use the item.
        Returns True if usable, False if not
        """
        return self.can_be_used

      




