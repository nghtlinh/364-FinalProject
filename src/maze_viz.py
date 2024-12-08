import matplotlib.pyplot as plt
from matplotlib import animation
import logging
import warnings

logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.getLogger('PIL').setLevel(logging.WARNING)
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")


class Visualizer(object):
    """Class that handles all aspects of visualization."""
    
    def __init__(self, maze, cell_size, media_filename):
        self.maze = maze
        self.cell_size = cell_size
        self.height = maze.num_rows * cell_size
        self.width = maze.num_cols * cell_size
        self.ax = None
        self.lines = dict()
        self.squares = dict()
        self.media_filename = media_filename

    def configure_plot(self):
        """Sets the initial properties of the maze plot and creates the axes."""
        fig = plt.figure(figsize=(7, 7 * self.maze.num_rows / self.maze.num_cols))
        self.ax = plt.axes()
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        return fig

    def plot_walls(self):
        """Plots the walls of the maze."""
        for i in range(self.maze.num_rows):
            for j in range(self.maze.num_cols):
                if self.maze.initial_grid[i][j].is_entry_exit == "entry":
                    self.ax.text(j * self.cell_size, i * self.cell_size, "START", fontsize=7, weight="bold")
                elif self.maze.initial_grid[i][j].is_entry_exit == "exit":
                    self.ax.text(j * self.cell_size, i * self.cell_size, "END", fontsize=7, weight="bold")
                if self.maze.initial_grid[i][j].walls["top"]:
                    self.ax.plot([j * self.cell_size, (j + 1) * self.cell_size],
                                 [i * self.cell_size, i * self.cell_size], color="k")
                if self.maze.initial_grid[i][j].walls["right"]:
                    self.ax.plot([(j + 1) * self.cell_size, (j + 1) * self.cell_size],
                                 [i * self.cell_size, (i + 1) * self.cell_size], color="k")
                if self.maze.initial_grid[i][j].walls["bottom"]:
                    self.ax.plot([(j + 1) * self.cell_size, j * self.cell_size],
                                 [(i + 1) * self.cell_size, (i + 1) * self.cell_size], color="k")
                if self.maze.initial_grid[i][j].walls["left"]:
                    self.ax.plot([j * self.cell_size, j * self.cell_size],
                                 [(i + 1) * self.cell_size, i * self.cell_size], color="k")

    def show_maze_solution(self):
        """Plots the maze solution with a moving object, dashed lines, and backtracking markers."""
        fig = self.configure_plot()
        self.plot_walls()

        list_of_backtrackers = [path_element[0] for path_element in self.maze.solution_path if path_element[1]]

        # Keeps track of how many circles have been drawn
        circle_num = 0

        self.ax.add_patch(plt.Circle(((self.maze.solution_path[0][0][1] + 0.5)*self.cell_size,
                                      (self.maze.solution_path[0][0][0] + 0.5)*self.cell_size), 0.2*self.cell_size,
                                     fc=("purple"), alpha=0.4))

        for i in range(1, self.maze.solution_path.__len__()):
            if self.maze.solution_path[i][0] not in list_of_backtrackers and\
                    self.maze.solution_path[i-1][0] not in list_of_backtrackers:
                circle_num += 1
                self.ax.add_patch(plt.Circle(((self.maze.solution_path[i][0][1] + 0.5)*self.cell_size,
                    (self.maze.solution_path[i][0][0] + 0.5)*self.cell_size), 0.2*self.cell_size,
                    fc = ("purple"), alpha = 0.4))

        # Display the plot to the user
        plt.show()

        # Handle any saving
        if self.media_filename:
            fig.savefig("{}{}.png".format(self.media_filename, "_solution"), frameon=None)

    def show_generation_animation(self):
        """Function that animates the process of generating the a maze where path is a list
        of coordinates indicating the path taken to carve out (break down walls) the maze."""

        # Create the figure and style the axes
        fig = self.configure_plot()

        # The square that represents the head of the algorithm
        indicator = plt.Rectangle((self.maze.generation_path[0][0]*self.cell_size, self.maze.generation_path[0][1]*self.cell_size),
            self.cell_size, self.cell_size, fc = "purple", alpha = 0.6)

        self.ax.add_patch(indicator)

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

        plt.show(block=False)

        if self.media_filename:
            print("Saving generation animation. This may take a minute....")
            mpeg_writer = animation.FFMpegWriter(fps=24, bitrate=1000,
                                                 codec="libx264", extra_args=["-pix_fmt", "yuv420p"])
            anim.save("{}{}{}x{}.mp4".format(self.media_filename, "_generation_", self.maze.num_rows,
                                           self.maze.num_cols), writer=mpeg_writer)

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
                         [i*self.cell_size, i*self.cell_size], linewidth = 2, color = color_walls)[0]
                if self.maze.initial_grid[i][j].walls["right"]:
                    self.lines["{},{}: right".format(i, j)] = self.ax.plot([(j+1)*self.cell_size, (j+1)*self.cell_size],
                         [i*self.cell_size, (i+1)*self.cell_size], linewidth = 2, color = color_walls)[0]
                if self.maze.initial_grid[i][j].walls["bottom"]:
                    self.lines["{},{}: bottom".format(i, j)] = self.ax.plot([(j+1)*self.cell_size, j*self.cell_size],
                         [(i+1)*self.cell_size, (i+1)*self.cell_size], linewidth = 2, color = color_walls)[0]
                if self.maze.initial_grid[i][j].walls["left"]:
                    self.lines["{},{}: left".format(i, j)] = self.ax.plot([j*self.cell_size, j*self.cell_size],
                             [(i+1)*self.cell_size, i*self.cell_size], linewidth = 2, color = color_walls)[0]
                self.squares["{},{}".format(i, j)] = plt.Rectangle((j*self.cell_size,
                                                                    i*self.cell_size), self.cell_size, self.cell_size,
                                                                   fc = "darkgreen", alpha = 0.4, visible = False)
                self.ax.add_patch(self.squares["{},{}".format(i, j)])

    def animate_maze_solution(self):
        """Animates the maze solution, leaving a dashed trace for the path and marking backtracking with 'X'."""
        fig = self.configure_plot()
        self.plot_walls()

        # Adding indicator to see shere current search is happening.
        indicator = plt.Rectangle((self.maze.solution_path[0][0][0]*self.cell_size,
                                   self.maze.solution_path[0][0][1]*self.cell_size), self.cell_size, self.cell_size,
                                  fc="black", alpha=0.6)
        self.ax.add_patch(indicator)

        self.add_path()

        def animate_squares(frame):
            """Function to animate the solved path of the algorithm."""
            if frame > 0:
                if self.maze.solution_path[frame - 1][1]:  # Color backtracking
                    self.squares["{},{}".format(self.maze.solution_path[frame - 1][0][0],
                                           self.maze.solution_path[frame - 1][0][1])].set_facecolor("darkred")

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
                                   interval=5, blit=True, repeat=False)
        logging.debug("Finished creating solution animation")

        # Display the animation to the user
        plt.show()

        # Save the animation if a filename is specified
        if self.media_filename:
            anim.save(f"{self.media_filename}_solution_animation.gif", writer="pillow", fps=30)

