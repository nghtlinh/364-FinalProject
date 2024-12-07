from __future__ import absolute_import
from src.maze_manager import MazeManager
from src.maze import Maze
import pickle
import threading
import matplotlib.pyplot as plt
import queue

def save_maze_state(maze, filename="maze.pkl"):
    """Save the maze state to a file using pickle."""
    with open(filename, "wb") as file:
        pickle.dump(maze, file)
    print(f"Maze saved to {filename}")

def load_maze_state(filename="maze.pkl"):
    """Load the maze state from a file."""
    with open(filename, "rb") as file:
        maze = pickle.load(file)
    print(f"Maze loaded from {filename}")
    return maze

def solve_with_depth_first(manager, maze_id, result_queue):
    path = manager.solve_maze(maze_id, "DepthFirst")
    result_queue.put(("Depth First Search", path))

def solve_with_breadth_first(manager, maze_id, result_queue):
    path = manager.solve_maze(maze_id, "BreadthFirst")
    result_queue.put(("Breadth First Search", path))

def solve_with_a_star_manhattan(manager, maze_id, result_queue):
    path = manager.solve_maze_with_A_Star(maze_id, "AStar", "Manhattan")
    result_queue.put(("A* with Manhattan", path))

def solve_with_a_star_euclidean(manager, maze_id, result_queue):
    path = manager.solve_maze_with_A_Star(maze_id, "AStar", "Euclidean")
    result_queue.put(("A* with Euclidean", path))

def show_solution(maze, path, title):
    """Display the maze and its solution in a separate window using matplotlib."""
    fig, ax = plt.subplots()
    ax.imshow(maze.grid, cmap="binary")  # Display the maze grid

    # Mark the solution path
    for (x, y) in path:
        ax.plot(y, x, marker="o", color="red", markersize=5)

    ax.set_title(title)
    plt.show()

if __name__ == "__main__":
    # Initialize the MazeManager, which handles maze creation, solving, and visualization.
    manager = MazeManager()

    # Add a 10x10 maze to the manager.
    maze = manager.add_maze(10, 10)

    # Save the newly generated maze state.
    save_maze_state(maze)

    # Load the maze state (in case you want to reload the saved maze).
    loaded_maze = load_maze_state()

    # Create a queue to collect results from threads
    result_queue = queue.Queue()

    # Create threads to solve the maze with multiple algorithms
    threads = [
        threading.Thread(target=solve_with_depth_first, args=(manager, loaded_maze.id, result_queue)),
        threading.Thread(target=solve_with_breadth_first, args=(manager, loaded_maze.id, result_queue)),
        threading.Thread(target=solve_with_a_star_manhattan, args=(manager, loaded_maze.id, result_queue)),
        threading.Thread(target=solve_with_a_star_euclidean, args=(manager, loaded_maze.id, result_queue))
    ]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Collect results from the result queue
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    # # Show all solutions in separate windows on the main thread
    # for title, path in results:
    #     show_solution(loaded_maze, path, title)

    print("All algorithms have finished solving the maze.")
