import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
import tkinter as tk


def load_data(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            data.append(row[1:])  # Omit the first two columns
    return data


def create_scatter_plot(x, y, data):
    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("NBA Player Scatter Plot")

    # Create a cursor that displays the name on hover
    cursor = mplcursors.cursor(hover=True)

    @cursor.connect("add")
    def on_hover(sel):
        index = sel.target.index
        name = data[index][0]  # Get the name from the first element of the row
        sel.annotation.set_text(name)

    return fig


def update_plot(header_var):
    global fig_frame

    selected_index = int(header_var.get())
    selected_header = header_names[selected_index]
    # Update the plot based on the selected header
    # Get the data for the selected header
    # Exclude the first column (name)
    selected_data = [float(row[selected_index + 1]) for row in data]
    # Update the x values with the selected data
    x = selected_data

    # Clear the previous plot
    plt.clf()

    # Create a new scatter plot with updated x values
    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y)
    plt.xlabel(selected_header)
    plt.ylabel("Y")
    plt.title("NBA Player Scatter Plot")

    # Create a cursor that displays the name on hover
    cursor = mplcursors.cursor(hover=True)

    @cursor.connect("add")
    def on_hover(sel):
        index = sel.target.index
        # Get the name from the first element of the row
        name = data[index][0]
        sel.annotation.set_text(name)

    # Update the canvas with the new plot
    canvas = FigureCanvasTkAgg(fig, master=fig_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def main():
    global header_names, data, x, y, fig_frame

    filename = "NBA player 2022-2023.csv"
    data = load_data(filename)
    x = [float(row[28]) for row in data]
    y = [float(row[5]) for row in data]
    fig = create_scatter_plot(x, y, data)

    root = tk.Tk()
    root.title("NBA Player Analysis")

    # Create a frame for the scatter plot
    fig_frame = tk.Frame(root)
    fig_frame.pack(side="left")

    # Embed the scatter plot in the frame
    canvas = FigureCanvasTkAgg(fig, master=fig_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Get the header names
    header_names = data[0][2:]  # Exclude the first two columns

    # Create a dropdown menu to select the header index
    header_var = tk.StringVar(root)
    header_var.set("0")  # Set the default selection to the first header
    header_menu = tk.OptionMenu(root, header_var, *range(len(header_names)))
    header_menu.pack()

    def update_plot(header_var):
        selected_index = int(header_var.get())
        selected_header = header_names[selected_index]
        selected_data = [float(row[selected_index + 2]) for row in data]
        x = selected_data

        plt.clf()

        fig, ax = plt.subplots()
        scatter = ax.scatter(x, y)
        plt.xlabel(selected_header)
        plt.ylabel("Y")
        plt.title("NBA Player Scatter Plot")

        cursor = mplcursors.cursor(hover=True)

        @cursor.connect("add")
        def on_hover(sel):
            index = sel.target.index
            name = data[index][0]
            sel.annotation.set_text(name)

        canvas = FigureCanvasTkAgg(fig, master=fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    update_button = tk.Button(root, text="Update Plot",
                              command=lambda: update_plot(header_var))
    update_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
