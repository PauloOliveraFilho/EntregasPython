from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["SME_DB"]
colecao = db["Entrega"]


def listar_entregas_em_curso():
    entregas = colecao.find({
        "status": "em_curso"
    }).sort("data_pedido", -1)

    return list(entregas)


def listar_entregas_finalizadas():
    entregas = colecao.find({
        "status": {"$in": ["entregue", "problema"]}
    }).sort("data_entrega", -1)

    return list(entregas)


def finalizar_entrega(id_entrega):
    agora = datetime.now()

    resultado = colecao.update_one(
        {"_id": ObjectId(id_entrega)},
        {
            "$set": {
                "status": "entregue",
                "entregue": True,
                "problema_entrega": False,
                "descricao_problema": "",
                "data_entrega": agora.strftime("%Y-%m-%d"),
                "hora_entrega": agora.strftime("%H:%M")
            }
        }
    )

    return resultado.modified_count > 0


def marcar_problema(id_entrega, descricao="Problema na entrega"):
    agora = datetime.now()

    resultado = colecao.update_one(
        {"_id": ObjectId(id_entrega)},
        {
            "$set": {
                "status": "problema",
                "entregue": False,
                "problema_entrega": True,
                "descricao_problema": descricao,
                "data_entrega": agora.strftime("%Y-%m-%d"),
                "hora_entrega": agora.strftime("%H:%M")
            }
        }
    )

    return resultado.modified_count > 0


def buscar_estatisticas():
    total = colecao.count_documents({})
    em_curso = colecao.count_documents({"status": "em_curso"})
    entregues = colecao.count_documents({"status": "entregue"})
    problemas = colecao.count_documents({"status": "problema"})

    return {
        "total": total,
        "em_curso": em_curso,
        "entregues": entregues,
        "problemas": problemas
    }

def excluir_entrega(id_entrega):
    resultado = colecao.delete_one({
        "_id": ObjectId(id_entrega)
    })

    return resultado.deleted_count > 0

def consulta_entregas_em_curso_resumida():
    entregas = colecao.find(
        {
            "$and": [
                {"status": "em_curso"},
                {"valor_total": {"$gte": 20}}
            ]
        },
        {
            "comprador.nome": 1,
            "comprador.telefone": 1,
            "endereco.bairro": 1,
            "valor_total": 1,
            "previsao_entrega": 1,
            "codigo_seguranca": 1,
            "status": 1
        }
    ).sort("valor_total", -1)

    return list(entregas)


def consulta_total_por_status():
    resultado = colecao.aggregate([
        {
            "$group": {
                "_id": "$status",
                "quantidade": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "quantidade": -1
            }
        }
    ])

    return list(resultado)


def consulta_faturamento_por_entregador():
    resultado = colecao.aggregate([
        {
            "$match": {
                "status": {"$in": ["entregue", "problema"]}
            }
        },
        {
            "$group": {
                "_id": "$entregador.nome",
                "total_entregas": {"$sum": 1},
                "faturamento_total": {"$sum": "$valor_total"},
                "media_por_entrega": {"$avg": "$valor_total"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "entregador": "$_id",
                "total_entregas": 1,
                "faturamento_total": 1,
                "media_por_entrega": 1
            }
        },
        {
            "$sort": {
                "faturamento_total": -1
            }
        }
    ])

    return list(resultado)


def consulta_problemas_por_bairro():
    resultado = colecao.aggregate([
        {
            "$match": {
                "problema_entrega": True
            }
        },
        {
            "$group": {
                "_id": "$endereco.bairro",
                "total_problemas": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "bairro": "$_id",
                "total_problemas": 1
            }
        },
        {
            "$sort": {
                "total_problemas": -1
            }
        }
    ])

    return list(resultado)


def consulta_produtos_mais_vendidos():
    resultado = colecao.aggregate([
        {
            "$unwind": "$itens"
        },
        {
            "$group": {
                "_id": "$itens.nome",
                "quantidade_vendida": {"$sum": "$itens.quantidade"},
                "faturamento_produto": {"$sum": "$itens.valor_total_item"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "produto": "$_id",
                "quantidade_vendida": 1,
                "faturamento_produto": 1
            }
        },
        {
            "$sort": {
                "quantidade_vendida": -1
            }
        },
        {
            "$limit": 10
        }
    ])

    return list(resultado)