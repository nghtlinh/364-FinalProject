from __future__ import absolute_import
from src.maze_manager import MazeManager
from src.maze import Maze

if __name__ == "__main__":

    # Initialize the MazeManager, which handles maze creation, solving, and visualization.
    manager = MazeManager()

    # Add a 10x10 maze to the manager.
    maze = manager.add_maze(10, 10)

    # Solve the maze using multiple algorithms
    manager.solve_maze(maze.id, "DepthFirst")
    # manager.solve_maze(maze.id, "BreadthFirst")
    # manager.solve_maze_with_A_Star(maze.id, "AStar", "Manhattan")
    # manager.solve_maze_with_A_Star(maze.id, "AStar", "Euclidean")

    # Display the unsolved maze.
    # manager.show_maze(maze.id)

    # Display the maze with a custom cell size (default is 1).
    # manager.show_maze(maze.id, 2)

    # Show the maze generation animation.
    # manager.show_generation_animation(maze.id)

    # Show the solution animation.
    manager.show_solution_animation(maze.id)

    # Display the maze with the solution path.
    # manager.show_solution(maze.id)
