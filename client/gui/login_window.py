import tkinter as tk
from tkinter import messagebox


class InternalAlerts:
    def __init__(self):
        self.start_backend = 'START_BACKEND'


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


class LoginWindow:
    def __init__(self, linker):
        self.linker = linker
        self.linker.send_notif("GUI linker connected")
        ialerts = InternalAlerts()

        self.width = 600
        self.height = 450
        n_of_rows = 3
        n_of_cols = 4
        row_height = int(self.height / n_of_rows)
        column_width = int(self.width / n_of_cols)

        self.main_bg_color = '#14213d'
        self.secondary_color = '#fca311'
        self.tertiary_color = 'black'
        self.main_text_color = 'white'

        self.root = tk.Tk()
        self.root.geometry(f'{self.width}x{self.height}')
        self.root.resizable(width=0, height=0)
        self.root.title('minichat - login')

        self.main_frame = tk.Frame(self.root, width=self.width, height=self.height)
        self.main_frame.grid(column=0, row=0, sticky='N W E S')

        # Define main font type.
        main_font_size = 15
        main_font_family = 'Helvetica'
        font_type = FontType(main_font_family, main_font_size)

        # 1st row frame
        self.title_frame = RowFrame(self.main_frame, self.width, bg=self.main_bg_color, height=row_height, anchor='s')
        self.title_frame.grid(row=1)

        self.title = tk.Label(self.title_frame, text='MiniChat', font=font_type.h1())
        self.title.grid(sticky='')

        # 2nd row frame
        self.entry_frame = RowFrame(self.main_frame, self.width, bg=self.main_bg_color, height=row_height, anchor='s')
        self.entry_frame.grid(row=2)

        tk.Label(self.entry_frame, text='Username:', font=font_type.p()).grid()
        self.user_name = tk.StringVar()
        self.user_name_entry = tk.Entry(self.entry_frame, textvariable=self.user_name, font=font_type.p())
        self.user_name_entry.grid(row=2)

        # 3rd row frame
        self.login_btn_frame = RowFrame(self.main_frame, self.width, bg=self.main_bg_color,
                                        height=row_height, anchor='n')
        self.login_btn_frame.grid(row=3)

        def check_user_name():
            name = self.user_name.get()
            if name:
                message='Your name is correct'
                messagebox.showinfo(message=message)
                self.linker.send_notif(ialerts.start_backend, name)

        self.login_btn = tk.Button(self.login_btn_frame, text='Login', command=check_user_name)
        self.login_btn.grid()

        # Styling
        # Apply padding, change bg and fg, and replace relief to FLAT.
        for row in self.main_frame.winfo_children():
            for child in row.winfo_children():
                child.grid_configure(padx=10, pady=10)
                child.configure(bg=self.main_bg_color, fg=self.main_text_color, relief=tk.FLAT)

        # Change button color.
        self.login_btn.configure(bg=self.tertiary_color)

        # Change Entry color and add padding.
        self.user_name_entry.configure(bg=self.secondary_color, fg='black', borderwidth=4)

    def start(self):
        self.root.mainloop()
