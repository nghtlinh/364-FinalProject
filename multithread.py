import threading
from queue import Queue
from src.maze_manager import MazeManager

def solve_maze_with_algorithm(manager, maze_id, algorithm, heuristic, result_queue):
    """
    Solve a maze using a specific algorithm in a separate thread.
    Pass the result to the main thread via a queue.
    """
    try:
        if algorithm == "AStar":
            if not heuristic:
                raise ValueError("Heuristic must be specified for A* algorithm.")
            manager.solve_maze_with_A_Star(maze_id, algorithm, heuristic)
        else:
            manager.solve_maze(maze_id, algorithm)
        
        # Pass success status to the main thread
        result_queue.put((maze_id, algorithm, "success"))
    except Exception as e:
        # Pass error status to the main thread
        result_queue.put((maze_id, algorithm, f"error: {str(e)}"))

def reset_maze(manager, maze_id):
    """Reset maze state to ensure algorithms work independently."""
    maze = manager.get_maze(maze_id)
    for row in maze.grid:
        for cell in row:
            cell.visited = False
    maze.solution_path = None

if __name__ == "__main__":
    # Initialize the MazeManager
    manager = MazeManager()

    # Generate a single maze
    maze = manager.add_maze(20, 20)
    print(f"Generated maze with ID: {maze.id}")

    # Queue to receive results from threads
    result_queue = Queue()

    # Define the algorithms to use
    algorithms = [
        ("AStar", "Euclidean"),
        ("DepthFirst", None),
        ("BreadthFirst", None),
        ("AStar", "Manhattan"),
    ]

    # Create and start threads
    threads = []
    for idx, (algorithm, heuristic) in enumerate(algorithms):
        # Reset maze before solving with each algorithm
        reset_maze(manager, maze.id)
        t = threading.Thread(
            target=solve_maze_with_algorithm,
            args=(manager, maze.id, algorithm, heuristic, result_queue),
            name=f"SolverThread-{idx}"
        )
        threads.append(t)
        t.start()

    # Wait for threads to complete
    for t in threads:
        t.join()

    # Process results in the main thread
    while not result_queue.empty():
        maze_id, algorithm, status = result_queue.get()
        if "error" in status:
            print(f"Error solving maze {maze_id} with {algorithm}: {status}")
        else:
            print(f"Maze {maze_id} solved with {algorithm}. Showing solution animation...")
        try:
            manager.show_solution_animation(maze_id)
        except ValueError as e:
            print(f"Visualization failed for {algorithm} due to: {e}")
