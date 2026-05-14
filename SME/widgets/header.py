import tkinter as tk


class Header(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg="#34495e", height=50)

        self.pack(fill="x")

    def addBotao(self, texto, comando):

        btn = tk.Button(
            self,
            text=texto,
            command=comando
        )

        btn.pack(side="left", padx=10, pady=10)