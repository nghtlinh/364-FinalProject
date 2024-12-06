import heapq
import math
import time
import random
import logging
from src.maze import Maze

logging.basicConfig(level=logging.DEBUG)

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

    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.debug('Class BreadthFirst ctor called')

        self.name = "Breadth First Recursive"
        super().__init__(maze, neighbor_method, quiet_mode)

    def solve(self):

        """Function that implements the breadth-first algorithm for solving the maze. This means that
                for each iteration in the outer loop, the search visits one cell in all possible branches. Then
                moves on to the next level of cells in each branch to continue the search."""

        logging.debug("Class BreadthFirst solve called")
        current_level = [self.maze.entry_coor]  # Stack of cells at current level of search
        path = list()  # To track path of solution cell coordinates

        print("\nSolving the maze with breadth-first search...")
        time_start = time.perf_counter()

        while True:  # Loop until return statement is encountered
            next_level = list()

            while current_level:  # While still cells left to search on current level
                k_curr, l_curr = current_level.pop(0)  # Search one cell on the current level
                self.maze.grid[k_curr][l_curr].visited = True  # Mark current cell as visited
                path.append(((k_curr, l_curr), False))  # Append current cell to total search path

                if (k_curr, l_curr) == self.maze.exit_coor:  # Exit if current cell is exit cell
                    if not self.quiet_mode:
                        print("Number of moves performed: {}".format(len(path)))
                        print("Execution time for algorithm: {:.4f}".format(time.perf_counter() - time_start))
                    return path

                neighbour_coors = self.maze.find_neighbours(k_curr, l_curr)  # Find neighbour indicies
                neighbour_coors = self.maze.validate_neighbours_solve(neighbour_coors, k_curr,
                                                                  l_curr, self.maze.exit_coor[0],
                                                                  self.maze.exit_coor[1], self.neighbor_method)

                if neighbour_coors is not None:
                    for coor in neighbour_coors:
                        next_level.append(coor)  # Add all existing real neighbours to next search level

            for cell in next_level:
                current_level.append(cell)  # Update current_level list with cells for nex search level
        logging.debug("Class BreadthFirst leaving solve")

class DepthFirst(Solver):
    """A solver that implements the depth-first recursive backtracker algorithm.
    """

    def __init__(self, maze, quiet_mode=False,  neighbor_method="fancy"):
        logging.debug('Class DepthFirstBacktracker ctor called')

        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "Depth First Backtracker"

    def solve(self):
        logging.debug("Class DepthFirstBacktracker solve called")
        k_curr, l_curr = self.maze.entry_coor      # Where to start searching
        self.maze.grid[k_curr][l_curr].visited = True     # Set initial cell to visited
        visited_cells = list()                  # Stack of visited cells for backtracking
        path = list()                           # To track path of solution and backtracking cells
        if not self.quiet_mode:
            print("\nSolving the maze with depth-first search...")

        time_start = time.time()

        while (k_curr, l_curr) != self.maze.exit_coor:     # While the exit cell has not been encountered
            neighbour_indices = self.maze.find_neighbours(k_curr, l_curr)    # Find neighbour indices
            neighbour_indices = self.maze.validate_neighbours_solve(neighbour_indices, k_curr,
                l_curr, self.maze.exit_coor[0], self.maze.exit_coor[1], self.neighbor_method)

            if neighbour_indices is not None:   # If there are unvisited neighbour cells
                visited_cells.append((k_curr, l_curr))              # Add current cell to stack
                path.append(((k_curr, l_curr), False))  # Add coordinates to part of search path
                k_next, l_next = random.choice(neighbour_indices)   # Choose random neighbour
                self.maze.grid[k_next][l_next].visited = True                 # Move to that neighbour
                k_curr = k_next
                l_curr = l_next

            elif len(visited_cells) > 0:              # If there are no unvisited neighbour cells
                path.append(((k_curr, l_curr), True))   # Add coordinates to part of search path
                k_curr, l_curr = visited_cells.pop()    # Pop previous visited cell (backtracking)

        path.append(((k_curr, l_curr), False))  # Append final location to path
        if not self.quiet_mode:
            print("Number of moves performed: {}".format(len(path)))
            print("Execution time for algorithm: {:.4f}".format(time.time() - time_start))

        logging.debug('Class DepthFirstBacktracker leaving solve')
        return path

class AStar(Solver):
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
    
    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "AStar"
        
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
                    h_new = self._manhattan_heuristic(neighbor, goal)
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