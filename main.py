import tkinter as tk
from model import SettingsModel
from view import TrackerView
from controller import TrackerController

def main():
    root = tk.Tk()
    
    model = SettingsModel()
    palette = model.get_active_palette()
    
    view = TrackerView(root, palette, model.settings)
    controller = TrackerController(model, view)
    
    controller.update_clock_loop()
    root.mainloop()

if __name__ == "__main__":
    main()