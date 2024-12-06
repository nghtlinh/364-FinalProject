
from __future__ import absolute_import
from src.maze_manager import MazeManager
from src.maze import Maze


if __name__ == "__main__":

    # The easiest way to use the library is through the Manager class. It acts as the glue between
    # The visualization, solver, and maze classes. Mazes inside the manager have unique ids that we use
    # to specify particular mazes.
    manager = MazeManager()

    # We can add mazes to the manager two different ways.
    # The first way, we specify the maze dimensions. The maze that is created gets returned back to you.
    maze = manager.add_maze(10, 10)

    # Once we have a maze in the manager, we can tell the manager to solve it with a particular algorithm.
    #manager.solve_maze(maze.id, "DepthFirstBacktracker")
    #manager.solve_maze(maze.id, "BreadthFirstBiDirectional")
    #manager.solve_maze(maze.id, "BiDirectional")
    manager.solve_maze(maze.id, "AStar")

    # To see the unsolved maze, call
    # manager.show_maze(maze.id)

    # You can also set the size of the cell by passing show_maze's second argument. The default is 1.
    # manager.show_maze(maze.id, 2)

    # To show an animation of how the maze was generated, use the following line
    # manager.show_generation_animation(maze.id)

    # You can also see an animation of how the solver went about finding the end
    # manager.show_solution_animation(maze.id)

    # Finally, you can show an image of the maze with the solution path overlaid. All of these display
    # functions will save the figure if MazeManager::set_filename has been set.
    manager.show_solution(maze.id)