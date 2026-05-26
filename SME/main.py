import tkinter as tk

from Widgets.header import Header

from Janelas.Dashboard import Dashboard
from Janelas.Entregas import Entregas


root = tk.Tk()

root.title("Sistema de Monitoramento de Entregas")

root.geometry("1100x650")
root.minsize(900, 500)

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
    "Entregas em Curso",
    lambda: mostrarTela(lambda master: Entregas(master, tipo="em_curso"))
)

header.addBotao(
    "Entregas Finalizadas",
    lambda: mostrarTela(lambda master: Entregas(master, tipo="finalizadas"))
)

header.addBotao(
    "Dashboard",
    lambda: mostrarTela(Dashboard)
)

mostrarTela(lambda master: Entregas(master, tipo="em_curso"))

root.mainloop()