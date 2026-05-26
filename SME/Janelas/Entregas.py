import tkinter as tk

from Widgets.EntregaCard import Card
from Services.db import listar_entregas_em_curso, listar_entregas_finalizadas


class Entregas(tk.Frame):

    def __init__(self, master, tipo="em_curso"):
        super().__init__(master, bg="#f4f6f8")

        self.tipo = tipo

        if self.tipo == "em_curso":
            titulo = "Entregas em Curso"
            entregas = listar_entregas_em_curso()
        else:
            titulo = "Entregas Finalizadas"
            entregas = listar_entregas_finalizadas()

        labelTitulo = tk.Label(
            self,
            text=titulo,
            font=("Arial", 20, "bold"),
            bg="#f4f6f8",
            fg="#222222"
        )
        labelTitulo.pack(pady=20)

        area_scroll = tk.Frame(self, bg="#f4f6f8")
        area_scroll.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            area_scroll,
            bg="#f4f6f8",
            highlightthickness=0
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            area_scroll,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.listaFrame = tk.Frame(self.canvas, bg="#f4f6f8")

        self.janela_lista = self.canvas.create_window(
            (0, 0),
            window=self.listaFrame,
            anchor="nw"
        )

        self.listaFrame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(
                self.janela_lista,
                width=event.width
            )
        )

        self.canvas.bind("<Enter>", self.ativar_scroll_mouse)
        self.canvas.bind("<Leave>", self.desativar_scroll_mouse)

        if len(entregas) == 0:
            labelEntregas = tk.Label(
                self.listaFrame,
                text="Nenhuma entrega encontrada.",
                font=("Arial", 12),
                bg="#f4f6f8",
                fg="#333333"
            )
            labelEntregas.pack(pady=20)
        else:
            for entrega in entregas:
                card = Card(self.listaFrame, entregaData=entrega, tipo=self.tipo)
                card.pack(fill="x", padx=20, pady=10)

    def ativar_scroll_mouse(self, event):
        self.canvas.bind_all("<MouseWheel>", self.rolar_mouse)

    def desativar_scroll_mouse(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def rolar_mouse(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")