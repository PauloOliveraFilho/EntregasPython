import tkinter as tk

from widgets.header import Header

from Janelas.Dashboard import Dashboard
from Janelas.Entregas import Entregas


root = tk.Tk()

root.title("Sistema de Monitoramento de Entregas")

root.geometry("900x400")

header = Header(root)

container = tk.Frame(root)

container.pack(fill="both", expand=True)

# FUNÇÃO PARA TROCAR TELAS
def mostrarTela(tela):

    # remove tela antiga
    for widget in container.winfo_children():
        widget.destroy()

    # cria nova tela
    novaTela = tela(container)

    novaTela.pack(fill="both", expand=True)


# BOTÕES DO HEADER

header.addBotao(
    "Entregas Finalizadas",
    lambda: mostrarTela(Entregas)
)

header.addBotao(
    "Dashboard",
    lambda: mostrarTela(Dashboard)
)

# TELA INICIAL
mostrarTela(Entregas)

root.mainloop()