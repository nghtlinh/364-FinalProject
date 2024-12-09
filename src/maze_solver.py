import math
import time
import random
import logging
from src.maze import Maze
import warnings

logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.getLogger('PIL').setLevel(logging.WARNING)
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
logging.basicConfig(level=logging.INFO)  # Change to INFO to reduce verbosity

class Solver(object):
    """Base class for solution methods.
    Every new solution method should override the solve method.

    Attributes:
        maze (list): The maze which is being solved.
        neighbor_method:
        quiet_mode: When enabled, information is not outputted to the console

    """

    def __init__(self, maze, quiet_mode, neighbor_method):
        logging.debug("Class Solver ctor called")

        self.maze = maze
        self.neighbor_method = neighbor_method
        self.name = ""
        self.quiet_mode = quiet_mode

    def solve(self):
        logging.debug('Class: Solver solve called')
        raise NotImplementedError

    def get_name(self):
        logging.debug('Class Solver get_name called')
        raise self.name

    def get_path(self):
        logging.debug('Class Solver get_path called')
        return self.path

class BreadthFirst(Solver):

    def __init__(self, maze, quiet_mode=False, neighbor_method="brute-force"):
        logging.debug('Class BFSCellSolver ctor called')
        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "BFS Cell Solver"
    
    def solve(self):
        """Solve maze using breadth-first search algorithm"""
        logging.debug("Class BFSCellSolver solve called")
        print("\nSolving the maze with breadth-first search...")
        
        time_start = time.time()
        
        # Initialize variables
        visited = set()  # Using a set for O(1) lookup
        queue = []
        path = []
        
        # Add start position to queue
        current = self.maze.entry_coor
        queue.append(current)
        visited.add(current)
        
        # Keep track of parent cells for path reconstruction
        parent = {}
        
        while queue:
            current = queue.pop(0)  # Take first element (FIFO)
            path.append((current, False))
            
            # Check if reached exit
            if current == self.maze.exit_coor:
                print(f"Number of moves performed: {len(path)}")
                print(f"Execution time for algorithm: {time.time() - time_start:.4f}")
                
                # Reconstruct the actual path from entry to exit
                final_path = []
                curr = current
                while curr in parent:
                    final_path.append((curr, False))
                    curr = parent[curr]
                final_path.append((self.maze.entry_coor, False))
                final_path.reverse()
                return final_path
            
            # Find valid neighbors
            neighbors = self.maze.find_neighbours(current[0], current[1])
            if neighbors:
                for k_n, l_n in neighbors:
                    # Check if neighbor is unvisited and accessible (no walls between)
                    if (k_n, l_n) not in visited and not self.maze.grid[current[0]][current[1]].is_walls_between(self.maze.grid[k_n][l_n]):
                        queue.append((k_n, l_n))
                        visited.add((k_n, l_n))
                        parent[(k_n, l_n)] = current
                        self.maze.grid[k_n][l_n].visited = True
        
        logging.debug("Class BFSCellSolver leaving solve - no solution found")
        return path

class DepthFirst(Solver):
    """A solver that implements the depth-first recursive backtracker algorithm."""

    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.debug('Class DepthFirstBacktracker ctor called')
        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "Depth First Backtracker"

    def solve(self):
        logging.debug("Class DepthFirstBacktracker solve called")
        print("\nSolving the maze with depth-first search...")

        time_start = time.time()
        
        k_curr, l_curr = self.maze.entry_coor
        self.maze.grid[k_curr][l_curr].visited = True
        visited_cells = []
        path = []
        
        while (k_curr, l_curr) != self.maze.exit_coor:
            neighbor_indices = self.maze.find_neighbours(k_curr, l_curr)
            valid_neighbors = []

            if neighbor_indices:
                for k_n, l_n in neighbor_indices:
                    if (not self.maze.grid[k_n][l_n].visited and 
                        not self.maze.grid[k_curr][l_curr].is_walls_between(
                            self.maze.grid[k_n][l_n])):
                        valid_neighbors.append((k_n, l_n))
            
            if valid_neighbors:
                visited_cells.append((k_curr, l_curr))
                path.append(((k_curr, l_curr), False))

                k_next, l_next = random.choice(valid_neighbors)
                self.maze.grid[k_next][l_next].visited = True
                
                # Move to that neighbor
                k_curr, l_curr = k_next, l_next
                
            elif visited_cells:
                path.append(((k_curr, l_curr), True))
                k_curr, l_curr = visited_cells.pop()
                
            else:
                print("No solution found!")
                print(f"Execution time for algorithm: {time.time() - time_start:.4f}")
                return path

        path.append(((k_curr, l_curr), False))
        
        print(f"Number of moves performed: {len(path)}")
        print(f"Execution time for algorithm: {time.time() - time_start:.4f}")

        return path
    
class AStar(Solver):
    """A solver that implements the A* pathfinding algorithm."""
    
    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy", heuristic="Manhattan"):
        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "A* Solver"
        self.heuristic = heuristic
    
    def _manhattan_heuristic(self, current, goal):
        """Calculate the Manhattan distance heuristic."""
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])
    
    def _euclidean_heuristic(self, current, goal):
        """Calculate the Euclidean distance heuristic."""
        return math.sqrt((current[0] - goal[0])**2 + (current[1] - goal[1])**2)
    
    def _get_heuristic(self, current, goal):
        """Get the appropriate heuristic based on settings."""
        if self.heuristic.lower() == "manhattan":
            return self._manhattan_heuristic(current, goal)
        elif self.heuristic.lower() == "euclidean":
            return self._euclidean_heuristic(current, goal)
        else:
            return self._manhattan_heuristic(current, goal)

    def solve(self):
        """Solve maze using A* pathfinding algorithm"""
        logging.debug("Class AStar solve called")
        print(f"\nSolving the maze with A* algorithm using {self.heuristic} heuristic...")
        
        time_start = time.time()
        start = self.maze.entry_coor
        goal = self.maze.exit_coor
        
        open_set = {start}  # Nodes to be evaluated
        closed_set = set()  # Nodes already evaluated
        came_from = {}      # Path tracking
        g_score = {start: 0}  # Cost from start to current position
        f_score = {start: self._get_heuristic(start, goal)}  # Estimated total cost
        path = []  # Track the exploration path
        
        while open_set:
            # Get node with lowest f_score
            current = min(open_set, key=lambda pos: f_score.get(pos, float('inf')))
            path.append((current, False))
            
            if current == goal:
                # Reconstruct path
                final_path = []
                while current in came_from:
                    final_path.append((current, False))
                    current = came_from[current]
                final_path.append((start, False))
                final_path.reverse()
                
                print(f"Number of moves performed: {len(path)}")
                print(f"Execution time for algorithm: {time.time() - time_start:.4f}")
                return final_path
            
            open_set.remove(current)
            closed_set.add(current)
            
            # Find valid neighbors
            neighbors = self.maze.find_neighbours(current[0], current[1])
            if neighbors:
                for k_n, l_n in neighbors:
                    neighbor = (k_n, l_n)
                    
                    # Skip if in closed set or there's a wall between cells
                    if neighbor in closed_set or self.maze.grid[current[0]][current[1]].is_walls_between(self.maze.grid[k_n][l_n]):
                        continue
                    
                    tentative_g_score = g_score[current] + 1
                    
                    if neighbor not in open_set:
                        open_set.add(neighbor)
                    elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                        continue
                    
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self._get_heuristic(neighbor, goal)
                    self.maze.grid[k_n][l_n].visited = True
        
        print("No solution found!")
        print(f"Execution time for algorithm: {time.time() - time_start:.4f}")
        return path