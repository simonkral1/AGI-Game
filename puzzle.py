"""
Puzzle system for the game - handles password puzzels and item-based ones!
Pretty much anything that needs solving goes here
"""

class Puzzle:
    """
    A puzzle that players solve with either a password or some items.
    When u solve it, it might unlock a room or give an item
    Can be either a password puzzle (like a keypad) or need specific items.
    
    Attributes:
        name: Puzzle's display name
        description: How the puzzle appears to player
        is_solved: Whether puzzle is completed
        password: Solution word (if it's a password puzzle)
        required_items: Items needed to solve (if it's an item puzzle)
        gives_items: Reward items when solved
    """
    
    def __init__(self, name, description, success_message, 
                 unlocks_room=None, is_solved=False, password=None, 
                 required_items=None, gives_items=None):
        """
        Makes a new puzzle to challenge the player.
        
        Args:
            name: what to call it
            description: what it looks like/how it works
            success_message: what to show when they win
            unlocks_room: room it unlocks (if any)
            password: the answer (if its a password puzzle)
            required_items: stuff needed to solve it
            gives_items: rewards u get
        """
        self.name = name
        self.description = description
        self.is_solved = is_solved
        self.success_message = success_message
        self.password = password
        self.unlocks_room = unlocks_room
        self.required_items = required_items or []
        self.gives_items = gives_items or []

    def solve(self, attempt=None, items=None):
        """
        Try to solve it with password or items.
        Returns if it worked, a message, and maybe some items
        """
        #  check if puzzle requires items
        if self.required_items:
            return self._solve_with_items(items)
            
        #  password solution
        return self._solve_with_password(attempt)
            
    def _solve_with_items(self, items):
        """
        Checks if player used the right items.
        Returns if it worked + what to tell them
        """
        if not items:
            return False, "You might need some items to solve this..."
        
        required_names = [item.name.lower() for item in self.required_items]
        provided_names = [item.name.lower() for item in items]
        
        if all(name in provided_names for name in required_names):
            self._mark_solved()
            return True, self.success_message
        return False, "You don't have the right combination of items."

    def _solve_with_password(self, attempt):
        """
        See if they got the password right.
        Returns if correct + message + maybe items
        """
        if attempt == self.password:
            self._mark_solved()
            if self.gives_items:
                return True, self.success_message, self.gives_items
            return True, self.success_message
        return False, "That's not correct."
        
    def _mark_solved(self):
        """
        Sets puzzle as done and opens any door it should
        """
        self.is_solved = True
        if self.unlocks_room:
            self.unlocks_room.islocked = False

            


    




    
    