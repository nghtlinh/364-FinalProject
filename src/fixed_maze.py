from src.cell import Cell
from src.maze import Maze

class FixedMaze(Maze):
    """Fixed maze class with predefined structure."""
    def __init__(self, grid, entry=(0, 0), exit=None, id=0):
        """
        Initialize the fixed maze with a predefined grid.
        Args:
            grid (list): 2D list of integers (1 = wall, 0 = path).
            entry (tuple): Entry point coordinates (row, col).
            exit (tuple): Exit point coordinates (row, col). If None, defaults to bottom-right corner.
            id (int): Unique identifier for the maze.
        """
        self.grid_size = len(grid) * len(grid[0])
        self.num_rows = len(grid)
        self.num_cols = len(grid[0])
        self.id = id
        self.entry_coor = entry
        self.exit_coor = exit or (self.num_rows - 1, self.num_cols - 1)
        self.solution_path = None

        # Convert the 2D integer grid into Cell objects
        self.initial_grid = self._convert_to_cells(grid)
        self.grid = self.initial_grid

    def _convert_to_cells(self, grid):
        """Convert a 2D list of integers into a grid of Cell objects."""
        cell_grid = []
        for row_index, row in enumerate(grid):
            cell_row = []
            for col_index, value in enumerate(row):
                cell = Cell(row_index, col_index)

                # Determine walls based on value and neighbors
                cell.walls = {
                    "top": row_index == 0 or grid[row_index - 1][col_index] == 1,
                    "right": col_index == self.num_cols - 1 or grid[row_index][col_index + 1] == 1,
                    "bottom": row_index == self.num_rows - 1 or grid[row_index + 1][col_index] == 1,
                    "left": col_index == 0 or grid[row_index][col_index - 1] == 1,
                }

                # Mark entry and exit points
                if (row_index, col_index) == self.entry_coor:
                    cell.is_entry_exit = "entry"
                elif (row_index, col_index) == self.exit_coor:
                    cell.is_entry_exit = "exit"

                cell_row.append(cell)
            cell_grid.append(cell_row)
        return cell_grid
