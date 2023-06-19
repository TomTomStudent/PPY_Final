import tkinter as tk
from DataManager import DataManager
from GUI import GUI

if __name__ == "__main__":
    root = tk.Tk()
    data_manager = DataManager("Data/NBA player 2022-2023.csv")
    data_manager.load_data()

    gui = GUI(root, data_manager)

    root.protocol("WM_DELETE_WINDOW", gui.on_closing)

    root.mainloop()

# apikey = AIzaSyBlX2U4hnPnK6F3vsVRl54ai9RnKc21MkE
# cx = c6181f801ca8b4273
