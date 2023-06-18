from matplotlib import font_manager
import pandas as pd
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mplcursors
import sys


class PlayerStats(object):
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

        self.name_label()
        self.create_label()
        self.predicted_label()
        self.real_label()
        self.create_role_menu()
        self.create_date_menu()
        self.create_confirm_button()
        self.create_create_button()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def name_label(self):
        self.name_var = tk.StringVar()
        self.name_var.set("Players name")
        label0 = tk.Label(self.button_frame, textvariable=self.name_var)
        label0.pack(side=tk.TOP)

    def create_label(self):
        self.label_var = tk.StringVar()  # Variable to store the label text
        self.label_var.set("This is where the player will be")
        label = tk.Label(self.button_frame, textvariable=self.label_var)
        label.pack(side=tk.TOP)

    def predicted_label(self):
        self.label_var2 = tk.StringVar()  # Variable to store the label text
        self.label_var2.set("Predicted player stats")
        label2 = tk.Label(self.button_frame, textvariable=self.label_var2)
        label2.pack(side=tk.TOP)

    def real_label(self):
        self.label_var3 = tk.StringVar()  # Variable to store the label text
        self.label_var3.set("Real player stats (if exists)")
        label3 = tk.Label(self.button_frame, textvariable=self.label_var3)
        label3.pack(side=tk.TOP)

    def on_closing(self):
        self.root.destroy()
        sys.exit()

    def create_scatter_plot(self):
        x = [float(player.pts)
             for player in self.data_manager.get_player_stats()]
        y = [float(player.g)
             for player in self.data_manager.get_player_stats()]

        # Destroy the old plot if it exists
        self.fig_frame.destroy()
        self.fig_frame = tk.Frame(self.root)
        self.fig_frame.pack(side=tk.LEFT)

        fig = create_scatter_plot(
            x, y, self.data_manager.get_player_stats(), "PTS")

        # Create a canvas to display the plot
        canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        canvas.draw()
        canvas.mpl_connect("pick_event", lambda event: self.on_plot_pick(
            event, canvas))  # Connect pick_event to callback
        canvas.get_tk_widget().pack()

        return canvas  # Return the canvas object

    def on_plot_pick(self, event, canvas):
        # Get the index of the selected player
        index = event.ind[0]
        player = self.data_manager.get_player_stats()[index]
        # Update the label with the player name
        self.label_var.set(f"Selected player: {player.player}")
        # Update the canvas to reflect the label change
        canvas.draw()

    def update_plot(self):
        selected_header = self.header_var.get()

        x = [float(getattr(player, selected_header.lower()))
             for player in self.data_manager.get_player_stats()]
        y = [float(player.g)
             for player in self.data_manager.get_player_stats()]

        # Destroy the old plot if it exists
        self.fig_frame.destroy()
        self.fig_frame = tk.Frame(self.root)
        self.fig_frame.pack(side=tk.LEFT)

        fig = create_scatter_plot(
            x, y, self.data_manager.get_player_stats(), selected_header)

        # Create a canvas to display the plot
        canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def create_role_menu(self):
        header_names = [
            'rk', 'age', 'g', 'gs', 'mp', 'fg', 'fga',
            'fg_pct', 'three_p', 'three_pa', 'three_pct', 'two_p', 'two_pa', 'two_pct', 'efg_pct',
            'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk',
            'tov', 'pf', 'pts'
        ]
        self.header_names = header_names
        self.header_var.set(header_names[0])
        option_menu = tk.OptionMenu(
            self.button_frame, self.header_var, *header_names)
        option_menu.pack(side=tk.TOP)

    def create_date_menu(self):
        dates = [
            '22/23', '21/22', '20/21'
        ]
        date_files = [
            'NBA player 2022-2023.csv', 'NBA player 2021-2022.csv', 'NBA player 2020-2021.csv'
        ]
        self.dates = dates
        self.dates_var = tk.StringVar()
        self.dates_var.set(dates[0])

        def on_date_select(*args):
            selected_date = self.dates_var.get()
            index = dates.index(selected_date)
            selected_file = date_files[index]
            self.data_manager = DataManager(selected_file)
            self.data_manager.load_data()
            self.update_plot()

        option_menu = tk.OptionMenu(
            self.button_frame, self.dates_var, *dates, command=on_date_select)
        option_menu.pack(side=tk.TOP)

    def create_confirm_button(self):
        confirm_button = tk.Button(
            self.button_frame, text="Confirm", command=self.update_plot)
        confirm_button.pack(side=tk.TOP)

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
        create_button.pack(side=tk.TOP)


def create_scatter_plot(x, y, data, selected_header):
    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y)
    plt.xlabel(selected_header.upper())  # Update the x-axis label here
    plt.ylabel("G")
    plt.title("NBA Player Scatter Plot")

    # Create a cursor that displays the name on hover
    cursor = mplcursors.cursor(hover=True)

    # Set the font to Arial
    prop = font_manager.FontProperties(family='Arial')

    @cursor.connect("add")
    def on_hover(sel):
        index = sel.target.index
        player = data[index]

        name = player.player
        age = player.age
        g = player.g
        gs = player.gs
        mp = player.mp
        fg = player.fg
        fga = player.fga
        fg_pct = player.fg_pct
        three_p = player.three_p
        three_pa = player.three_pa
        three_pct = player.three_pct
        two_p = player.two_p
        two_pa = player.two_pa
        two_pct = player.two_pct
        efg_pct = player.efg_pct
        ft = player.ft
        fta = player.fta
        ft_pct = player.ft_pct
        orb = player.orb
        drb = player.drb
        trb = player.trb
        ast = player.ast
        stl = player.stl
        blk = player.blk
        tov = player.tov
        pf = player.pf
        pts = player.pts

        sel.annotation.set_text(f"{name}, {age}")
        sel.annotation.set_fontproperties(prop)
        gui.name_var.set(f"{name}, {age}")
        gui.label_var.set(f"PTS: {pts}, G: {g}, GS: {gs}, MP: {mp}, FG: {fg}, FGA: {fga}, FG %: {fg_pct}, 3P: {three_p}\n"
                          f"3PA: {three_pa}, 3P%: {three_pct}, 2P: {two_p}, 2PA: {two_pa}, 2P%: {two_pct}, eFG%: {efg_pct}\n"
                          f"FT: {ft}, FTA: {fta}, FT%: {ft_pct}, ORB: {orb}, DRB: {drb}, TRB: {trb}, AST: {ast}\n"
                          f"STL: {stl}, BLK: {blk}, TOV: {tov}, PF: {pf}")

        allinfo = get_player_info(name)
        for row in allinfo:
            # print(x)
            pts = row["PTS"]
            g = row["G"]
            print(f"Points: {pts}, Games: {g}")

    def on_click(event):
        if event.button == 1:
            index = event.target.index
            name = data[index].player
            gui.label_var.set(f"Selected player: {name}")

    fig.canvas.mpl_connect("button_press_event", on_click)

    return fig


def get_player_info(player_name):
    csv_files = ['NBA player 2022-2023.csv',
                 'NBA player 2021-2022.csv', 'NBA player 2020-2021.csv']
    player_info = []

    for csv_file in csv_files:
        data = pd.read_csv(csv_file)
        matching_rows = data[data['Player'] == player_name]
        for _, row in matching_rows.iterrows():
            player_info.append(row)

    return player_info


if __name__ == "__main__":
    root = tk.Tk()
    data_manager = DataManager("NBA player 2022-2023.csv")
    data_manager.load_data()

    gui = GUI(root, data_manager)

    root.protocol("WM_DELETE_WINDOW", gui.on_closing)

    root.mainloop()
