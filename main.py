from __future__ import absolute_import
from src.maze_manager import MazeManager
from src.maze import Maze
import pickle

def save_maze_state(maze, filename="maze.pkl"):
    """Save the maze state to a file using pickle."""
    maze.reset_solution()
    with open(filename, "wb") as file:
        pickle.dump(maze, file)
    print(f"Maze saved to {filename}")

def load_maze_state(filename="maze.pkl"):
    """Load the maze state from a file."""
    with open(filename, "rb") as file:
        maze = pickle.load(file)
    print(f"Maze loaded from {filename}")
    maze.reset_solution()

    return maze

if __name__ == "__main__":

    # Initialize the MazeManager, which handles maze creation, solving, and visualization.
    manager = MazeManager()

    # IF we don't have a maze and need to create a new one:
    # maze = manager.add_maze(80, 80)
    # save_maze_state(maze)  

    # # IF we already have a saved maz e
    maze = load_maze_state()
    loaded_maze = manager.add_existing_maze(maze)
    # manager.show_maze(maze.id)
    
    # Solve the maze using an algorithm (e.g., BreadthFirst)
    # manager.solve_maze(maze.id, "DepthFirst")
    # manager.solve_maze(maze.id, "BreadthFirst")
    # manager.solve_maze(maze.id, "AStar", "Manhattan")
    manager.solve_maze(maze.id, "AStar", "Euclidean")

    # Show the solution animation.
    # manager.show_generation_animation(maze.id)
    # manager.show_solution_animation(maze.id)

    # Display the maze with the solution path.
    # manager.show_solution(maze.id)