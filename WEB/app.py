from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# CONEXÃO COM O MONGODB
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["SME_DB"]
colecao = db["Entrega"]


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/api/status", methods=["GET"])
def verificar_status():
    try:
        cliente.admin.command("ping")

        return jsonify({
            "status": "ok",
            "mensagem": "Conexão com MongoDB funcionando."
        })

    except Exception as erro:
        return jsonify({
            "status": "erro",
            "mensagem": str(erro)
        }), 500


@app.route("/api/pedidos", methods=["POST"])
def criar_pedido():
    dados = request.get_json() or {}

    agora = datetime.now()
    previsao = agora + timedelta(minutes=45)

    produtos = dados.get("produtos", [])
    itens = converter_produtos_para_itens(produtos)

    valor_produtos = calcular_valor_produtos(itens)
    frete = float(dados.get("frete", 8))
    valor_total = valor_produtos + frete

    pedido = {
        "itens": itens,

        "comprador": {
            "nome": dados.get("cliente", "Cliente não informado"),
            "cpf": dados.get("cpf", "Não informado"),
            "telefone": dados.get("telefone", "")
        },

        "entregador": {
            "nome": "Aguardando associação",
            "matricula": "",
            "veiculo": {
                "tipo": "",
                "marca": "",
                "placa": ""
            }
        },

        "endereco": {
            "logradouro": dados.get("logradouro", dados.get("endereco", "")),
            "numero": dados.get("numero", ""),
            "complemento": dados.get("complemento", ""),
            "bairro": dados.get("bairro", ""),
            "cidade": dados.get("cidade", "Itapetininga")
        },

        "observacao": dados.get("observacao", ""),

        "frete": frete,
        "valor_produtos": valor_produtos,
        "valor_total": valor_total,

        "codigo_seguranca": gerar_codigo_seguranca(dados),

        "status": "em_curso",
        "entregue": False,
        "problema_entrega": False,
        "descricao_problema": "",

        "data_pedido": agora.strftime("%Y-%m-%d"),
        "hora_pedido": agora.strftime("%H:%M"),
        "previsao_entrega": previsao.strftime("%H:%M"),

        "data_entrega": None,
        "hora_entrega": None
    }

    resultado = colecao.insert_one(pedido)

    pedido["_id"] = str(resultado.inserted_id)

    return jsonify({
        "mensagem": "Pedido cadastrado com sucesso.",
        "pedido": pedido
    }), 201


def converter_produtos_para_itens(produtos):
    itens = []

    for produto in produtos:
        nome = produto.get("nome", "Produto sem nome")
        quantidade = int(produto.get("qtd", produto.get("quantidade", 1)))
        preco = float(produto.get("preco", produto.get("preco_unitario", 0)))

        item = {
            "tipos": ["mercado"],
            "nome": nome,
            "quantidade": quantidade,
            "preco_unitario": preco,
            "valor_total_item": quantidade * preco
        }

        itens.append(item)

    return itens


def calcular_valor_produtos(itens):
    total = 0

    for item in itens:
        total += item.get("valor_total_item", 0)

    return total


def gerar_codigo_seguranca(dados):
    codigo_ativo = dados.get("codigoSeguranca", False)

    if codigo_ativo:
        return str(random.randint(1000, 9999))

    return "Desativado"

if __name__ == "__main__":
    app.run(debug=True)