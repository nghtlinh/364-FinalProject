from src.maze import Maze
from src.maze_vizualization import Visualizer
from src.maze_solver import DepthFirst
from src.maze_solver import BreadthFirst
from src.maze_solver import AStar

class MazeManager(object):
    """A manager that abstracts the interaction with the library's components. The graphs, animations, maze creation,
    and solutions are all handled through the manager.

    Attributes:
        mazes (list): It is possible to have more than one maze. They are stored inside this variable.
        media_name (string): The filename for animations and images
        quiet_mode (bool): When true, information is not shown on the console
    """

    def __init__(self):
        self.mazes = []
        self.media_name = ""
        self.quiet_mode = False

    def add_maze(self, row, col, id=0):
        """Add a maze to the manager. We give the maze an index of
        the total number of mazes in the manager. As long as we don't
        add functionality to delete mazes from the manager, the ids will
        always be unique. Note that the id will always be greater than 0 because
        we add 1 to the length of self.mazes, which is set after the id assignment

        Args:
            row (int): The height of the maze
            col (int): The width of the maze
            id (int):  The optional unique id of the maze.

        Returns
            Maze: The newly created maze
        """

        if id != 0:
            self.mazes.append(Maze(row, col, id))
        else:
            if len(self.mazes) < 1:
                self.mazes.append(Maze(row, col, 0))
            else:
                self.mazes.append(Maze(row, col, len(self.mazes) + 1))

        return self.mazes[-1]

    def add_existing_maze(self, maze, override=True):
        """Add an already existing maze to the manager.
        Note that it is assumed that the maze already has an id. If the id
        already exists, the function will fail. To assign a new, unique id to
        the maze, set the overwrite flag to true.

        Args:
            maze: The maze that will be added to the manager
            override (bool): A flag that you can set to bypass checking the id

        Returns:
            True: If the maze was added to the manager
            False: If the maze could not be added to the manager
        """

        # Check if there is a maze with the same id. If there is a conflict, return False
        if self.check_matching_id(maze.id) is None:
            if override:
                if len(self.mazes) < 1:
                    maze.id = 0
                else:
                    maze.id = self.mazes.__len__()+1
        else:
            return False
        self.mazes.append(maze)
        return maze

    def get_maze(self, id):
        """Get a maze by its id.

            Args:
                id (int): The id of the desired maze

            Return:
                    Maze: Returns the maze if it was found.
                    None: If no maze was found
        """

        for maze in self.mazes:
            if maze.id == id:
                return maze
        print("Unable to locate maze")
        return None

    def get_mazes(self):
        """Get all of the mazes that the manager is holding"""
        return self.mazes

    def get_maze_count(self):
        """Gets the number of mazes that the manager is holding"""
        return self.mazes.__len__()

    def show_maze(self, id, cell_size=1):
        """Just show the generation animation and maze"""
        vis = Visualizer(self.get_maze(id), cell_size, self.media_name)
        vis.show_maze()

    def show_generation_animation(self, id, cell_size=1):
        vis = Visualizer(self.get_maze(id), cell_size, self.media_name)
        vis.show_generation_animation()

    def show_solution(self, id, cell_size=1):
        vis = Visualizer(self.get_maze(id), cell_size, self.media_name)
        vis.show_maze_solution()

    def show_solution_animation(self, id, cell_size =1):
        """ Shows the animation of the path that the solver took.

            Args:
                id (int): The id of the maze whose solution will be shown
                cell_size (int):
        """
        vis = Visualizer(self.get_maze(id), cell_size, self.media_name)
        vis.animate_maze_solution()

    def check_matching_id(self, id):
        """
            Check if the id already belongs to an existing maze
        """
        return next((maze for maze in self.mazes if maze .id == id), None)

    def set_filename(self, filename):
        """ Sets the filename for saving animations and images
            Args:
                filename (string): The name of the file without an extension
        """

        self.media_name = filename

    def set_quiet_mode(self, enabled):
        """ Enables/Disables the quiet mode
            Args:
                enabled (bool): True when quiet mode is on, False when it is off
        """
        self.quiet_mode=enabled
        
    def solve_maze(self, maze_id, method, heuristic_or_neighbor="fancy", neighbor_method="fancy"):
        """Called to solve a maze by a particular method.

        Args:
            maze_id (int): The id of the maze that will be solved
            method (string): The name of the method (DepthFirst, BreadthFirst, or AStar)
            heuristic_or_neighbor (string): For A*: heuristic method (Manhattan, Euclidean)
                                          For others: neighbor method (fancy or brute-force)
            neighbor_method (string): Only used for A*: method for choosing neighbors
        """
        maze = self.get_maze(maze_id)
        if maze is None:
            print("Unable to locate maze. Exiting solver.")
            return None
        
        maze.reset_solution()
        
        if method == "AStar":
            # For A*, properly order the parameters
            solver = AStar(maze, self.quiet_mode, neighbor_method, heuristic_or_neighbor)
            maze.solution_path = solver.solve()
        elif method == "DepthFirst":
            solver = DepthFirst(maze, self.quiet_mode, heuristic_or_neighbor)
            maze.solution_path = solver.solve()
        elif method == "BreadthFirst":
            solver = BreadthFirst(maze, self.quiet_mode, heuristic_or_neighbor)
            maze.solution_path = solver.solve()
        else:
            print(f"Unknown solving method: {method}")
            return None
            