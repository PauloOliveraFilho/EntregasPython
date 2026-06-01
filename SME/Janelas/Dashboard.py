import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Services.db import (
    buscar_estatisticas,
    consulta_total_por_status,
    consulta_faturamento_por_entregador,
    consulta_problemas_por_bairro,
    consulta_produtos_mais_vendidos
)


class Dashboard(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg="#f4f6f8")

        self.dados = buscar_estatisticas()

        self.criar_layout_com_scroll()

        self.criar_titulo()
        self.criar_cards_resumo()
        self.criar_graficos()

    def criar_layout_com_scroll(self):
        self.canvas = tk.Canvas(
            self,
            bg="#f4f6f8",
            highlightthickness=0
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.conteudo = tk.Frame(self.canvas, bg="#f4f6f8")

        self.janela_conteudo = self.canvas.create_window(
            (0, 0),
            window=self.conteudo,
            anchor="nw"
        )

        self.conteudo.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(
                self.janela_conteudo,
                width=event.width
            )
        )

        self.canvas.bind("<Enter>", self.ativar_scroll_mouse)
        self.canvas.bind("<Leave>", self.desativar_scroll_mouse)

    def ativar_scroll_mouse(self, event):
        self.canvas.bind_all("<MouseWheel>", self.rolar_mouse)

    def desativar_scroll_mouse(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def rolar_mouse(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def criar_titulo(self):
        label = tk.Label(
            self.conteudo,
            text="Dashboard",
            font=("Arial", 22, "bold"),
            bg="#f4f6f8",
            fg="#222222"
        )
        label.pack(pady=20)

    def criar_cards_resumo(self):
        area_cards = tk.Frame(self.conteudo, bg="#f4f6f8")
        area_cards.pack(fill="x", padx=20, pady=10)

        total = self.dados.get("total", 0)
        em_curso = self.dados.get("em_curso", 0)
        entregues = self.dados.get("entregues", 0)
        problemas = self.dados.get("problemas", 0)

        self.criar_card_resumo(area_cards, "Total de Pedidos", total, "#34495e", 0)
        self.criar_card_resumo(area_cards, "Em Curso", em_curso, "#1565c0", 1)
        self.criar_card_resumo(area_cards, "Entregues", entregues, "#2e7d32", 2)
        self.criar_card_resumo(area_cards, "Com Problema", problemas, "#c62828", 3)

        for coluna in range(4):
            area_cards.grid_columnconfigure(coluna, weight=1)

    def criar_card_resumo(self, master, titulo, valor, cor, coluna):
        card = tk.Frame(
            master,
            bg=cor,
            padx=15,
            pady=12
        )
        card.grid(row=0, column=coluna, sticky="ew", padx=5)

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

    def criar_graficos(self):
        area_graficos = tk.Frame(self.conteudo, bg="#f4f6f8")
        area_graficos.pack(fill="both", expand=True, padx=20, pady=20)

        self.criar_grafico_status(area_graficos, 0, 0)
        self.criar_grafico_faturamento_entregador(area_graficos, 0, 1)
        self.criar_grafico_produtos(area_graficos, 1, 0)
        self.criar_grafico_problemas_bairro(area_graficos, 1, 1)

        area_graficos.grid_columnconfigure(0, weight=1)
        area_graficos.grid_columnconfigure(1, weight=1)

    def criar_frame_grafico(self, master, row, column):
        frame = tk.Frame(
            master,
            bg="white",
            padx=10,
            pady=10,
            relief=tk.SOLID,
            bd=1
        )

        frame.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=8,
            pady=8
        )

        return frame

    def exibir_figura(self, figura, frame):
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def criar_grafico_status(self, master, row, column):
        frame = self.criar_frame_grafico(master, row, column)

        dados = consulta_total_por_status()

        nomes = []
        valores = []

        for item in dados:
            status = item.get("_id", "sem status")
            quantidade = item.get("quantidade", 0)

            nomes.append(self.formatar_status(status))
            valores.append(quantidade)

        figura = Figure(figsize=(5, 3.5), dpi=100)
        grafico = figura.add_subplot(111)

        if len(valores) == 0:
            self.mostrar_sem_dados(grafico)
        else:
            grafico.bar(nomes, valores)
            grafico.set_title("Entregas por Status")
            grafico.set_ylabel("Quantidade")
            grafico.set_ylim(0, max(valores) + 1)

        figura.tight_layout()
        self.exibir_figura(figura, frame)

    def criar_grafico_faturamento_entregador(self, master, row, column):
        frame = self.criar_frame_grafico(master, row, column)

        dados = consulta_faturamento_por_entregador()

        nomes = []
        valores = []

        for item in dados:
            nomes.append(item.get("entregador", "Não informado"))
            valores.append(item.get("faturamento_total", 0))

        figura = Figure(figsize=(5, 3.5), dpi=100)
        grafico = figura.add_subplot(111)

        if len(valores) == 0:
            self.mostrar_sem_dados(grafico)
        else:
            grafico.barh(nomes, valores)
            grafico.set_title("Faturamento por Entregador")
            grafico.set_xlabel("Valor em R$")

        figura.tight_layout()
        self.exibir_figura(figura, frame)

    def criar_grafico_produtos(self, master, row, column):
        frame = self.criar_frame_grafico(master, row, column)

        dados = consulta_produtos_mais_vendidos()

        nomes = []
        valores = []

        for item in dados[:5]:
            nomes.append(item.get("produto", "Produto"))
            valores.append(item.get("quantidade_vendida", 0))

        figura = Figure(figsize=(5, 3.5), dpi=100)
        grafico = figura.add_subplot(111)

        if len(valores) == 0:
            self.mostrar_sem_dados(grafico)
        else:
            grafico.bar(nomes, valores)
            grafico.set_title("Produtos Mais Vendidos")
            grafico.set_ylabel("Quantidade")
            grafico.tick_params(axis="x", rotation=20)

        figura.tight_layout()
        self.exibir_figura(figura, frame)

    def criar_grafico_problemas_bairro(self, master, row, column):
        frame = self.criar_frame_grafico(master, row, column)

        dados = consulta_problemas_por_bairro()

        bairros = []
        valores = []

        for item in dados[:5]:
            bairros.append(item.get("bairro", "Não informado"))
            valores.append(item.get("total_problemas", 0))

        figura = Figure(figsize=(5, 3.5), dpi=100)
        grafico = figura.add_subplot(111)

        if len(valores) == 0:
            self.mostrar_sem_dados(grafico)
        else:
            grafico.bar(bairros, valores)
            grafico.set_title("Problemas por Bairro")
            grafico.set_ylabel("Quantidade")
            grafico.tick_params(axis="x", rotation=20)

        figura.tight_layout()
        self.exibir_figura(figura, frame)

    def mostrar_sem_dados(self, grafico):
        grafico.text(
            0.5,
            0.5,
            "Sem dados para exibir",
            ha="center",
            va="center",
            fontsize=12
        )
        grafico.set_axis_off()

    def formatar_status(self, status):
        status_formatado = {
            "em_curso": "Em Curso",
            "entregue": "Entregue",
            "problema": "Problema"
        }

        return status_formatado.get(status, status)