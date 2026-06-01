import tkinter as tk
from tkinter import messagebox, simpledialog

from Services.db import finalizar_entrega, marcar_problema, excluir_entrega


class Card(tk.Frame):

    def __init__(self, master, entregaData, tipo="em_curso"):
        super().__init__(
            master,
            bg="#ffffff",
            bd=1,
            relief=tk.SOLID,
            padx=0,
            pady=0
        )

        self.entrega = entregaData
        self.tipo = tipo

        self.criar_card()

    def criar_card(self):
        comprador = self.entrega.get("comprador", {})
        entregador = self.entrega.get("entregador", {})
        endereco = self.entrega.get("endereco", {})

        # Cabeçalho do card
        header = tk.Frame(self, bg="#eef2f7", padx=12, pady=8)
        header.pack(fill="x")

        nome_cliente = comprador.get("nome", "Cliente não informado")
        status = self.entrega.get("status", "sem status")

        label_cliente = tk.Label(
            header,
            text=nome_cliente,
            font=("Arial", 13, "bold"),
            bg="#eef2f7",
            anchor="w"
        )
        label_cliente.pack(side="left", fill="x", expand=True)

        label_status = tk.Label(
            header,
            text=self.formatar_status(status),
            font=("Arial", 10, "bold"),
            bg=self.cor_status(status),
            fg="white",
            padx=10,
            pady=3
        )
        label_status.pack(side="right")

        # Corpo do card
        corpo = tk.Frame(self, bg="#ffffff", padx=12, pady=10)
        corpo.pack(fill="x")

        coluna_esquerda = tk.Frame(corpo, bg="#ffffff")
        coluna_esquerda.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        coluna_direita = tk.Frame(corpo, bg="#ffffff")
        coluna_direita.grid(row=0, column=1, sticky="nsew")

        corpo.grid_columnconfigure(0, weight=1)
        corpo.grid_columnconfigure(1, weight=1)

        # Seções
        secao_cliente = self.criar_secao(coluna_esquerda, "Dados do Cliente")
        self.adicionar_linha(secao_cliente, "Telefone", comprador.get("telefone", ""))
        self.adicionar_linha(secao_cliente, "CPF", comprador.get("cpf", ""))

        secao_pedido = self.criar_secao(coluna_esquerda, "Pedido")
        self.adicionar_linha(secao_pedido, "Itens", self.formatar_itens())
        self.adicionar_linha(secao_pedido, "Frete", self.moeda(self.entrega.get("frete", 0)))
        self.adicionar_linha(secao_pedido, "Total", self.moeda(self.entrega.get("valor_total", 0)))

        secao_entregador = self.criar_secao(coluna_direita, "Entregador")
        self.adicionar_linha(secao_entregador, "Nome", entregador.get("nome", ""))
        self.adicionar_linha(secao_entregador, "Matrícula", entregador.get("matricula", ""))

        veiculo = entregador.get("veiculo", {})
        self.adicionar_linha(secao_entregador, "Veículo", self.formatar_veiculo(veiculo))

        secao_endereco = self.criar_secao(coluna_direita, "Endereço")
        endereco_completo = self.formatar_endereco(endereco)
        self.adicionar_linha(secao_endereco, "Local", endereco_completo)

        secao_datas = self.criar_secao(coluna_direita, "Controle")
        self.adicionar_linha(secao_datas, "Pedido", self.formatar_data_hora("data_pedido", "hora_pedido"))

        if self.tipo == "em_curso":
            self.adicionar_linha(secao_datas, "Previsão", self.entrega.get("previsao_entrega", ""))

            codigo = self.entrega.get("codigo_seguranca", "Desativado")

            if codigo and codigo != "Desativado":
                self.adicionar_linha(secao_datas, "Código", codigo)
            else:
                self.adicionar_linha(secao_datas, "Código", "Não solicitado")
        else:
            self.adicionar_linha(secao_datas, "Entrega", self.formatar_data_hora("data_entrega", "hora_entrega"))

            codigo = self.entrega.get("codigo_seguranca", "Desativado")

            if codigo and codigo != "Desativado":
                self.adicionar_linha(secao_datas, "Código", codigo)

        observacao = self.entrega.get("observacao", "")
        problema_entrega = self.entrega.get("problema_entrega", False)

        if observacao or problema_entrega:
            area_extra = tk.Frame(self, bg="#ffffff", padx=12, pady=5)
            area_extra.pack(fill="x")

        if observacao:
            secao_obs = self.criar_secao(area_extra, "Observação")
            self.adicionar_linha(secao_obs, "Obs.", observacao)

        if problema_entrega:
            secao_problema = self.criar_secao(area_extra, "Problema na Entrega")
            self.adicionar_linha(
            secao_problema,
            "Descrição",
            self.entrega.get("descricao_problema", "")
        )

        # Rodapé com botões
        rodape = tk.Frame(self, bg="#ffffff", padx=12, pady=10)
        rodape.pack(fill="x")

        if self.tipo == "em_curso":
            btn_entregue = tk.Button(
                rodape,
                text="Marcar como entregue",
                command=self.marcar_como_entregue,
                bg="#2e7d32",
                fg="white",
                padx=10,
                pady=5,
                relief=tk.FLAT,
                cursor="hand2"
            )
            btn_entregue.pack(side="left", padx=(0, 8))

            btn_problema = tk.Button(
                rodape,
                text="Marcar problema",
                command=self.marcar_como_problema,
                bg="#c62828",
                fg="white",
                padx=10,
                pady=5,
                relief=tk.FLAT,
                cursor="hand2"
            )
            btn_problema.pack(side="left")

        btn_excluir = tk.Button(
            rodape,
            text="Excluir",
            command=self.excluir,
            bg="#555555",
            fg="white",
            padx=10,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_excluir.pack(side="right")

    def criar_secao(self, master, titulo):
        frame = tk.Frame(master, bg="#ffffff", pady=4)
        frame.pack(fill="x", anchor="n")

        label_titulo = tk.Label(
            frame,
            text=titulo,
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#333333",
            anchor="w"
        )
        label_titulo.pack(fill="x", pady=(0, 4))

        return frame

    def adicionar_linha(self, master, rotulo, valor):
        linha = tk.Frame(master, bg="#ffffff")
        linha.pack(fill="x", pady=1)

        label_rotulo = tk.Label(
            linha,
            text=f"{rotulo}:",
            font=("Arial", 9, "bold"),
            bg="#ffffff",
            fg="#555555",
            width=10,
            anchor="w"
        )
        label_rotulo.pack(side="left", anchor="n")

        label_valor = tk.Label(
            linha,
            text=str(valor),
            font=("Arial", 9),
            bg="#ffffff",
            fg="#222222",
            justify="left",
            anchor="w",
            wraplength=350
        )
        label_valor.pack(side="left", fill="x", expand=True)

    def formatar_itens(self):
        itens = self.entrega.get("itens", [])

        if not itens:
            return "Nenhum item informado"

        textos = []

        for item in itens:
            nome = item.get("nome", "")
            quantidade = item.get("quantidade", 0)
            preco = item.get("preco_unitario", 0)
            total = item.get("valor_total_item", quantidade * preco)

            textos.append(
                f"{nome} ({quantidade}x) - {self.moeda(total)}"
            )

        return "\n".join(textos)

    def formatar_veiculo(self, veiculo):
        tipo = veiculo.get("tipo", "")
        marca = veiculo.get("marca", "")
        placa = veiculo.get("placa", "")

        return f"{tipo} {marca} - {placa}"

    def formatar_endereco(self, endereco):
        logradouro = endereco.get("logradouro", "")
        numero = endereco.get("numero", "")
        complemento = endereco.get("complemento", "")
        bairro = endereco.get("bairro", "")
        cidade = endereco.get("cidade", "")

        texto = f"{logradouro}, {numero}"

        if complemento:
            texto += f" - {complemento}"

        texto += f"\n{bairro} - {cidade}"

        return texto

    def formatar_data_hora(self, campo_data, campo_hora):
        data = self.entrega.get(campo_data)
        hora = self.entrega.get(campo_hora)

        if data and hora:
            return f"{data} às {hora}"

        if data:
            return data

        if hora:
            return hora

        return "Não informado"

    def formatar_status(self, status):
        status_formatado = {
            "em_curso": "EM CURSO",
            "entregue": "ENTREGUE",
            "problema": "PROBLEMA"
        }

        return status_formatado.get(status, status.upper())

    def cor_status(self, status):
        cores = {
            "em_curso": "#1565c0",
            "entregue": "#2e7d32",
            "problema": "#c62828"
        }

        return cores.get(status, "#555555")

    def moeda(self, valor):
        try:
            return f"R$ {float(valor):.2f}".replace(".", ",")
        except:
            return "R$ 0,00"

    def marcar_como_entregue(self):
        resultado = finalizar_entrega(str(self.entrega["_id"]))

        if resultado is False:
            messagebox.showerror("Erro", "Não foi possível finalizar a entrega.")
            return

        messagebox.showinfo("Sucesso", "Entrega marcada como entregue.")
        self.destroy()

    def marcar_como_problema(self):
        descricao = simpledialog.askstring(
            "Problema na entrega",
            "Descreva o problema da entrega:",
            initialvalue="Problema na entrega"
        )

        if descricao is None:
            return

        resultado = marcar_problema(str(self.entrega["_id"]), descricao)

        if resultado is False:
            messagebox.showerror("Erro", "Não foi possível marcar problema na entrega.")
            return

        messagebox.showinfo("Sucesso", "Entrega marcada com problema.")
        self.destroy()

    def excluir(self):
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Tem certeza que deseja excluir esta entrega?"
        )

        if not confirmar:
            return

        resultado = excluir_entrega(str(self.entrega["_id"]))

        if resultado is False:
            messagebox.showerror("Erro", "Não foi possível excluir a entrega.")
            return

        messagebox.showinfo("Sucesso", "Entrega excluída com sucesso.")
        self.destroy()