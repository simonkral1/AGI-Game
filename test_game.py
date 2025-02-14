import unittest
from game import Game

class TestGame(unittest.TestCase):
    """Main test suite for our AGI escape room game"""
    
    def setUp(self):
        """Fresh game for each test"""
        self.game = Game()
    
    def test_room_navigation(self):
        """Player should be able to move between rooms and see available exits"""
        self.assertEqual(self.game.player.current_room, self.game.outside)
        self.game.player.move_to(self.game.lobby)
        self.assertEqual(self.game.player.current_room, self.game.lobby)
        exits = self.game.lobby.get_exits()
        self.assertIn("south", exits)
        self.assertIn("east", exits)
    
    def test_items(self):
        """Player should find and pick up the keycard in the lobby"""
        self.game.player.move_to(self.game.lobby)
        
        found = False
        for item in self.game.lobby.items:
            if item.name == "basic-keycard":
                found = True
                self.game.player.take_item(item)
        
        self.assertTrue(found)
        self.assertIn("basic-keycard", self.game.player.get_inventory())
    
    def test_puzzle(self):
        """GPU cluster puzzle should only be solvable with the cooling fan"""
        self.game.player.move_to(self.game.GPU_cluster)
        puzzle = self.game.GPU_cluster.puzzles[0]
        
        success, _ = puzzle.solve(items=[])
        self.assertFalse(success)
        
        success, _ = puzzle.solve(items=[self.game.fan])
        self.assertTrue(success)

    def test_win_condition(self):
        """Game should be winnable by using the safety handbook in the right places"""
        self.game.player.move_to(self.game.money_room)
        
        self.game.player.backpack.add_item(self.game.safety_handbook)
        self.game.money_room.npcs[0].use_item_with(self.game.safety_handbook, self.game)  

        self.game.player.move_to(self.game.agi_room)
        self.game.agi_room.npcs[0].use_item_with(self.game.safety_handbook, self.game)

    def test_keycard_unlocking(self):
        """Basic keycard should unlock level 1 doors"""
        self.game.player.move_to(self.game.lobby)
        self.game.player.take_item(self.game.basic_keycard)
        
        self.assertTrue(self.game.corridor.islocked)
        self.game.do_use_command("basic-keycard")
        self.assertFalse(self.game.corridor.islocked)

    def test_npc_interaction(self):
        """Sam should react differently after seeing the safety handbook"""
        self.game.player.move_to(self.game.money_room)
        
        sama = self.game.money_room.npcs[0]
        self.assertEqual(sama.name, "Sam Altman")
        
        initial_dialogue = sama.get_dialogue()
        self.game.player.backpack.add_item(self.game.safety_handbook)
        sama.use_item_with(self.game.safety_handbook, self.game)
        self.assertNotEqual(sama.get_dialogue(), initial_dialogue)

    def test_locked_room_progression(self):
        """Security system should require appropriate keycard levels"""
        self.game.player.move_to(self.game.lobby)
        
        corridor = self.game.corridor
        self.assertEqual(corridor.required_keycard_level, 1)
        self.assertTrue(corridor.islocked or corridor.required_keycard_level > 0)
        
        self.game.player.backpack.add_item(self.game.basic_keycard)
        self.game.do_use_command("basic-keycard")
        self.assertFalse(corridor.islocked)
        
        lab = self.game.lab
        self.assertEqual(lab.required_keycard_level, 2)
        self.assertTrue(lab.islocked or lab.required_keycard_level > 0)

    def test_inventory_management(self):
        """Items should be properly tracked when picked up and dropped"""
        self.game.player.move_to(self.game.lobby)
        
        initial_count = len(self.game.player.get_inventory())
        self.game.player.take_item(self.game.basic_keycard)
        self.assertEqual(len(self.game.player.get_inventory()), initial_count + 1)
        
        self.game.player.drop_item(self.game.basic_keycard)
        self.assertEqual(len(self.game.player.get_inventory()), initial_count)
        self.assertIn(self.game.basic_keycard, self.game.player.current_room.items)

    def test_room_description(self):
        """Room descriptions should update when NPCs enter"""
        room = self.game.GPU_cluster
        
        short_desc = room.get_short_description()
        self.assertIn("GPU cluster", short_desc)
        
        long_desc = room.get_long_description()
        self.assertIn("Exits:", long_desc)
        
        room.add_npc(self.game.sama)
        self.assertIn(self.game.sama.name, room.get_long_description())

if __name__ == '__main__':
    unittest.main() 