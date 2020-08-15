import tkinter as tk
# from tkinter import messagebox


class InternalAlerts:
    def __init__(self):
        self.start_backend = 'START_BACKEND'
        self.disconnect = 'DISCONNECT'


class RowFrame(tk.Frame):
    def __init__(self, master, master_width, bg='', height=1, anchor='center'):
        super().__init__(master, width=master_width, height=height)
        self.master = master
        self.height = height
        self.width = master_width
        self.bg = bg

        if self.bg:
            self.configure(bg=bg)
            
        self.grid_propagate(0)
        self.grid_anchor(anchor)


class FontType:
    def __init__(self, family='clean', main_size=16):
        self.family = family
        self.main_size = main_size

        self.h1_size = self.main_size * 4
        self.p_size = main_size

    def h1(self):
        font_obj = (self.family, self.h1_size)
        return font_obj

    def p(self):
        font_obj = (self.family, self.p_size)
        return font_obj


class LoginWindow(tk.Frame):
    def __init__(self, gui, **kw):
        self.width = 600
        self.height = 450
        super().__init__(**kw, master=gui.root, width=self.width, height=self.height)

        self.gui = gui  # Gui handler class.
        self.linker = gui.linker
        self.linker.send_notif("GUI linker connected")
        self.ialerts = InternalAlerts()

        self.n_of_rows = 3
        self.n_of_cols = 4
        self.row_height = int(self.height / self.n_of_rows)
        self.column_width = int(self.width / self.n_of_cols)

        self.main_bg_color = '#14213d'
        self.secondary_color = '#fca311'
        self.tertiary_color = 'black'
        self.main_text_color = 'white'

        # TODO: Review geometry, resizable and title functions.
        # self.root.geometry(f'{self.width}x{self.height}')
        # self.root.resizable(width=0, height=0)
        # self.root.title('minichat - login')

        # Define main font type.
        main_font_size = 15
        main_font_family = 'Helvetica'
        font_type = FontType(main_font_family, main_font_size)

        # Set layout.
        # 1st row frame
        title_frame = RowFrame(self, self.width, bg=self.main_bg_color, height=self.row_height, anchor='s')
        title_frame.grid(row=1)

        title = tk.Label(title_frame, text='MiniChat', font=font_type.h1())
        title.grid(sticky='')

        # 2nd row frame
        entry_frame = RowFrame(self, self.width, bg=self.main_bg_color, height=self.row_height, anchor='s')
        entry_frame.grid(row=2)

        tk.Label(entry_frame, text='Username:', font=font_type.p()).grid()
        user_name = tk.StringVar()
        user_name_entry = tk.Entry(entry_frame, textvariable=user_name, font=font_type.p())
        user_name_entry.grid(row=2)

        # 3rd row frame
        login_btn_frame = RowFrame(self, self.width, bg=self.main_bg_color, height=self.row_height, anchor='n')
        login_btn_frame.grid(row=3)

        def check_user_name():
            name = user_name.get()
            if name:
                self.linker.send_notif(self.ialerts.start_backend, name)

        login_btn = tk.Button(login_btn_frame, text='Login', command=check_user_name)
        login_btn.grid()

        # Styling
        # Apply padding, change bg and fg, and replace relief to FLAT.
        for row in self.winfo_children():
            for child in row.winfo_children():
                child.grid_configure(padx=10, pady=10)
                child.configure(bg=self.main_bg_color, fg=self.main_text_color, relief=tk.FLAT)

        # Change button color.
        login_btn.configure(bg=self.tertiary_color)

        # Change Entry color and add padding.
        user_name_entry.configure(bg=self.secondary_color, fg='black', borderwidth=4)

        # self.root.mainloop()

