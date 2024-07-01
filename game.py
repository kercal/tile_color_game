import random

class Tile:
    def __init__(self, color):
        """
        initialize a tile with a specific color
        """
        self.color = color

class Board:
    def __init__(self, n, m, colors):
        """
        initialize the board with dimensions and colors
        """
        self.n = n  # Board size
        self.m = m  # Number of colors
        # Create a grid of Tiles based on the provided colors
        self.grid = [[Tile(color) for color in row] for row in colors]

    def get_tile(self, x, y):
        """
        get the Tile object at the specified coordinates
        """
        if 0 <= x < self.n and 0 <= y < self.n:
            return self.grid[x][y]
        return None

    def set_tile_color(self, x, y, color):
        """
        set the color of the Tile at the specified coordinates
        """
        if 0 <= x < self.n and 0 <= y < self.n:
            self.grid[x][y].color = color

    def get_origin_color(self):
        """
        Get the color of the tile at the origin (0, 0)
        """
        return self.grid[0][0].color

    def clone(self):
        """
        Clone the board to create a new independent copy
        """
        colors = [[self.grid[x][y].color for y in range(self.n)] for x in range(self.n)]
        return Board(self.n, self.m, colors)

    def print_board(self):
        """
        Print the current state of the board to the console.
        """
        for row in self.grid:
            print(' '.join(tile.color for tile in row))
        print()

class Game:
    def __init__(self, board):
        """
        Initialize the Game with a Board
        """
        self.board = board
        self.moves = []  # List to keep track of moves made
        self.max_moves = 12  # Maximum number of moves allowed to prevent infinite loops

    def get_adjacent(self, x, y):
        """
        Get the coordinates of adjacent tiles.
       
        """
        adjacent = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_tile = self.board.get_tile(x + dx, y + dy)
            if adj_tile:
                adjacent.append((x + dx, y + dy))
        return adjacent

    def flood_fill(self, x, y, target_color, replacement_color, visited):
        """
        Perform a flood fill algorithm to change the color of connected tiles
 
        Return the number of tiles changed
        """
        if (x, y) in visited:
            return 0
        visited.add((x, y))

        tile = self.board.get_tile(x, y)
        if not tile or tile.color != target_color:
            return 0

        self.board.set_tile_color(x, y, replacement_color)
        size = 1

        for adj_x, adj_y in self.get_adjacent(x, y):
            size += self.flood_fill(adj_x, adj_y, target_color, replacement_color, visited)

        return size

    def choose_best_color(self):
        """
        Choose the best color to flood fill based on the greedy strategy.
        
        """
        origin_color = self.board.get_origin_color()
        # Dictionary to count the number of adjacent tiles for each color
        color_counts = {color: 0 for color in set(tile.color for row in self.board.grid for tile in row)}

        # Count the number of adjacent tiles for each color
        for x in range(self.board.n):
            for y in range(self.board.n):
                if self.board.get_tile(x, y).color == origin_color:
                    for adj_x, adj_y in self.get_adjacent(x, y):
                        adj_tile = self.board.get_tile(adj_x, adj_y)
                        if adj_tile.color != origin_color:
                            color_counts[adj_tile.color] += 1

        # Choose the color with the maximum adjacent tiles, breaking ties by color rank
        best_color = min(color_counts, key=lambda color: (-color_counts[color], color))
        return best_color

    def simulate_move(self, color):
        """
        Simulate a move by creating a clone of the current board and applying the move
        """
        simulated_board = self.board.clone()
        simulated_game = Game(simulated_board)
        simulated_game.flood_fill(0, 0, simulated_board.get_origin_color(), color, set())
        return simulated_board

    def lookahead(self, depth=2):
        """
        Perform a lookahead strategy by simulating moves up to a certain depth
        """
        if depth == 0:
            return self.choose_best_color()

        origin_color = self.board.get_origin_color()
        color_counts = {color: 0 for color in set(tile.color for row in self.board.grid for tile in row)}

        for color in color_counts:
            if color == origin_color:
                continue
            simulated_board = self.simulate_move(color)
            simulated_game = Game(simulated_board)
            next_color = simulated_game.lookahead(depth - 1)
            color_counts[color] = simulated_game.flood_fill(0, 0, color, next_color, set())

        best_color = min(color_counts, key=lambda color: (-color_counts[color], color))
        return best_color

    def play(self):
        """
        Play the game until all tiles are the same color or the maximum number of moves (12) is reached
        """
        while len(self.moves) < self.max_moves:
            origin_color = self.board.get_origin_color()
            best_color = self.lookahead(depth=2)  # Using a lookahead of 2 moves
            if best_color == origin_color:
                break
            self.moves.append(best_color)
            self.flood_fill(0, 0, origin_color, best_color, set())
            self.board.print_board()

        if len(self.moves) >= self.max_moves:
            print(f"Reached maximum number of moves ({self.max_moves}) without solving the board.")
        
        return self.moves

def generate_random_board(n, m):
    """
    Generate a random n x n board with m distinct colors
    """
    colors = [chr(i) for i in range(65, 65 + m)]  
    return [[random.choice(colors) for _ in range(n)] for _ in range(n)]


# Example usage:
if __name__ == "__main__":
    n = 6  # Board size
    m = 3  # Number of distinct colors
    random_colors = generate_random_board(n, m)
    board = Board(n, m, random_colors)
    game = Game(board)
    
    print("Initial board:")
    board.print_board()
    
    game.play()

