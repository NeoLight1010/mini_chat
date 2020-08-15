import tkinter as tk


class ChatWindow(tk.Frame):
    def __init__(self, gui, **kw):
        super().__init__(master=gui.root, **kw)
        self.gui = gui  # Gui handler class
        self.linker = gui.linker

        tk.Label(self, text='This is the chat window!').pack()
