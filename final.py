from matplotlib import font_manager
import pandas as pd
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mplcursors
import sys
import requests
from PIL import Image, ImageTk, UnidentifiedImageError
from io import BytesIO
from googleapiclient.discovery import build
import io
import projection


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

        self.image_label = tk.Label(self.button_frame)
        self.image_label.pack(side=tk.TOP)

        self.name_label()
        self.create_label()
        self.predicted_label()
        self.real_label()
        self.create_role_menu()
        self.create_date_menu()
        self.create_confirm_button()
        self.heatmap_button = tk.Button(
            self.button_frame, text="Heatmap accuracy", command=projection.heatmap_display)
        self.heatmap_button.pack(side=tk.TOP)
        self.models_button = tk.Button(
            self.button_frame, text="Models accuracy", command=projection.models_display)
        self.models_button.pack(side=tk.TOP)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def display_player_image(self, player_name):
        image_url = display_basketball_player_image(player_name)

        try:
            if image_url:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
                response = requests.get(image_url, headers=headers)
                response.raise_for_status()
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((200, 200))
                photo = ImageTk.PhotoImage(image)

                self.image_label.configure(image=photo)
                self.image_label.image = photo
            else:
                self.image_label.configure(image="")
        except (requests.RequestException, UnidentifiedImageError) as e:
            self.image_label.configure(image="")
            print(f"An error occurred while loading the image: {e}")

    def name_label(self):
        self.name_var = tk.StringVar()
        self.name_var.set("Players name")
        label0 = tk.Label(self.button_frame, textvariable=self.name_var)
        label0.pack(side=tk.TOP)

    def create_label(self):
        self.label_var = tk.StringVar()
        self.label_var.set("This is where the player will be")
        label = tk.Label(self.button_frame, textvariable=self.label_var)
        label.pack(side=tk.TOP)

    def predicted_label(self):
        self.label_var2 = tk.StringVar()
        self.label_var2.set("Predicted player stats")
        label2 = tk.Label(self.button_frame, textvariable=self.label_var2)
        label2.pack(side=tk.TOP)

    def real_label(self):
        self.label_var3 = tk.StringVar()
        self.label_var3.set("Difference or whatever (figure this part out)")
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

        self.fig_frame.destroy()
        self.fig_frame = tk.Frame(self.root)
        self.fig_frame.pack(side=tk.LEFT)

        fig = create_scatter_plot(
            x, y, self.data_manager.get_player_stats(), "PTS")

        canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        return canvas

    def on_plot_pick(self, event, canvas):
        index = event.ind[0]
        player = self.data_manager.get_player_stats()[index]
        self.label_var.set(f"Selected player: {player.player}")
        canvas.draw()

    def update_plot(self):
        selected_header = self.header_var.get()

        x = [float(getattr(player, selected_header.lower()))
             for player in self.data_manager.get_player_stats()]
        y = [float(player.g)
             for player in self.data_manager.get_player_stats()]

        self.fig_frame.destroy()
        self.fig_frame = tk.Frame(self.root)
        self.fig_frame.pack(side=tk.LEFT)

        fig = create_scatter_plot(
            x, y, self.data_manager.get_player_stats(), selected_header)

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


def create_scatter_plot(x, y, data, selected_header):
    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y)
    plt.xlabel(selected_header.upper())
    plt.ylabel("G")
    plt.title("NBA Player Scatter Plot")

    cursor = mplcursors.cursor(hover=True)

    prop = font_manager.FontProperties(family='Arial')

    @cursor.connect("add")
    def on_hover(sel):
        index = sel.index
        player = data[index]

        name = player.player
        age = player.age
        g = player.g
        fg = player.fg
        fga = player.fga
        three_p = player.three_p
        three_pa = player.three_pa
        three_pct = player.three_pct
        ft = player.ft
        fta = player.fta
        trb = player.trb
        ast = player.ast
        stl = player.stl
        blk = player.blk
        tov = player.tov
        pts = player.pts

        sel.annotation.set_text(f"{name}, {age}")
        sel.annotation.set_fontproperties(prop)
        gui.name_var.set(f"{name}, {age}")
        gui.label_var.set(f"PTS: {pts}, G: {g}, FG: {fg}, FGA: {fga},   3P: {three_p}, 3PA: {three_pa}, 3P%: {three_pct}\n"
                          f"FT: {ft}, FTA: {fta}, TRB: {trb}, AST: {ast}, STL: {stl}, BLK: {blk}, TOV: {tov}")
        sus_player = get_sus_player(name)
        for row in sus_player:
            zg = row["G"]
            zpts = row["PTS"]
            ztrb = row["TRB"]
            zast = row["AST"]
            zstl = row["STL"]
            zblk = row["BLK"]
            ztov = row["TOV"]
            zfga = row["FGA"]
            zfg = row["FG"]
            zfta = row["FTA"]
            zft = row["FT"]
            zthree_pa = row["3PA"]
            zthree_p = row["3P"]
            zthree_pct = row["PER"]
        gui.label_var2.set(f"PTS: {zpts}, G: {zg}, FG: {zfg}, FGA: {zfga}, 3P: {zthree_p}, 3PA: {zthree_pa}, 3P%: {zthree_pct}\n"
                           f"FT: {zft}, FTA: {zfta}, TRB: {ztrb}, AST: {zast}, STL: {zstl}, BLK: {zblk}, TOV: {ztov}")

        dg = g - zg
        dpts = pts - zpts
        dtrb = trb - ztrb
        dast = ast - zast
        dstl = stl - zstl
        dblk = blk - zblk
        dtov = tov - ztov
        dfga = fga - zfga
        dfg = fg - zfg
        dfta = fta - zfta
        dft = ft - zft
        dthree_pa = three_pa - zthree_pa
        dthree_p = three_p - zthree_p
        dthree_pct = three_pct - zthree_pct
        gui.label_var3.set(f"PTS: {dpts:.2f}, G: {dg:.2f}, FG: {dfg:.2f}, FGA: {dfga:.2f}, 3P: {dthree_p:.2f}, 3PA: {dthree_pa:.2f}, 3P%: {dthree_pct:.2f}\n"
                           f"FT: {dft:.2f}, FTA: {dfta:.2f}, TRB: {dtrb:.2f}, AST: {dast:.2f}, STL: {dstl:.2f}, BLK: {dblk:.2f}, TOV: {dtov:.2f}")

        gui.display_player_image(name)

        allinfo = get_player_info(name)
        for row in allinfo:
            # print(x)
            pts = row["PTS"]
            g = row["G"]
            #print(f"Points: {pts}, Games: {g}")

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


def get_sus_player(player_name):
    player_info = []
    data = pd.read_csv('m_2_predicted_player_stats_22_23.csv')
    matching_rows = data[data['Player'] == player_name]
    for _, row in matching_rows.iterrows():
        player_info.append(row)

    # for x in player_info:
    #     print(x)
    return player_info


cx = 'c6181f801ca8b4273'
api_key = 'AIzaSyBlX2U4hnPnK6F3vsVRl54ai9RnKc21MkE'


def search_images(query):
    service = build('customsearch', 'v1', developerKey=api_key)

    response = service.cse().list(
        cx=cx,
        q=query,
        searchType='image',
        num=1
    ).execute()

    if 'items' in response:
        image_url = response['items'][0]['link']
        return image_url

    return None


def display_basketball_player_image(player_name):
    query = player_name + ' basketball player'
    image_url = search_images(query)

    return image_url

# player_name = "LeBron James"
# print(display_basketball_player_image(player_name))


if __name__ == "__main__":
    projection.findTrue()
    projection.createSus()
    root = tk.Tk()
    data_manager = DataManager("NBA player 2022-2023.csv")
    data_manager.load_data()

    gui = GUI(root, data_manager)

    root.protocol("WM_DELETE_WINDOW", gui.on_closing)

    root.mainloop()

# apikey = AIzaSyBlX2U4hnPnK6F3vsVRl54ai9RnKc21MkE
# cx = c6181f801ca8b4273
