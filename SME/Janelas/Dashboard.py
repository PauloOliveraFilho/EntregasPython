import tkinter as tk


class Dashboard(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(
            self,
            text="Tela Dashboard",
            font=("Arial", 20)
        )

        label.pack(pady=50)