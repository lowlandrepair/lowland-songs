import tkinter as tk
from styles.theme import *

class Sidebar:
    def __init__(self, master, nav_commands):
        self.frame = tk.Frame(master, bg=SIDEBAR_COLOR, width=250)
        self.frame.grid(row=0, column=0, sticky="ns")
        self.frame.grid_propagate(False)
        self.create_widgets(nav_commands)

    def create_widgets(self, nav_commands):
        # Logo
        logo = tk.Label(self.frame, text="Lowland", fg=ACCENT_COLOR, bg=SIDEBAR_COLOR,
                        font=HEADER_FONT)
        logo.pack(pady=30)

        # Navigation buttons
        for label, command in nav_commands.items():
            btn = tk.Button(self.frame, text=label, fg="white", bg=SIDEBAR_COLOR,
                            font=FONT, relief="flat", activebackground=BUTTON_COLOR,
                            activeforeground=ACCENT_COLOR, command=command,
                            bd=0, padx=20, pady=10, anchor="w")
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=ACCENT_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=SIDEBAR_COLOR))
