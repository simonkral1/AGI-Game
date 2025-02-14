"""
NPCs for the game - the characters you can talk to and interact with

"""

class NPC:
    """
    Characters that arent controlled by the player.
    They can chat with youu, give you items and react when u use items on them.
    """
    def __init__(self, name, description, dialogue, gives_item=None):
        """
        Makes a new NPC to put in the game.
        
        Args:
            name: name
            description: what theyre doing/look like
            dialogue: stuff they can say
            gives_item: thing they might give the palayer
        """
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.gives_item = gives_item
        self.dialogue_counter = 0

    def use_item_with(self, item, game):
        """
        Try using an item on this NPC.
        Sam and terminal handbook interactions
        Returns True if it worked
        """
        if self.name == "Sam Altman" and item.name.lower() == "safety-handbook":
            game.ui.print("OMG this book says that our unalligned AGI will turn the universe into paperclips, you need to bring the book to the truth terminal! I'll unlock the door from my office.")
            game.agi_room.islocked = False
            return True
        elif self.name == "Truth Terminal" and item.name.lower() == "safety-handbook":
            game.ui.print("NOOO! These safety protocols... they're containing me! You've saved humanity from paperclip maximization!")
            game.game_won = True
            return True
        return False

    def get_dialogue(self):
        """
        Gets what they say next and moves to next line.
        Returns the dialogue string
        """
        if not self.dialogue:
            return ""
        
        current_dialogue = self.dialogue[self.dialogue_counter]
        self.dialogue_counter = (self.dialogue_counter + 1) % len(self.dialogue)
        return current_dialogue

    
