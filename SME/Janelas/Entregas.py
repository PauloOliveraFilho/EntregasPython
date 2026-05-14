import tkinter as tk

class Entregas(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(
            self,
            text="Tela Inicial",
            font=("Arial", 20)
        )

        label.pack(pady=50)

        