import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

categories = []  # Global variable to store the header


class PlayerStats:
    def __init__(self, rk, player, pos, age, tm, g, gs, mp, fg, fga, fg_pct, three_p, three_pa, three_p_pct,
                 two_p, two_pa, two_p_pct, efg_pct, ft, fta, ft_pct, orb, drb, trb, ast, stl, blk, tov, pf, pts):
        self.rk = rk
        self.player = player
        self.pos = pos
        self.age = age
        self.tm = tm
        self.g = g
        self.gs = gs
        self.mp = mp
        self.fg = fg
        self.fga = fga
        self.fg_pct = fg_pct
        self.three_p = three_p
        self.three_pa = three_pa
        self.three_p_pct = three_p_pct
        self.two_p = two_p
        self.two_pa = two_pa
        self.two_p_pct = two_p_pct
        self.efg_pct = efg_pct
        self.ft = ft
        self.fta = fta
        self.ft_pct = ft_pct
        self.orb = orb
        self.drb = drb
        self.trb = trb
        self.ast = ast
        self.stl = stl
        self.blk = blk
        self.tov = tov
        self.pf = pf
        self.pts = pts


class GUI:
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager
        self.header_var = tk.StringVar()
        self.header_names = []

        self.fig_frame = tk.Frame(self.root)
        self.fig_frame.pack(side=tk.LEFT)

        self.create_scatter_plot()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.RIGHT)

        self.create_option_menu()
        self.create_confirm_button()
        self.create_create_button()

    def create_scatter_plot(self):
        x = [float(getattr(player, "pts"))
             for player in self.data_manager.get_player_stats()]
        y = [float(getattr(player, "g"))
             for player in self.data_manager.get_player_stats()]

        # Destroy the old plot if it exists
        self.fig_frame.destroy()
        self.fig_frame = tk.Frame(self.root)
        self.fig_frame.pack(side=tk.LEFT)

        fig = self.create_plot(x, y, self.data_manager.get_player_stats())

        # Create a canvas to display the plot
        canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def update_plot(self):
        selected_header = self.header_var.get()  # Get the selected header name

        # Find the index of the selected header in the header names list
        selected_index = self.header_names.index(selected_header)

        x = [float(getattr(player, self.header_names[selected_index].lower()))
             for player in self.data_manager.get_player_stats()]
        y = [float(getattr(player, "g"))
             for player in self.data_manager.get_player_stats()]

        # Destroy the old plot if it exists
        self.fig_frame.destroy()
        self.fig_frame = tk.Frame(self.root)
        self.fig_frame.pack(side=tk.LEFT)

        fig = self.create_plot(
            x, y, self.data_manager.get_player_stats(), selected_header)

        # Create a canvas to display the plot
        canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def create_option_menu(self):
        header_names = [
            "Rk", "Player", "Pos", "Age", "Tm", "G", "GS", "MP", "FG", "FGA", "FG_Pct",
            "3P", "3PA", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB",
            "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"
        ]
        self.header_names = header_names

        self.header_var.set("PTS")  # Set initial value

        option_menu = ttk.OptionMenu(
            self.button_frame, self.header_var, *header_names)
        option_menu.pack(side=tk.LEFT)

    def create_confirm_button(self):
        confirm_button = tk.Button(
            self.button_frame, text="Confirm", command=self.update_plot)
        confirm_button.pack(side=tk.LEFT)

    def create_create_button(self):
        def create_player_popup():
            popup = tk.Toplevel()
            popup.title("Create New Player")
            popup.geometry("300x200")

            label = tk.Label(
                popup, text="Input the values for the new player:")
            label.pack()

            # Add input fields for player attributes

        create_button = tk.Button(
            self.button_frame, text="Create", command=create_player_popup)
        create_button.pack(side=tk.LEFT)

    def create_plot(self, x, y, data, selected_header="PTS"):
        fig, ax = plt.subplots()
        scatter = ax.scatter(x, y)
        plt.xlabel(selected_header)  # Set the x-axis label
        plt.ylabel("G")  # Set the y-axis label
        plt.title("NBA Player Scatter Plot")

        # Create a cursor that displays the name on hover
        cursor = mplcursors.cursor(hover=True)

        @cursor.connect("add")
        def on_hover(sel):
            index = sel.target.index
            name = data[index].player  # Get the player name from the data
            sel.annotation.set_text(name)

        return fig


class DataManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.player_stats = []

        self.load_data()

    def load_data(self):
        # Read the data from the CSV file and create PlayerStats instances
        with open(self.file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

            global categories
            categories = lines[0].strip().split(",")  # Save the header

            for line in lines[1:]:
                attributes = line.strip().split(",")
                player_stats = PlayerStats(*attributes)
                self.player_stats.append(player_stats)

    def get_player_stats(self):
        return self.player_stats


if __name__ == "__main__":
    file_path = "NBA player 2022-2023.csv"
    data_manager = DataManager(file_path)

    root = tk.Tk()
    root.title("NBA Player Stats")
    root.geometry("800x600")

    gui = GUI(root, data_manager)

    exit_button = tk.Button(root, text="Exit", command=sys.exit)
    exit_button.pack()

    root.mainloop()
