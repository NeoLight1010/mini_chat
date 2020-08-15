import tkinter as tk


class GuiHandler:
    """GuiHandler is a class for handling all the app windows."""
    def __init__(self, linker, frames):
        self.frames = frames
        self.root = tk.Tk()
        self.linker = linker
        self.frame = None
        self.switch_frame(0)

        # Handle closing.
        def on_closing():
            self.linker.send_notif('DISCONNECT')
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)

    def switch_frame(self, n):
        """Opens window at index n from windows list. It also terminates the previously open window."""
        if self.frame is not None:
            self.frame.destroy()

        self.frame = self.frames[n](self)
        self.frame.grid()

    def start(self):
        self.root.mainloop()
