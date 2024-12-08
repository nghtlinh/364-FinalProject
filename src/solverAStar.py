import heapq
import math
import time
import logging
from src.maze import Maze

logging.basicConfig(level=logging.DEBUG)

class SolverAStar(object):
    """Base class for solution methods.
    Every new solution method should override the solve method.

    Attributes:
        maze (list): The maze which is being solved.
        neighbor_method:
        quiet_mode: When enabled, information is not outputted to the console

    """

    def __init__(self, maze, quiet_mode, neighbor_method, heuristic_method):
        self.maze = maze
        self.neighbor_method = neighbor_method
        self.name = ""
        self.quiet_mode = quiet_mode
        self.heuristic_method = heuristic_method
    
class AStar(SolverAStar):
    """A solver that implements the A* pathfinding algorithm.
    Uses a reliable heuristic function and proper cell tracking.
    """
    
    class AStarCell:
        """Helper class to track A* specific cell information"""
        def __init__(self):
            self.parent = None  # Parent cell coordinates
            self.f = float('inf')  # Total cost (g + h)
            self.g = float('inf')  # Cost from start
            self.h = 0  # Heuristic estimate to goal
    
    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy", heuristic_method=""):
        super().__init__(maze, neighbor_method, quiet_mode, heuristic_method)
        self.name = "AStar"
        self.heuristic_method = heuristic_method
        
    def _euclidean_heuristic(self, current, goal):
        """Calculate the Euclidean distance heuristic between current and goal coordinates."""
        return math.sqrt((current[0] - goal[0])**2 + (current[1] - goal[1])**2)
    
    def _manhattan_heuristic(self, current, goal):
        """Calculate the Manhattan distance heuristic between current and goal coordinates."""
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def solve(self):
        """Implements the A* pathfinding algorithm to solve the maze."""
        logging.debug("Class AStar solve called")
        
        # Reset visited status
        for i in range(self.maze.num_rows):
            for j in range(self.maze.num_cols):
                self.maze.grid[i][j].visited = False
        
        start = self.maze.entry_coor
        goal = self.maze.exit_coor
        
        if not self.quiet_mode:
            print("\nSolving the maze with A* pathfinding algorithm...")
        time_start = time.time()
        
        # Initialize cell details grid
        cell_details = [[self.AStarCell() for _ in range(self.maze.num_cols)] 
                       for _ in range(self.maze.num_rows)]
        
        # Initialize start cell
        cell_details[start[0]][start[1]].f = 0
        cell_details[start[0]][start[1]].g = 0
        cell_details[start[0]][start[1]].h = 0
        cell_details[start[0]][start[1]].parent = start
        
        # Initialize open and closed lists
        open_list = [(0, start)]  # (f_score, coordinates)
        closed_list = set()
        
        while open_list:
            # Get cell with minimum f_score
            current = heapq.heappop(open_list)[1]
            
            if current in closed_list:
                continue
                
            closed_list.add(current)
            self.maze.grid[current[0]][current[1]].visited = True
            
            # Check if we reached the goal
            if current == goal:
                # Reconstruct path
                path = []
                while current != start:
                    # Check if this cell was part of backtracking
                    path.append((current, False))
                    current = cell_details[current[0]][current[1]].parent
                path.append((start, False))
                path.reverse()
                
                if not self.quiet_mode:
                    print("Number of moves performed: {}".format(len(path)))
                    print("Execution time for algorithm: {:.4f}".format(time.time() - time_start))
                
                self.maze.solution_path = path
                return path
            
            # Get valid neighbors
            neighbors = self.maze.find_neighbours(current[0], current[1])
            if neighbors:
                neighbors = self.maze.validate_neighbours_solve(
                    neighbors, current[0], current[1],
                    goal[0], goal[1], self.neighbor_method
                )
            
            if not neighbors:
                continue
                
            # Check each neighbor
            for neighbor in neighbors:
                if neighbor in closed_list:
                    continue
                    
                # Calculate new g score
                g_new = cell_details[current[0]][current[1]].g + 1
                
                # Check if neighbor is in open list with a better path
                if (cell_details[neighbor[0]][neighbor[1]].f == float('inf') or 
                    cell_details[neighbor[0]][neighbor[1]].g > g_new):
                    
                    # Update neighbor's details
                    if self.heuristic_method == "Manhattan":
                        h_new = self._manhattan_heuristic(neighbor, goal)
                    elif self.heuristic_method == "Euclidean":
                        h_new = self._euclidean_heuristic(neighbor, goal)
                    f_new = g_new + h_new
                    
                    cell_details[neighbor[0]][neighbor[1]].f = f_new
                    cell_details[neighbor[0]][neighbor[1]].g = g_new
                    cell_details[neighbor[0]][neighbor[1]].h = h_new
                    cell_details[neighbor[0]][neighbor[1]].parent = current
                    
                    heapq.heappush(open_list, (f_new, neighbor))
        
        if not self.quiet_mode:
            print("No solution found!")
            print("Execution time for algorithm: {:.4f}".format(time.time() - time_start))
        
        self.maze.solution_path = None
        return None
        