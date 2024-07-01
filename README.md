# Tile Color Flood Game

This challenge implements a one-player tile color flood game where the goal is to make all tiles on an `n x n` board the same color with the fewest number of moves. The player can choose from `m` different colors, and each move changes the color of all tiles connected to the origin tile to the chosen color.

### Algorithm

I firstly implemented a greedy algorithm , which made decisions based solely on the immediate number of adjacent tiles that could be changed but this algorithm sometimes caused loops or inefficient solutions. So, to improve the performance, I used a lookahead strategy, this one simulates potential future moves to make better decisions and it improved the efficiency of the game.

## How the Lookahead Strategy Works

1. **Simulate Move**: Creates a clone of the current board and applies a move to it.
2. **Recursive Lookahead**: Simulates future moves up to a specified depth andfor every possible color move it evaluates the board state after the move, then recursively looks ahead one step further
3. **Evaluating and Choosing the Best Move**: Uses the flood_fill method on the simulated board to evaluate the number of tiles that can be flooded for each potential move. Selects the color that maximizes the number of connected tiles in future states

## How to Run the Code

### Running the Game

**Run the game**:
`bash
    python game.py
    `

### Running the Tests

**Run the tests**:
`bash
    python test_game.py
    `

## Explanation of Test Cases

- **test_flood_fill**: Verifies that the flood fill algorithm correctly changes the color of connected tiles.
- **test_choose_best_color**: Ensures that the algorithm for choosing the best color works correctly.
- **test_play**: Checks the entire game flow on a fixed board, ensuring it completes within a reasonable number of moves and that the moves are valid.
- **test_single_color_board**: Ensures that a board with a single color is recognized as already complete.
- **test_all_different_colors**: Tests the game's handling of a board with all different colors.
- **test_small_board**: Verifies the game's behavior on the smallest possible board.
- **test_randomized_board**: Tests the game on a randomized board to ensure robustness.
