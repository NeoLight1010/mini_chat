import tkinter as tk


class ChatWindow(tk.Frame):
    def __init__(self, gui, **kw):
        self.width = 600
        self.height = 450
        super().__init__(**kw, master=gui.root, width=self.width, height=self.height)

        self.gui = gui  # Gui handler class
        self.root = gui.root
        self.linker = gui.linker

        self.gui.root.geometry(f'{self.width}x{self.height}')

        header = tk.Frame(self, bg='green')
        content = tk.Frame(self, bg='red')
        footer = tk.Frame(self, bg='green')

        self.columnconfigure(0, weight=1)  # 100%

        self.rowconfigure(0, weight=1)  # 10%
        self.rowconfigure(1, weight=8)  # 80%
        self.rowconfigure(2, weight=1)  # 10%

        header.grid(row=0, sticky='news')
        content.grid(row=1, sticky='news')
        footer.grid(row=2, sticky='news')
