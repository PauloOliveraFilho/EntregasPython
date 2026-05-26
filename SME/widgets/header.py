import tkinter as tk


class Header(tk.Frame):

    def __init__(self, master):
        super().__init__(
            master,
            bg="#263238",
            height=60
        )

        self.pack(fill="x")
        self.pack_propagate(False)

        self.area_titulo = tk.Frame(self, bg="#263238")
        self.area_titulo.pack(side="left", padx=20)

        self.label_titulo = tk.Label(
            self.area_titulo,
            text="SME",
            font=("Arial", 18, "bold"),
            bg="#263238",
            fg="white"
        )
        self.label_titulo.pack(side="left")

        self.label_subtitulo = tk.Label(
            self.area_titulo,
            text="Sistema de Monitoramento de Entregas",
            font=("Arial", 10),
            bg="#263238",
            fg="#cfd8dc"
        )
        self.label_subtitulo.pack(side="left", padx=(10, 0))

        self.area_botoes = tk.Frame(self, bg="#263238")
        self.area_botoes.pack(side="right", padx=20)

    def addBotao(self, texto, comando):
        btn = tk.Button(
            self.area_botoes,
            text=texto,
            command=comando,
            font=("Arial", 10, "bold"),
            bg="#37474f",
            fg="white",
            activebackground="#455a64",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2"
        )

        btn.pack(side="left", padx=5)