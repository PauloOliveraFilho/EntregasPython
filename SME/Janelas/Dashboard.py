import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Services.db import buscar_estatisticas


class Dashboard(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg="#f4f6f8")

        self.dados = buscar_estatisticas()

        self.criar_titulo()
        self.criar_cards_resumo()
        self.criar_area_graficos()

    def criar_titulo(self):
        label = tk.Label(
            self,
            text="Dashboard",
            font=("Arial", 22, "bold"),
            bg="#f4f6f8",
            fg="#222222"
        )
        label.pack(pady=20)

    def criar_cards_resumo(self):
        area_cards = tk.Frame(self, bg="#f4f6f8")
        area_cards.pack(fill="x", padx=20, pady=10)

        total = self.dados.get("total", 0)
        em_curso = self.dados.get("em_curso", 0)
        entregues = self.dados.get("entregues", 0)
        problemas = self.dados.get("problemas", 0)

        self.criar_card_resumo(area_cards, "Total de Pedidos", total, "#34495e")
        self.criar_card_resumo(area_cards, "Em Curso", em_curso, "#1565c0")
        self.criar_card_resumo(area_cards, "Entregues", entregues, "#2e7d32")
        self.criar_card_resumo(area_cards, "Com Problema", problemas, "#c62828")

    def criar_card_resumo(self, master, titulo, valor, cor):
        card = tk.Frame(
            master,
            bg=cor,
            padx=15,
            pady=12
        )
        card.pack(side="left", fill="x", expand=True, padx=5)

        label_titulo = tk.Label(
            card,
            text=titulo,
            font=("Arial", 10, "bold"),
            bg=cor,
            fg="white"
        )
        label_titulo.pack()

        label_valor = tk.Label(
            card,
            text=str(valor),
            font=("Arial", 20, "bold"),
            bg=cor,
            fg="white"
        )
        label_valor.pack(pady=(5, 0))

    def criar_area_graficos(self):
        area_graficos = tk.Frame(self, bg="#f4f6f8")
        area_graficos.pack(fill="both", expand=True, padx=20, pady=20)

        self.criar_grafico_barras(area_graficos)
        self.criar_grafico_pizza(area_graficos)

    def criar_grafico_barras(self, master):
        frame_grafico = tk.Frame(master, bg="white", padx=10, pady=10)
        frame_grafico.pack(side="left", fill="both", expand=True, padx=5)

        status = ["Em Curso", "Entregues", "Problemas"]

        valores = [
            self.dados.get("em_curso", 0),
            self.dados.get("entregues", 0),
            self.dados.get("problemas", 0)
        ]

        figura = Figure(figsize=(4, 3), dpi=100)
        grafico = figura.add_subplot(111)

        grafico.bar(status, valores)

        grafico.set_title("Entregas por Status")
        grafico.set_ylabel("Quantidade")
        grafico.set_ylim(0, max(valores) + 1 if max(valores) > 0 else 1)

        figura.tight_layout()

        canvas = FigureCanvasTkAgg(figura, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def criar_grafico_pizza(self, master):
        frame_grafico = tk.Frame(master, bg="white", padx=10, pady=10)
        frame_grafico.pack(side="left", fill="both", expand=True, padx=5)

        labels = ["Em Curso", "Entregues", "Problemas"]

        valores = [
            self.dados.get("em_curso", 0),
            self.dados.get("entregues", 0),
            self.dados.get("problemas", 0)
        ]

        figura = Figure(figsize=(4, 3), dpi=100)
        grafico = figura.add_subplot(111)

        if sum(valores) == 0:
            grafico.text(
                0.5,
                0.5,
                "Sem dados para exibir",
                ha="center",
                va="center",
                fontsize=12
            )
            grafico.set_axis_off()
        else:
            grafico.pie(
                valores,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90
            )
            grafico.set_title("Percentual de Entregas")

        figura.tight_layout()

        canvas = FigureCanvasTkAgg(figura, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)