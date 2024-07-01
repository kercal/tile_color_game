import unittest
from game import Board, Game, generate_random_board

class TestGame(unittest.TestCase):

    def setUp(self):
        # Predefined board configuration for consistency
        colors = [
            ['R', 'G', 'B', 'B', 'G', 'R'],
            ['R', 'R', 'B', 'B', 'G', 'R'],
            ['G', 'G', 'G', 'B', 'B', 'G'],
            ['B', 'R', 'R', 'G', 'G', 'G'],
            ['G', 'G', 'B', 'B', 'R', 'R'],
            ['R', 'R', 'G', 'G', 'B', 'B']
        ]
        self.board = Board(6, 3, colors)
        self.game = Game(self.board)

    def test_flood_fill(self):
        print("Running test_flood_fill")
        self.game.flood_fill(0, 0, 'R', 'G', set())
        self.assertEqual(self.board.get_tile(0, 0).color, 'G')
        self.assertEqual(self.board.get_tile(1, 0).color, 'G')
        self.assertEqual(self.board.get_tile(1, 1).color, 'G')
        print("test_flood_fill passed")

    def test_choose_best_color(self):
        print("Running test_choose_best_color")
        best_color = self.game.choose_best_color()
        self.assertEqual(best_color, 'G')
        print("test_choose_best_color passed")

    def test_play(self):
        print("Running test_play")
        moves = self.game.play()
        self.assertTrue(len(moves) >= 5 and len(moves) <= 12)
        self.assertTrue(all(move in ['R', 'G', 'B'] for move in moves))
        final_color = self.board.get_tile(0, 0).color
        self.assertTrue(all(tile.color == final_color for row in self.board.grid for tile in row))
        print(f"test_play passed with {len(moves)} moves")

class TestGameAdditional(unittest.TestCase):

    def test_single_color_board(self):
        print("Running test_single_color_board")
        colors = [
            ['R', 'R', 'R'],
            ['R', 'R', 'R'],
            ['R', 'R', 'R']
        ]
        board = Board(3, 1, colors)
        game = Game(board)
        moves = game.play()
        self.assertEqual(len(moves), 0)
        final_color = board.get_tile(0, 0).color
        self.assertTrue(all(tile.color == final_color for row in board.grid for tile in row))
        print("test_single_color_board passed")

    def test_all_different_colors(self):
        print("Running test_all_different_colors")
        colors = [
            ['R', 'G', 'B'],
            ['G', 'B', 'R'],
            ['B', 'R', 'G']
        ]
        board = Board(3, 3, colors)
        game = Game(board)
        moves = game.play()
        self.assertTrue(len(moves) >= 1 and len(moves) <= 9)
        final_color = board.get_tile(0, 0).color
        self.assertTrue(all(tile.color == final_color for row in board.grid for tile in row))
        print(f"test_all_different_colors passed with {len(moves)} moves")

    def test_small_board(self):
        print("Running test_small_board")
        colors = [['R']]
        board = Board(1, 1, colors)
        game = Game(board)
        moves = game.play()
        self.assertEqual(len(moves), 0)
        final_color = board.get_tile(0, 0).color
        self.assertTrue(all(tile.color == final_color for row in board.grid for tile in row))
        print("test_small_board passed")

    def test_randomized_board(self):
        print("Running test_randomized_board")
        n = 6  # Size of the board
        m = 3  # Number of distinct colors
        random_colors = generate_random_board(n, m)
        board = Board(n, m, random_colors)
        game = Game(board)
        moves = game.play()
        self.assertTrue(len(moves) > 0 and len(moves) <= game.max_moves)
        self.assertTrue(all(move in [chr(i) for i in range(65, 65 + m)] for move in moves))
        final_color = board.get_tile(0, 0).color
        self.assertTrue(all(tile.color == final_color for row in board.grid for tile in row))
        print(f"test_randomized_board passed with {len(moves)} moves")

if __name__ == '__main__':
    unittest.main()
