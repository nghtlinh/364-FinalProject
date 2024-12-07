from __future__ import absolute_import
from src.maze_manager import MazeManager
from src.maze import Maze
import copy

if __name__ == "__main__":

    # # Initialize the MazeManager, which handles maze creation, solving, and visualization.
    # manager = MazeManager()

    # # Add a 10x10 maze to the manager.
    # maze = manager.add_maze(10, 10)

    # # Solve the maze using multiple algorithms
    # # manager.solve_maze(maze.id, "DepthFirst")
    # # manager.solve_maze(maze.id, "BreadthFirst")
    # manager.solve_maze_with_A_Star(maze.id, "AStar", "Manhattan")
    # # manager.solve_maze_with_A_Star(maze.id, "AStar", "Euclidean")

    # # if manager.solve_maze_with_A_Star(maze.id, "AStar", "Euclidean") is None:
    # #     print("A* algorithm failed to find a solution.")
    # # else:
    # #     manager.show_solution_animation(maze.id)

    # # Display the unsolved maze.
    # # manager.show_maze(maze.id)

    # # Display the maze with a custom cell size (default is 1).
    # # manager.show_maze(maze.id, 2)

    # # Show the maze generation animation.
    # # manager.show_generation_animation(maze.id)

    # # Show the solution animation.
    # manager.show_solution_animation(maze.id)

    # # Display the maze with the solution path.
    # manager.show_solution(maze.id)

# from __future__ import absolute_import
# from src.maze_manager import MazeManager
# from src.maze import Maze

# if __name__ == "__main__":
#     # Initialize the Maze Manager
    manager = MazeManager()

    original_maze = manager.add_maze(10, 10)

    # Add three identical mazes for comparison
    maze1 = copy.deepcopy(original_maze)
    maze2 = copy.deepcopy(original_maze)
    maze3 = copy.deepcopy(original_maze)
    maze4 = copy.deepcopy(original_maze)

    # Solve each maze with different algorithms
    # print("\nSolving using Breadth-First Search...")
    # manager.solve_maze(maze1.id, "BreadthFirst")
    # manager.show_solution_animation(maze1.id)
    
    # print("\nSolving using A* Euc Search...")
    # manager.solve_maze_with_A_Star(maze2.id, "AStar", "Euclidean")
    # manager.show_solution_animation(maze2.id)

    # print("\nSolving using A* Manh Search...")
    # manager.solve_maze(maze3.id, "AStar", "Manhattan")
    # manager.show_solution_animation(maze3.id)

    print("\nSolving using Depth-First Search...")
    manager.solve_maze(maze4.id, "DepthFirst")
    manager.show_solution_animation(maze4.id)

    # Optionally, show the final solved maze images
    # manager.show_solution(maze1.id)
    # manager.show_solution(maze2.id)
    # manager.show_solution(maze3.id)
    # manager.show_solution(maze4.id)
