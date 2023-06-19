import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mplcursors
import sys
import requests
from PIL import Image, ImageTk, UnidentifiedImageError
import io
import DataManager as dm
import HelperFunctions as hf
import PlayerStats as ps
from matplotlib import font_manager


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

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def display_player_image(self, player_name):
        query = player_name + ' basketball player'
        image_url = dm.search_images(query)

        try:
            if image_url:
                response = requests.get(image_url)
                response.raise_for_status()  # Check    for any request errors
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                # Resize the image to 200x200 pixels
                image = image.resize((200, 200))
                photo = ImageTk.PhotoImage(image)

                self.image_label.configure(image=photo)
                self.image_label.image = photo
                self.name_label.configure(text=player_name)
            else:
                self.image_label.configure(image="")
                self.name_label.configure(
                    text=f"No image found for {player_name}")
        except (requests.RequestException, UnidentifiedImageError) as e:
            self.image_label.configure(image="")
            self.name_label.configure(
                text=f"Error loading image for {player_name}")
            print(f"An error occurred while loading the image: {e}")

    # def image(self):
    #     url = "https://picsum.photos/200"

    #     # try:
    #     # Download the image from the URL
    #     response = requests.get(url)
    #     response.raise_for_status()

    #     # Open the image using PIL
    #     image = Image.open(io.BytesIO(response.content))
    #     image = image.resize((200, 200), Image.ANTIALIAS)

    #     # Convert the image to PhotoImage format for Tkinter
    #     self.photo = ImageTk.PhotoImage(image)

    #     # Create a label to display the image
    #     self.image_label = tk.Label(self.button_frame, image=self.photo)
    #     self.image_label.pack(side=tk.TOP)

    #     # except Exception as e:
    #     #     print(f"Error: {e}")

    def name_label(self):
        self.name_var = tk.StringVar()
        self.name_var.set("Players name")
        self.image_label = tk.Label(self.button_frame)
        self.image_label.pack(side=tk.TOP)
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
            'Data\\NBA player 2022-2023.csv', 'Data\\NBA player 2021-2022.csv', 'Data\\NBA player 2020-2021.csv'
        ]
        self.dates = dates
        self.dates_var = tk.StringVar()
        self.dates_var.set(dates[0])

        def on_date_select(*args):
            selected_date = self.dates_var.get()
            index = dates.index(selected_date)
            selected_file = date_files[index]
            self.data_manager = dm(selected_file)
            self.data_manager.load_data()
            self.update_plot()

        option_menu = tk.OptionMenu(
            self.button_frame, self.dates_var, *dates, command=on_date_select)
        option_menu.pack(side=tk.TOP)

    def create_confirm_button(self):
        confirm_button = tk.Button(
            self.button_frame, text="Confirm", command=self.update_plot)
        confirm_button.pack(side=tk.TOP)

    # def create_create_button(self):
    #     def create_player_popup():
    #         popup = tk.Toplevel()
    #         popup.title("Create New Player")
    #         popup.geometry("300x200")

    #         label = tk.Label(
    #             popup, text="Input the values for the new player:")
    #         label.pack()

    #         # Add input fields for player attributes

    #     create_button = tk.Button(
    #         self.button_frame, text="Create", command=create_player_popup)
    #     create_button.pack(side=tk.TOP)


def create_scatter_plot(x, y, data, selected_header, guii):
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
        index = sel.index
        player = data[index]

        name = player.player
        age = player.age
        g = player.g
        # gs = player.gs
        # mp = player.mp
        fg = player.fg
        fga = player.fga
        # fg_pct = player.fg_pct
        three_p = player.three_p
        three_pa = player.three_pa
        three_pct = player.three_pct
        # two_p = player.two_p
        # two_pa = player.two_pa
        # two_pct = player.two_pct
        # efg_pct = player.efg_pct
        ft = player.ft
        fta = player.fta
        #ft_pct = player.ft_pct
        # orb = player.orb
        # drb = player.drb
        trb = player.trb
        ast = player.ast
        stl = player.stl
        blk = player.blk
        tov = player.tov
        # pf = player.pf
        pts = player.pts

        sel.annotation.set_text(f"{name}, {age}")
        sel.annotation.set_fontproperties(prop)
        guii.name_var.set(f"{name}, {age}")
        guii.label_var.set(f"PTS: {pts}, G: {g}, FG: {fg}, FGA: {fga},   3P: {three_p}, 3PA: {three_pa}, 3P%: {three_pct}\n"
                           f"FT: {ft}, FTA: {fta}, TRB: {trb}, AST: {ast}, STL: {stl}, BLK: {blk}, TOV: {tov}")
        sus_player = hf.get_sus_player(name)
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
        guii.label_var2.set(f"PTS: {zpts}, G: {zg}, FG: {zfg}, FGA: {zfga}, 3P: {zthree_p}, 3PA: {zthree_pa}, 3P%: {zthree_pct}\n"
                            f"FT: {zft}, FTA: {zfta}, TRB: {ztrb}, AST: {zast}, STL: {zstl}, BLK: {zblk}, TOV: {ztov}")
        # gs = player.gs
        # mp = player.mp
        # fg_pct = player.fg_pct
        # two_p = player.two_p
        # two_pa = player.two_pa
        # two_pct = player.two_pct
        # efg_pct = player.efg_pct
        #zft_pct = sus_player[1]
        # orb = player.orb
        # drb = player.drb
        # pf = player.pf

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
        guii.label_var3.set(f"PTS: {dpts:.2f}, G: {dg:.2f}, FG: {dfg:.2f}, FGA: {dfga:.2f}, 3P: {dthree_p:.2f}, 3PA: {dthree_pa:.2f}, 3P%: {dthree_pct:.2f}\n"
                            f"FT: {dft:.2f}, FTA: {dfta:.2f}, TRB: {dtrb:.2f}, AST: {dast:.2f}, STL: {dstl:.2f}, BLK: {dblk:.2f}, TOV: {dtov:.2f}")

        guii.display_player_image(name)

        guii.url.set(hf.display_basketball_player_image(name))

        allinfo = hf.get_player_info(name)
        for row in allinfo:
            # print(x)
            pts = row["PTS"]
            g = row["G"]
            #print(f"Points: {pts}, Games: {g}")

    def on_click(event):
        if event.button == 1:
            index = event.index
            name = data[index].player
            guii.label_var.set(f"Selected player: {name}")

    fig.canvas.mpl_connect("button_press_event", on_click)

    return fig
