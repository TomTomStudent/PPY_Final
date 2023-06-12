import pandas as pd
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PlayerStats:
    def __init__(self, rk, player, pos, age, team, g, gs, mp, fg, fga, fg_pct, three_p, three_pa, three_pct, two_p, two_pa, two_pct, efg_pct, ft, fta, ft_pct, orb, drb, trb, ast, stl, blk, tov, pf, pts):
        self.rk = rk
        self.player = player
        self.pos = pos
        self.age = age
        self.team = team
        self.g = g
        self.gs = gs
        self.mp = mp
        self.fg = fg
        self.fga = fga
        self.fg_pct = fg_pct
        self.three_p = three_p
        self.three_pa = three_pa
        self.three_pct = three_pct
        self.two_p = two_p
        self.two_pa = two_pa
        self.two_pct = two_pct
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

    def update_stats(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class DataManager:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.player_stats = []

    def load_data(self):
        data = pd.read_csv(self.csv_file)
        for _, row in data.iterrows():
            player = PlayerStats(
                rk=row['Rk'],
                player=row['Player'],
                pos=row['Pos'],
                age=row['Age'],
                team=row['Tm'],
                g=row['G'],
                gs=row['GS'],
                mp=row['MP'],
                fg=row['FG'],
                fga=row['FGA'],
                fg_pct=row['FG%'],
                three_p=row['3P'],
                three_pa=row['3PA'],
                three_pct=row['3P%'],
                two_p=row['2P'],
                two_pa=row['2PA'],
                two_pct=row['2P%'],
                efg_pct=row['eFG%'],
                ft=row['FT'],
                fta=row['FTA'],
                ft_pct=row['FT%'],
                orb=row['ORB'],
                drb=row['DRB'],
                trb=row['TRB'],
                ast=row['AST'],
                stl=row['STL'],
                blk=row['BLK'],
                tov=row['TOV'],
                pf=row['PF'],
                pts=row['PTS']
            )
            self.player_stats.append(player)

    def get_player_stats(self):
        return self.player_stats

    def update_player_stats(self, player, **kwargs):
        player.update_stats(**kwargs)


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
        x = [float(player.pts)
             for player in self.data_manager.get_player_stats()]
        y = [float(player.g)
             for player in self.data_manager.get_player_stats()]

        # Destroy the old plot if it exists
        self.fig_frame.destroy()
        self.fig_frame = tk.Frame(self.root)
        self.fig_frame.pack(side=tk.LEFT)

        fig = create_scatter_plot(x, y, self.data_manager.get_player_stats())

        # Create a canvas to display the plot
        canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def update_plot(self):
        selected_index = int(self.header_var.get())
        selected_header = self.header_names[selected_index]

        x = [float(getattr(player, selected_header.lower()))
             for player in self.data_manager.get_player_stats()]
        y = [float(player.g)
             for player in self.data_manager.get_player_stats()]

        # Destroy the old plot if it exists
        self.fig_frame.destroy()
        self.fig_frame = tk.Frame(self.root)
        self.fig_frame.pack(side=tk.LEFT)

        fig = create_scatter_plot(x, y, self.data_manager.get_player_stats())

        # Create a canvas to display the plot
        canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def create_option_menu(self):
        header_names = [header.lower() for header in PlayerStats.__dict__.keys(
        ) if not header.startswith("__")]
        self.header_names = header_names

        option_menu = tk.OptionMenu(
            self.button_frame, self.header_var, *range(len(header_names)))
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


def create_scatter_plot(x, y, data):
    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y)
    plt.xlabel("PTS")
    plt.ylabel("G")
    plt.title("NBA Player Scatter Plot")

    # Create a cursor that displays the name on hover
    cursor = mplcursors.cursor(hover=True)

    @cursor.connect("add")
    def on_hover(sel):
        index = sel.target.index
        name = data[index].player  # Get the player name
        sel.annotation.set_text(name)

    return fig


class NeuralNetwork:
    def __init__(self):
        # Implement the initialization logic for the neural network
        pass

    def feedforward(self):
        # Implement the feedforward calculation logic
        pass

    def train(self):
        # Implement the training logic for the neural network
        pass

    def evaluate(self):
        # Implement the logic to evaluate the accuracy of the network using the test dataset
        pass

    # Implement additional methods for neural network operations


if __name__ == "__main__":
    root = tk.Tk()
    data_manager = DataManager("NBA player 2022-2023.csv")
    data_manager.load_data()

    gui = GUI(root, data_manager)

    root.mainloop()
