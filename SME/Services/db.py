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