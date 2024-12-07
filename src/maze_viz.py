# import matplotlib.pyplot as plt
# from matplotlib import animation
# import logging
# import warnings

# logging.getLogger('matplotlib').setLevel(logging.WARNING)
# logging.getLogger('PIL').setLevel(logging.WARNING)
# warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")


# class Visualizer(object):
#     """Class that handles all aspects of visualization.


#     Attributes:
#         maze: The maze that will be visualized
#         cell_size (int): How large the cells will be in the plots
#         height (int): The height of the maze
#         width (int): The width of the maze
#         ax: The axes for the plot
#         lines:
#         squares:

#     """
#     def __init__(self, maze, cell_size, media_filename):
#         self.maze = maze
#         self.cell_size = cell_size
#         self.height = maze.num_rows * cell_size
#         self.width = maze.num_cols * cell_size
#         self.ax = None
#         self.lines = dict()
#         self.squares = dict()


#     def show_maze(self):
#         """Displays a plot of the maze without the solution path"""

#         # Create the plot figure and style the axes
#         fig = self.configure_plot()

#         # Plot the walls on the figure
#         self.plot_walls()

#         # Display the plot to the user
#         plt.show()

#     def plot_walls(self):
#         """ Plots the walls of a maze. This is used when generating the maze image"""
#         for i in range(self.maze.num_rows):
#             for j in range(self.maze.num_cols):
#                 if self.maze.initial_grid[i][j].is_entry_exit == "entry":
#                     self.ax.text(j*self.cell_size, i*self.cell_size, "START", fontsize=7, weight="bold")
#                 elif self.maze.initial_grid[i][j].is_entry_exit == "exit":
#                     self.ax.text(j*self.cell_size, i*self.cell_size, "END", fontsize=7, weight="bold")
#                 if self.maze.initial_grid[i][j].walls["top"]:
#                     self.ax.plot([j*self.cell_size, (j+1)*self.cell_size],
#                                  [i*self.cell_size, i*self.cell_size], color="k")
#                 if self.maze.initial_grid[i][j].walls["right"]:
#                     self.ax.plot([(j+1)*self.cell_size, (j+1)*self.cell_size],
#                                  [i*self.cell_size, (i+1)*self.cell_size], color="k")
#                 if self.maze.initial_grid[i][j].walls["bottom"]:
#                     self.ax.plot([(j+1)*self.cell_size, j*self.cell_size],
#                                  [(i+1)*self.cell_size, (i+1)*self.cell_size], color="k")
#                 if self.maze.initial_grid[i][j].walls["left"]:
#                     self.ax.plot([j*self.cell_size, j*self.cell_size],
#                                  [(i+1)*self.cell_size, i*self.cell_size], color="k")

#     def configure_plot(self):
#         """Sets the initial properties of the maze plot. Also creates the plot and axes"""

#         # Create the plot figure
#         fig = plt.figure(figsize = (7, 7*self.maze.num_rows/self.maze.num_cols))

#         # Create the axes
#         self.ax = plt.axes()

#         # Set an equal aspect ratio
#         self.ax.set_aspect("equal")

#         # Remove the axes from the figure
#         self.ax.axes.get_xaxis().set_visible(False)
#         self.ax.axes.get_yaxis().set_visible(False)

#         title_box = self.ax.text(0, self.maze.num_rows + self.cell_size + 0.1,
#                             r"{}$\times${}".format(self.maze.num_rows, self.maze.num_cols),
#                             bbox={"facecolor": "gray", "alpha": 0.5, "pad": 4}, fontname="serif", fontsize=15)

#         return fig

#     # def show_maze_solution(self):
#     #     """Function that plots the solution to the maze. Also adds indication of entry and exit points."""

#     #      # Create the figure and style the axes
#     #     fig = self.configure_plot()

#     #     # Plot the walls onto the figure
#     #     self.plot_walls()

#     #     # Iterate through the solution path and add dotted circles
#     #     for idx, (cell, _) in enumerate(self.maze.solution_path):
#     #         # Calculate the center of the cell
#     #         center_x = (cell[1] + 0.5) * self.cell_size
#     #         center_y = (cell[0] + 0.5) * self.cell_size

#     #         # Add a dotted circle at the current cell position
#     #         self.ax.add_patch(plt.Circle((center_x, center_y), 0.2 * self.cell_size, 
#     #                                     color="green", alpha=0.6, linestyle='dotted'))

#     #     # Add labels for the start and end points
#     #     self.ax.text(self.cell_size / 2, self.cell_size / 2, "START", fontsize=10, fontweight="bold")
#     #     self.ax.text((self.maze.num_cols - 0.5) * self.cell_size, 
#     #                 (self.maze.num_rows - 0.5) * self.cell_size, "END", fontsize=10, fontweight="bold")

#     #     # Display the plot to the user
#     #     plt.show()

#     #     # Save the solution image if a filename is specified

#     def show_maze_solution(self):
#         """Plots the maze solution with a moving object, dashed lines, and backtracking markers."""
#         fig = self.configure_plot()
#         self.plot_walls()

#         # Add dashed lines for the solution path
#         for idx in range(1, len(self.maze.solution_path)):
#             prev_cell = self.maze.solution_path[idx - 1][0]
#             curr_cell = self.maze.solution_path[idx][0]

#             x_start = (prev_cell[1] + 0.5) * self.cell_size
#             y_start = (prev_cell[0] + 0.5) * self.cell_size
#             x_end = (curr_cell[1] + 0.5) * self.cell_size
#             y_end = (curr_cell[0] + 0.5) * self.cell_size

#             self.ax.plot([x_start, x_end], [y_start, y_end], linestyle="--", color="gray", linewidth=1.5)

#         # Add a small object at the start
#         curr_position = plt.Circle((0.5 * self.cell_size, 0.5 * self.cell_size), 0.2 * self.cell_size, color="blue", alpha=0.8)
#         self.ax.add_patch(curr_position)

#         # Handle backtracking with 'X'
#         for idx, (cell, is_backtracking) in enumerate(self.maze.solution_path):
#             center_x = (cell[1] + 0.5) * self.cell_size
#             center_y = (cell[0] + 0.5) * self.cell_size

#             if is_backtracking:
#                 # Place an 'X' for backtracking
#                 self.ax.text(center_x, center_y, "X", fontsize=10, fontweight="bold", color="red", ha="center", va="center")
#             else:
#                 # Move the object to the current position
#                 curr_position.center = (center_x, center_y)

#         # Add labels for the start and end points
#         self.ax.text(0.5 * self.cell_size, 0.5 * self.cell_size, "START", fontsize=10, fontweight="bold", color="black")
#         self.ax.text((self.maze.num_cols - 0.5) * self.cell_size,
#                      (self.maze.num_rows - 0.5) * self.cell_size, "END", fontsize=10, fontweight="bold", color="black")

#         plt.show(block=False)
    
#     def animate_maze_solution(self):
#         """Animates the maze solution, leaving a dashed trace for the path and marking backtracking with 'X'."""
#         fig = self.configure_plot()
#         self.plot_walls()

#         # Add the moving object (circle)
#         moving_object = plt.Circle((0.5 * self.cell_size, 0.5 * self.cell_size), 0.2 * self.cell_size, color="blue", alpha=0.8)
#         self.ax.add_patch(moving_object)

#         # Store the previous position for drawing the trace
#         prev_x, prev_y = None, None

#         def animate(frame):
#             """Update the moving object, trace, and backtracking markers."""
#             nonlocal prev_x, prev_y  # Allow modification of previous position
#             cell, is_backtracking = self.maze.solution_path[frame]

#             # Current position of the moving object
#             center_x = (cell[1] + 0.5) * self.cell_size
#             center_y = (cell[0] + 0.5) * self.cell_size

#             # Draw the trace
#             if prev_x is not None and prev_y is not None:
#                 if is_backtracking:
#                     # Place an 'X' for backtracking
#                     self.ax.text(prev_x, prev_y, "X", fontsize=12, fontweight="bold", color="red", ha="center", va="center")
#                 else:
#                     # Draw a dashed line for the path
#                     self.ax.plot([prev_x, center_x], [prev_y, center_y], linestyle="--", color="gray", linewidth=1.5)

#             # Update the moving object position
#             moving_object.center = (center_x, center_y)

#             # Update the previous position
#             prev_x, prev_y = center_x, center_y

#             return moving_object,

#         # Create the animation
#         anim = animation.FuncAnimation(
#             fig, animate, frames=len(self.maze.solution_path), interval=100, blit=False, repeat=False
#         )

#         plt.show()


#     # def show_generation_animation(self):
#     #     """Function that animates the process of generating the a maze where path is a list
#     #     of coordinates indicating the path taken to carve out (break down walls) the maze."""

#     #     # Create the figure and style the axes
#     #     fig = self.configure_plot()

#     #     # The square that represents the head of the algorithm
#     #     indicator = plt.Rectangle((self.maze.generation_path[0][0]*self.cell_size, self.maze.generation_path[0][1]*self.cell_size),
#     #         self.cell_size, self.cell_size, fc = "purple", alpha = 0.6)

#     #     self.ax.add_patch(indicator)

#     #     # Only need to plot right and bottom wall for each cell since walls overlap.
#     #     # Also adding squares to animate the path taken to carve out the maze.
#     #     color_walls = "k"
#     #     for i in range(self.maze.num_rows):
#     #         for j in range(self.maze.num_cols):
#     #             self.lines["{},{}: right".format(i, j)] = self.ax.plot([(j+1)*self.cell_size, (j+1)*self.cell_size],
#     #                     [i*self.cell_size, (i+1)*self.cell_size],
#     #                 linewidth = 2, color = color_walls)[0]
#     #             self.lines["{},{}: bottom".format(i, j)] = self.ax.plot([(j+1)*self.cell_size, j*self.cell_size],
#     #                     [(i+1)*self.cell_size, (i+1)*self.cell_size],
#     #                 linewidth = 2, color = color_walls)[0]

#     #             self.squares["{},{}".format(i, j)] = plt.Rectangle((j*self.cell_size,
#     #                 i*self.cell_size), self.cell_size, self.cell_size, fc = "red", alpha = 0.4)
#     #             self.ax.add_patch(self.squares["{},{}".format(i, j)])

#     #     # Plotting boundaries of maze.
#     #     color_boundary = "k"
#     #     self.ax.plot([0, self.width], [self.height,self.height], linewidth = 2, color = color_boundary)
#     #     self.ax.plot([self.width, self.width], [self.height, 0], linewidth = 2, color = color_boundary)
#     #     self.ax.plot([self.width, 0], [0, 0], linewidth = 2, color = color_boundary)
#     #     self.ax.plot([0, 0], [0, self.height], linewidth = 2, color = color_boundary)

#     #     def animate(frame):
#     #         """Function to supervise animation of all objects."""
#     #         animate_walls(frame)
#     #         animate_squares(frame)
#     #         animate_indicator(frame)
#     #         self.ax.set_title("Step: {}".format(frame + 1), fontname="serif", fontsize=19)
#     #         return []

#     #     def animate_walls(frame):
#     #         """Function that animates the visibility of the walls between cells."""
#     #         if frame > 0:
#     #             self.maze.grid[self.maze.generation_path[frame-1][0]][self.maze.generation_path[frame-1][1]].remove_walls(
#     #                 self.maze.generation_path[frame][0],
#     #                 self.maze.generation_path[frame][1])   # Wall between curr and neigh

#     #             self.maze.grid[self.maze.generation_path[frame][0]][self.maze.generation_path[frame][1]].remove_walls(
#     #                 self.maze.generation_path[frame-1][0],
#     #                 self.maze.generation_path[frame-1][1])   # Wall between neigh and curr

#     #             current_cell = self.maze.grid[self.maze.generation_path[frame-1][0]][self.maze.generation_path[frame-1][1]]
#     #             next_cell = self.maze.grid[self.maze.generation_path[frame][0]][self.maze.generation_path[frame][1]]

#     #             """Function to animate walls between cells as the search goes on."""
#     #             for wall_key in ["right", "bottom"]:    # Only need to draw two of the four walls (overlap)
#     #                 if current_cell.walls[wall_key] is False:
#     #                     self.lines["{},{}: {}".format(current_cell.row,
#     #                         current_cell.col, wall_key)].set_visible(False)
#     #                 if next_cell.walls[wall_key] is False:
#     #                     self.lines["{},{}: {}".format(next_cell.row,
#     #                                              next_cell.col, wall_key)].set_visible(False)

#     #     def animate_squares(frame):
#     #         """Function to animate the searched path of the algorithm."""
#     #         self.squares["{},{}".format(self.maze.generation_path[frame][0],
#     #                                self.maze.generation_path[frame][1])].set_visible(False)
#     #         return []

#     #     def animate_indicator(frame):
#     #         """Function to animate where the current search is happening."""
#     #         indicator.set_xy((self.maze.generation_path[frame][1]*self.cell_size,
#     #                           self.maze.generation_path[frame][0]*self.cell_size))
#     #         return []

#     #     logging.debug("Creating generation animation")
#     #     anim = animation.FuncAnimation(fig, animate, frames=self.maze.generation_path.__len__(),
#     #                                    interval=100, blit=True, repeat=False)

#     #     logging.debug("Finished creating the generation animation")

#     #     # Display the plot to the user
#     #     plt.show()

#     def add_path(self):
#         # Adding squares to animate the path taken to solve the maze. Also adding entry/exit text
#         color_walls = "k"
#         for i in range(self.maze.num_rows):
#             for j in range(self.maze.num_cols):
#                 if self.maze.initial_grid[i][j].is_entry_exit == "entry":
#                     self.ax.text(j*self.cell_size, i*self.cell_size, "START", fontsize = 7, weight = "bold")
#                 elif self.maze.initial_grid[i][j].is_entry_exit == "exit":
#                     self.ax.text(j*self.cell_size, i*self.cell_size, "END", fontsize = 7, weight = "bold")

#                 if self.maze.initial_grid[i][j].walls["top"]:
#                     self.lines["{},{}: top".format(i, j)] = self.ax.plot([j*self.cell_size, (j+1)*self.cell_size],
#                          [i*self.cell_size, i*self.cell_size], linewidth = 1, color = color_walls)[0]
#                 if self.maze.initial_grid[i][j].walls["right"]:
#                     self.lines["{},{}: right".format(i, j)] = self.ax.plot([(j+1)*self.cell_size, (j+1)*self.cell_size],
#                          [i*self.cell_size, (i+1)*self.cell_size], linewidth = 1, color = color_walls)[0]
#                 if self.maze.initial_grid[i][j].walls["bottom"]:
#                     self.lines["{},{}: bottom".format(i, j)] = self.ax.plot([(j+1)*self.cell_size, j*self.cell_size],
#                          [(i+1)*self.cell_size, (i+1)*self.cell_size], linewidth = 1, color = color_walls)[0]
#                 if self.maze.initial_grid[i][j].walls["left"]:
#                     self.lines["{},{}: left".format(i, j)] = self.ax.plot([j*self.cell_size, j*self.cell_size],
#                              [(i+1)*self.cell_size, i*self.cell_size], linewidth = 1, color = color_walls)[0]
#                 self.squares["{},{}".format(i, j)] = plt.Rectangle((j*self.cell_size,
#                                                                     i*self.cell_size), self.cell_size, self.cell_size,
#                                                                    fc = "red", alpha = 0.4, visible = False)
#                 self.ax.add_patch(self.squares["{},{}".format(i, j)])

#     # def animate_maze_solution(self):
#     #     """Function that animates the process of generating the a maze where path is a list
#     #     of coordinates indicating the path taken to carve out (break down walls) the maze."""

#     #     # Create the figure and style the axes
#     #     fig = self.configure_plot()

#     #     # Adding indicator to see shere current search is happening.
#     #     indicator = plt.Rectangle((self.maze.solution_path[0][0][0]*self.cell_size,
#     #                                self.maze.solution_path[0][0][1]*self.cell_size), self.cell_size, self.cell_size,
#     #                               fc="purple", alpha=0.6)
#     #     self.ax.add_patch(indicator)

#     #     self.add_path()

#     #     def animate_squares(frame):
#     #         """Function to animate the solved path of the algorithm."""
#     #         if frame > 0:
#     #             if self.maze.solution_path[frame - 1][1]:  # Color backtracking
#     #                 self.squares["{},{}".format(self.maze.solution_path[frame - 1][0][0],
#     #                                        self.maze.solution_path[frame - 1][0][1])].set_facecolor("green")

#     #             self.squares["{},{}".format(self.maze.solution_path[frame - 1][0][0],
#     #                                    self.maze.solution_path[frame - 1][0][1])].set_visible(True)
#     #             self.squares["{},{}".format(self.maze.solution_path[frame][0][0],
#     #                                    self.maze.solution_path[frame][0][1])].set_visible(False)
#     #         return []

#     #     def animate_indicator(frame):
#     #         """Function to animate where the current search is happening."""
#     #         indicator.set_xy((self.maze.solution_path[frame][0][1] * self.cell_size,
#     #                           self.maze.solution_path[frame][0][0] * self.cell_size))
#     #         return []

#     #     def animate(frame):
#     #         """Function to supervise animation of all objects."""
#     #         animate_squares(frame)
#     #         animate_indicator(frame)
#     #         self.ax.set_title("Step: {}".format(frame + 1), fontname = "serif", fontsize = 19)
#     #         return []

#     #     logging.debug("Creating solution animation")
#     #     anim = animation.FuncAnimation(fig, animate, frames=self.maze.solution_path.__len__(),
#     #                                    interval=100, blit=True, repeat=False)
#     #     logging.debug("Finished creating solution animation")

#     #     # Display the animation to the user
#     #     plt.show()

#     #     # Handle any saving
#     #     if self.media_filename:
#     #         print("Saving solution animation. This may take a minute....")
#     #         mpeg_writer = animation.FFMpegWriter(fps=24, bitrate=1000,
#     #                                              codec="libx264", extra_args=["-pix_fmt", "yuv420p"])
#     #         anim.save("{}{}{}x{}.mp4".format(self.media_filename, "_solution_", self.maze.num_rows,
#     #                                        self.maze.num_cols), writer=mpeg_writer)

# # import matplotlib.pyplot as plt
# # from matplotlib import animation
# # import logging

# # logging.basicConfig(level=logging.DEBUG)

# # class Visualizer(object):
# #     """Class that handles all aspects of visualization."""
    
# #     def __init__(self, maze, cell_size, media_filename):
# #         self.maze = maze
# #         self.cell_size = cell_size
# #         self.height = maze.num_rows * cell_size
# #         self.width = maze.num_cols * cell_size
# #         self.ax = None
# #         self.lines = dict()
# #         self.squares = dict()
# #         self.media_filename = media_filename

# #     def configure_plot(self):
# #         """Sets the initial properties of the maze plot and creates the axes."""
# #         fig = plt.figure(figsize=(7, 7 * self.maze.num_rows / self.maze.num_cols))
# #         self.ax = plt.axes()
# #         self.ax.set_aspect("equal")
# #         self.ax.axis("off")
# #         return fig

# #     def plot_walls(self):
# #         """Plots the walls of the maze."""
# #         for i in range(self.maze.num_rows):
# #             for j in range(self.maze.num_cols):
# #                 if self.maze.initial_grid[i][j].is_entry_exit == "entry":
# #                     self.ax.text(j * self.cell_size, i * self.cell_size, "START", fontsize=7, weight="bold")
# #                 elif self.maze.initial_grid[i][j].is_entry_exit == "exit":
# #                     self.ax.text(j * self.cell_size, i * self.cell_size, "END", fontsize=7, weight="bold")
# #                 if self.maze.initial_grid[i][j].walls["top"]:
# #                     self.ax.plot([j * self.cell_size, (j + 1) * self.cell_size],
# #                                  [i * self.cell_size, i * self.cell_size], color="k")
# #                 if self.maze.initial_grid[i][j].walls["right"]:
# #                     self.ax.plot([(j + 1) * self.cell_size, (j + 1) * self.cell_size],
# #                                  [i * self.cell_size, (i + 1) * self.cell_size], color="k")
# #                 if self.maze.initial_grid[i][j].walls["bottom"]:
# #                     self.ax.plot([(j + 1) * self.cell_size, j * self.cell_size],
# #                                  [(i + 1) * self.cell_size, (i + 1) * self.cell_size], color="k")
# #                 if self.maze.initial_grid[i][j].walls["left"]:
# #                     self.ax.plot([j * self.cell_size, j * self.cell_size],
# #                                  [(i + 1) * self.cell_size, i * self.cell_size], color="k")

#     # def show_maze_solution(self):
#     #     """Plots the maze solution with a moving object, dashed lines, and backtracking markers."""
#     #     fig = self.configure_plot()
#     #     self.plot_walls()

#     #     # Add dashed lines for the solution path
#     #     for idx in range(1, len(self.maze.solution_path)):
#     #         prev_cell = self.maze.solution_path[idx - 1][0]
#     #         curr_cell = self.maze.solution_path[idx][0]

#     #         x_start = (prev_cell[1] + 0.5) * self.cell_size
#     #         y_start = (prev_cell[0] + 0.5) * self.cell_size
#     #         x_end = (curr_cell[1] + 0.5) * self.cell_size
#     #         y_end = (curr_cell[0] + 0.5) * self.cell_size

#     #         self.ax.plot([x_start, x_end], [y_start, y_end], linestyle="--", color="gray", linewidth=1.5)

#     #     # Add a small object at the start
#     #     curr_position = plt.Circle((0.5 * self.cell_size, 0.5 * self.cell_size), 0.2 * self.cell_size, color="blue", alpha=0.8)
#     #     self.ax.add_patch(curr_position)

#     #     # Handle backtracking with 'X'
#     #     for idx, (cell, is_backtracking) in enumerate(self.maze.solution_path):
#     #         center_x = (cell[1] + 0.5) * self.cell_size
#     #         center_y = (cell[0] + 0.5) * self.cell_size

#     #         if is_backtracking:
#     #             # Place an 'X' for backtracking
#     #             self.ax.text(center_x, center_y, "X", fontsize=12, fontweight="bold", color="red", ha="center", va="center")
#     #         else:
#     #             # Move the object to the current position
#     #             curr_position.center = (center_x, center_y)

#     #     # Add labels for the start and end points
#     #     self.ax.text(0.5 * self.cell_size, 0.5 * self.cell_size, "START", fontsize=10, fontweight="bold", color="black")
#     #     self.ax.text((self.maze.num_cols - 0.5) * self.cell_size,
#     #                  (self.maze.num_rows - 0.5) * self.cell_size, "END", fontsize=10, fontweight="bold", color="black")

#     #     plt.show(block=False)

#     #     if self.media_filename:
#     #         fig.savefig(f"{self.media_filename}_solution_path.png", bbox_inches="tight")
    
#     # def animate_maze_solution(self):
#     #     """Animates the maze solution, leaving a dashed trace for the path and marking backtracking with 'X'."""
#     #     fig = self.configure_plot()
#     #     self.plot_walls()

#     #     # Add the moving object (circle)
#     #     moving_object = plt.Circle((0.5 * self.cell_size, 0.5 * self.cell_size), 0.2 * self.cell_size, color="blue", alpha=0.8)
#     #     self.ax.add_patch(moving_object)

#     #     # Store the previous position for drawing the trace
#     #     prev_x, prev_y = None, None

#     #     def animate(frame):
#     #         """Update the moving object, trace, and backtracking markers."""
#     #         nonlocal prev_x, prev_y  # Allow modification of previous position
#     #         cell, is_backtracking = self.maze.solution_path[frame]

#     #         # Current position of the moving object
#     #         center_x = (cell[1] + 0.5) * self.cell_size
#     #         center_y = (cell[0] + 0.5) * self.cell_size

#     #         # Draw the trace
#     #         if prev_x is not None and prev_y is not None:
#     #             if is_backtracking:
#     #                 # Place an 'X' for backtracking
#     #                 self.ax.text(prev_x, prev_y, "X", fontsize=12, fontweight="bold", color="red", ha="center", va="center")
#     #             else:
#     #                 # Draw a dashed line for the path
#     #                 self.ax.plot([prev_x, center_x], [prev_y, center_y], linestyle="--", color="gray", linewidth=1.5)

#     #         # Update the moving object position
#     #         moving_object.center = (center_x, center_y)

#     #         # Update the previous position
#     #         prev_x, prev_y = center_x, center_y

#     #         return moving_object,

#     #     # Create the animation
#     #     anim = animation.FuncAnimation(
#     #         fig, animate, frames=len(self.maze.solution_path), interval=100, blit=False, repeat=False
#     #     )

#     #     plt.show()

#     #     # Save the animation if a filename is specified
#     #     if self.media_filename:
#     #         anim.save(f"{self.media_filename}_solution_animation.gif", writer="pillow", fps=30)



import matplotlib.pyplot as plt
from matplotlib import animation
import logging

logging.basicConfig(level=logging.DEBUG)


class Visualizer(object):
    """Class that handles all aspects of visualization.


    Attributes:
        maze: The maze that will be visualized
        cell_size (int): How large the cells will be in the plots
        height (int): The height of the maze
        width (int): The width of the maze
        ax: The axes for the plot
        lines:
        squares:
        media_filename (string): The name of the animations and images

    """
    def __init__(self, maze, cell_size, media_filename):
        self.maze = maze
        self.cell_size = cell_size
        self.height = maze.num_rows * cell_size
        self.width = maze.num_cols * cell_size
        self.ax = None
        self.lines = dict()
        self.squares = dict()


    def show_maze(self):
        """Displays a plot of the maze without the solution path"""

        # Create the plot figure and style the axes
        fig = self.configure_plot()

        # Plot the walls on the figure
        self.plot_walls()

        # Display the plot to the user
        plt.show()

    def plot_walls(self):
        """ Plots the walls of a maze. This is used when generating the maze image"""
        for i in range(self.maze.num_rows):
            for j in range(self.maze.num_cols):
                if self.maze.initial_grid[i][j].is_entry_exit == "entry":
                    self.ax.text(j*self.cell_size, i*self.cell_size, "START", fontsize=7, weight="bold")
                elif self.maze.initial_grid[i][j].is_entry_exit == "exit":
                    self.ax.text(j*self.cell_size, i*self.cell_size, "END", fontsize=7, weight="bold")
                if self.maze.initial_grid[i][j].walls["top"]:
                    self.ax.plot([j*self.cell_size, (j+1)*self.cell_size],
                                 [i*self.cell_size, i*self.cell_size], color="k")
                if self.maze.initial_grid[i][j].walls["right"]:
                    self.ax.plot([(j+1)*self.cell_size, (j+1)*self.cell_size],
                                 [i*self.cell_size, (i+1)*self.cell_size], color="k")
                if self.maze.initial_grid[i][j].walls["bottom"]:
                    self.ax.plot([(j+1)*self.cell_size, j*self.cell_size],
                                 [(i+1)*self.cell_size, (i+1)*self.cell_size], color="k")
                if self.maze.initial_grid[i][j].walls["left"]:
                    self.ax.plot([j*self.cell_size, j*self.cell_size],
                                 [(i+1)*self.cell_size, i*self.cell_size], color="k")

    def configure_plot(self):
        """Sets the initial properties of the maze plot. Also creates the plot and axes"""

        # Create the plot figure
        fig = plt.figure(figsize = (7, 7*self.maze.num_rows/self.maze.num_cols))

        # Create the axes
        self.ax = plt.axes()

        # Set an equal aspect ratio
        self.ax.set_aspect("equal")

        # Remove the axes from the figure
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        title_box = self.ax.text(0, self.maze.num_rows + self.cell_size + 0.1,
                            r"{}$\times${}".format(self.maze.num_rows, self.maze.num_cols),
                            bbox={"facecolor": "gray", "alpha": 0.5, "pad": 4}, fontname="serif", fontsize=15)

        return fig

    # def show_maze_solution(self):
    #     """Function that plots the solution to the maze. Also adds indication of entry and exit points."""

    #      # Create the figure and style the axes
    #     fig = self.configure_plot()

    #     # Plot the walls onto the figure
    #     self.plot_walls()

    #     # Iterate through the solution path and add dotted circles
    #     for idx, (cell, _) in enumerate(self.maze.solution_path):
    #         # Calculate the center of the cell
    #         center_x = (cell[1] + 0.5) * self.cell_size
    #         center_y = (cell[0] + 0.5) * self.cell_size

    #         # Add a dotted circle at the current cell position
    #         self.ax.add_patch(plt.Circle((center_x, center_y), 0.2 * self.cell_size, 
    #                                     color="green", alpha=0.6, linestyle='dotted'))

    #     # Add labels for the start and end points
    #     self.ax.text(self.cell_size / 2, self.cell_size / 2, "START", fontsize=10, fontweight="bold")
    #     self.ax.text((self.maze.num_cols - 0.5) * self.cell_size, 
    #                 (self.maze.num_rows - 0.5) * self.cell_size, "END", fontsize=10, fontweight="bold")

    #     # Display the plot to the user
    #     plt.show()

    #     # Save the solution image if a filename is specified
    #     if self.media_filename:
    #         fig.savefig(f"{self.media_filename}_solution.png", bbox_inches="tight")

    def show_maze_solution(self):
        """Function that plots the solution to the maze with a moving object, backtracking markers, and dashed lines."""

        # Create the figure and style the axes
        fig = self.configure_plot()

        # Plot the walls onto the figure
        self.plot_walls()

        # Add dashed lines for the solution path
        for idx in range(1, len(self.maze.solution_path)):
            prev_cell = self.maze.solution_path[idx - 1][0]
            curr_cell = self.maze.solution_path[idx][0]

            # Get the coordinates for dashed lines
            x_start = (prev_cell[1] + 0.5) * self.cell_size
            y_start = (prev_cell[0] + 0.5) * self.cell_size
            x_end = (curr_cell[1] + 0.5) * self.cell_size
            y_end = (curr_cell[0] + 0.5) * self.cell_size

            # Add a dashed line
            self.ax.plot([x_start, x_end], [y_start, y_end], linestyle="--", color="gray", linewidth=1.5)

        # Add a small object at the start
        curr_position = plt.Circle((0.5 * self.cell_size, 0.5 * self.cell_size), 0.2 * self.cell_size, color="blue", alpha=0.8)
        self.ax.add_patch(curr_position)

        # Handle backtracking with 'X'
        for idx, (cell, is_backtracking) in enumerate(self.maze.solution_path):
            center_x = (cell[1] + 0.5) * self.cell_size
            center_y = (cell[0] + 0.5) * self.cell_size

            if is_backtracking:
                # Place an 'X' for backtracking
                self.ax.text(center_x, center_y, "X", fontsize=12, fontweight="bold", color="red", ha="center", va="center")
            else:
                # Move the object to the current position
                curr_position.center = (center_x, center_y)

        # Add labels for the start and end points
        self.ax.text(0.5 * self.cell_size, 0.5 * self.cell_size, "START", fontsize=10, fontweight="bold", color="black")
        self.ax.text((self.maze.num_cols - 0.5) * self.cell_size,
                    (self.maze.num_rows - 0.5) * self.cell_size, "END", fontsize=10, fontweight="bold", color="black")

        # Display the plot to the user
        plt.show()




    def show_generation_animation(self):
        """Function that animates the process of generating the a maze where path is a list
        of coordinates indicating the path taken to carve out (break down walls) the maze."""

        # Create the figure and style the axes
        fig = self.configure_plot()

        # The square that represents the head of the algorithm
        indicator = plt.Rectangle((self.maze.generation_path[0][0]*self.cell_size, self.maze.generation_path[0][1]*self.cell_size),
            self.cell_size, self.cell_size, fc = "purple", alpha = 0.6)

        self.ax.add_patch(indicator)

        # Only need to plot right and bottom wall for each cell since walls overlap.
        # Also adding squares to animate the path taken to carve out the maze.
        color_walls = "k"
        for i in range(self.maze.num_rows):
            for j in range(self.maze.num_cols):
                self.lines["{},{}: right".format(i, j)] = self.ax.plot([(j+1)*self.cell_size, (j+1)*self.cell_size],
                        [i*self.cell_size, (i+1)*self.cell_size],
                    linewidth = 2, color = color_walls)[0]
                self.lines["{},{}: bottom".format(i, j)] = self.ax.plot([(j+1)*self.cell_size, j*self.cell_size],
                        [(i+1)*self.cell_size, (i+1)*self.cell_size],
                    linewidth = 2, color = color_walls)[0]

                self.squares["{},{}".format(i, j)] = plt.Rectangle((j*self.cell_size,
                    i*self.cell_size), self.cell_size, self.cell_size, fc = "red", alpha = 0.4)
                self.ax.add_patch(self.squares["{},{}".format(i, j)])

        # Plotting boundaries of maze.
        color_boundary = "k"
        self.ax.plot([0, self.width], [self.height,self.height], linewidth = 2, color = color_boundary)
        self.ax.plot([self.width, self.width], [self.height, 0], linewidth = 2, color = color_boundary)
        self.ax.plot([self.width, 0], [0, 0], linewidth = 2, color = color_boundary)
        self.ax.plot([0, 0], [0, self.height], linewidth = 2, color = color_boundary)

        def animate(frame):
            """Function to supervise animation of all objects."""
            animate_walls(frame)
            animate_squares(frame)
            animate_indicator(frame)
            self.ax.set_title("Step: {}".format(frame + 1), fontname="serif", fontsize=19)
            return []

        def animate_walls(frame):
            """Function that animates the visibility of the walls between cells."""
            if frame > 0:
                self.maze.grid[self.maze.generation_path[frame-1][0]][self.maze.generation_path[frame-1][1]].remove_walls(
                    self.maze.generation_path[frame][0],
                    self.maze.generation_path[frame][1])   # Wall between curr and neigh

                self.maze.grid[self.maze.generation_path[frame][0]][self.maze.generation_path[frame][1]].remove_walls(
                    self.maze.generation_path[frame-1][0],
                    self.maze.generation_path[frame-1][1])   # Wall between neigh and curr

                current_cell = self.maze.grid[self.maze.generation_path[frame-1][0]][self.maze.generation_path[frame-1][1]]
                next_cell = self.maze.grid[self.maze.generation_path[frame][0]][self.maze.generation_path[frame][1]]

                """Function to animate walls between cells as the search goes on."""
                for wall_key in ["right", "bottom"]:    # Only need to draw two of the four walls (overlap)
                    if current_cell.walls[wall_key] is False:
                        self.lines["{},{}: {}".format(current_cell.row,
                            current_cell.col, wall_key)].set_visible(False)
                    if next_cell.walls[wall_key] is False:
                        self.lines["{},{}: {}".format(next_cell.row,
                                                 next_cell.col, wall_key)].set_visible(False)

        def animate_squares(frame):
            """Function to animate the searched path of the algorithm."""
            self.squares["{},{}".format(self.maze.generation_path[frame][0],
                                   self.maze.generation_path[frame][1])].set_visible(False)
            return []

        def animate_indicator(frame):
            """Function to animate where the current search is happening."""
            indicator.set_xy((self.maze.generation_path[frame][1]*self.cell_size,
                              self.maze.generation_path[frame][0]*self.cell_size))
            return []

        logging.debug("Creating generation animation")
        anim = animation.FuncAnimation(fig, animate, frames=self.maze.generation_path.__len__(),
                                       interval=100, blit=True, repeat=False)

        logging.debug("Finished creating the generation animation")

        # Display the plot to the user
        plt.show()

    def add_path(self):
        # Adding squares to animate the path taken to solve the maze. Also adding entry/exit text
        color_walls = "k"
        for i in range(self.maze.num_rows):
            for j in range(self.maze.num_cols):
                if self.maze.initial_grid[i][j].is_entry_exit == "entry":
                    self.ax.text(j*self.cell_size, i*self.cell_size, "START", fontsize = 7, weight = "bold")
                elif self.maze.initial_grid[i][j].is_entry_exit == "exit":
                    self.ax.text(j*self.cell_size, i*self.cell_size, "END", fontsize = 7, weight = "bold")

                if self.maze.initial_grid[i][j].walls["top"]:
                    self.lines["{},{}: top".format(i, j)] = self.ax.plot([j*self.cell_size, (j+1)*self.cell_size],
                         [i*self.cell_size, i*self.cell_size], linewidth = 1, color = color_walls)[0]
                if self.maze.initial_grid[i][j].walls["right"]:
                    self.lines["{},{}: right".format(i, j)] = self.ax.plot([(j+1)*self.cell_size, (j+1)*self.cell_size],
                         [i*self.cell_size, (i+1)*self.cell_size], linewidth = 1, color = color_walls)[0]
                if self.maze.initial_grid[i][j].walls["bottom"]:
                    self.lines["{},{}: bottom".format(i, j)] = self.ax.plot([(j+1)*self.cell_size, j*self.cell_size],
                         [(i+1)*self.cell_size, (i+1)*self.cell_size], linewidth = 1, color = color_walls)[0]
                if self.maze.initial_grid[i][j].walls["left"]:
                    self.lines["{},{}: left".format(i, j)] = self.ax.plot([j*self.cell_size, j*self.cell_size],
                             [(i+1)*self.cell_size, i*self.cell_size], linewidth = 1, color = color_walls)[0]
                self.squares["{},{}".format(i, j)] = plt.Rectangle((j*self.cell_size,
                                                                    i*self.cell_size), self.cell_size, self.cell_size,
                                                                   fc = "green", alpha = 0.4, visible = False)
                self.ax.add_patch(self.squares["{},{}".format(i, j)])

    def animate_maze_solution(self):
        """"Function to animate the maze solution path."""
        if not self.maze.solution_path:
            logging.error("No solution path found. Cannot animate the solution.")
            print("No solution found for the maze.")
            return

        # Create the figure and style the axes
        fig = self.configure_plot()

        # Adding indicator to see where the current search is happening
        indicator = plt.Rectangle((self.maze.solution_path[0][0][0] * self.cell_size,
                                self.maze.solution_path[0][0][1] * self.cell_size),
                                self.cell_size, self.cell_size, fc="purple", alpha=0.6)
        self.ax.add_patch(indicator)

        self.add_path()

        def animate_squares(frame):
            """Function to animate the solved path of the algorithm."""
            if frame > 0:
                if self.maze.solution_path[frame - 1][1]:  # Color backtracking
                    self.squares["{},{}".format(self.maze.solution_path[frame - 1][0][0],
                                           self.maze.solution_path[frame - 1][0][1])].set_facecolor("red")

                self.squares["{},{}".format(self.maze.solution_path[frame - 1][0][0],
                                       self.maze.solution_path[frame - 1][0][1])].set_visible(True)
                self.squares["{},{}".format(self.maze.solution_path[frame][0][0],
                                       self.maze.solution_path[frame][0][1])].set_visible(False)
            return []

        def animate_indicator(frame):
            """Function to animate where the current search is happening."""
            indicator.set_xy((self.maze.solution_path[frame][0][1] * self.cell_size,
                              self.maze.solution_path[frame][0][0] * self.cell_size))
            return []

        def animate(frame):
            """Function to supervise animation of all objects."""
            animate_squares(frame)
            animate_indicator(frame)
            self.ax.set_title("Step: {}".format(frame + 1), fontname = "serif", fontsize = 19)
            return []

        logging.debug("Creating solution animation")
        anim = animation.FuncAnimation(fig, animate, frames=self.maze.solution_path.__len__(),
                                       interval=100, blit=True, repeat=False)
        logging.debug("Finished creating solution animation")

        # Display the animation to the user
        plt.show()