from pymongo import MongoClient

cliente = MongoClient("mongodb://localhost:27017/")

db = cliente["SME_DB"]
colecao = db["Entrega"]

# CUIDADO:
# Se quiser apagar os dados antigos antes de inserir os novos, descomente a linha abaixo.
colecao.delete_many({})

entregas = [
    {
        "itens": [
            {
                "tipos": ["fruta", "alimento"],
                "nome": "Banana",
                "quantidade": 2,
                "preco_unitario": 4,
                "valor_total_item": 8
            }
        ],
        "comprador": {
            "nome": "Mercurio Silva",
            "cpf": "123.456.789-10",
            "telefone": "(15) 99123-2134"
        },
        "entregador": {
            "nome": "Juliana Souza",
            "matricula": "0001",
            "veiculo": {
                "tipo": "Moto",
                "marca": "Biz",
                "placa": "ACB-2345"
            }
        },
        "endereco": {
            "logradouro": "Rua Santos",
            "numero": 111,
            "complemento": "Fundos",
            "bairro": "Jardim das Rosas",
            "cidade": "Itapetininga"
        },
        "observacao": "Apertar a campainha.",
        "frete": 4,
        "valor_produtos": 8,
        "valor_total": 12,
        "status": "em_curso",
        "entregue": False,
        "problema_entrega": False,
        "descricao_problema": "",
        "data_pedido": "2026-05-25",
        "hora_pedido": "18:00",
        "previsao_entrega": "18:40",
        "data_entrega": None,
        "hora_entrega": None
    },
    {
        "itens": [
            {
                "tipos": ["bebida", "mercado"],
                "nome": "Refrigerante 2L",
                "quantidade": 1,
                "preco_unitario": 10,
                "valor_total_item": 10
            },
            {
                "tipos": ["alimento", "padaria"],
                "nome": "Pão Francês",
                "quantidade": 10,
                "preco_unitario": 1,
                "valor_total_item": 10
            }
        ],
        "comprador": {
            "nome": "Ana Carolina",
            "cpf": "222.333.444-55",
            "telefone": "(15) 99888-1122"
        },
        "entregador": {
            "nome": "Carlos Mendes",
            "matricula": "0002",
            "veiculo": {
                "tipo": "Moto",
                "marca": "Honda CG",
                "placa": "DEF-7788"
            }
        },
        "endereco": {
            "logradouro": "Avenida Peixoto Gomide",
            "numero": 450,
            "complemento": "Casa 2",
            "bairro": "Centro",
            "cidade": "Itapetininga"
        },
        "observacao": "Entregar na garagem.",
        "frete": 6,
        "valor_produtos": 20,
        "valor_total": 26,
        "status": "em_curso",
        "entregue": False,
        "problema_entrega": False,
        "descricao_problema": "",
        "data_pedido": "2026-05-25",
        "hora_pedido": "18:10",
        "previsao_entrega": "18:55",
        "data_entrega": None,
        "hora_entrega": None
    },
    {
        "itens": [
            {
                "tipos": ["limpeza"],
                "nome": "Detergente",
                "quantidade": 3,
                "preco_unitario": 3,
                "valor_total_item": 9
            },
            {
                "tipos": ["limpeza"],
                "nome": "Esponja",
                "quantidade": 2,
                "preco_unitario": 2,
                "valor_total_item": 4
            }
        ],
        "comprador": {
            "nome": "Roberto Lima",
            "cpf": "333.444.555-66",
            "telefone": "(15) 99777-3344"
        },
        "entregador": {
            "nome": "Fernanda Alves",
            "matricula": "0003",
            "veiculo": {
                "tipo": "Carro",
                "marca": "Fiat Uno",
                "placa": "GHI-9090"
            }
        },
        "endereco": {
            "logradouro": "Rua Campos Sales",
            "numero": 89,
            "complemento": "",
            "bairro": "Vila Rio Branco",
            "cidade": "Itapetininga"
        },
        "observacao": "Cliente pediu para ligar antes.",
        "frete": 5,
        "valor_produtos": 13,
        "valor_total": 18,
        "status": "entregue",
        "entregue": True,
        "problema_entrega": False,
        "descricao_problema": "",
        "data_pedido": "2026-05-24",
        "hora_pedido": "14:20",
        "previsao_entrega": "15:00",
        "data_entrega": "2026-05-24",
        "hora_entrega": "14:52"
    },
    {
        "itens": [
            {
                "tipos": ["fruta", "alimento"],
                "nome": "Maçã",
                "quantidade": 5,
                "preco_unitario": 2,
                "valor_total_item": 10
            },
            {
                "tipos": ["fruta", "alimento"],
                "nome": "Laranja",
                "quantidade": 6,
                "preco_unitario": 1.5,
                "valor_total_item": 9
            }
        ],
        "comprador": {
            "nome": "Beatriz Moraes",
            "cpf": "444.555.666-77",
            "telefone": "(15) 99666-5566"
        },
        "entregador": {
            "nome": "Juliana Souza",
            "matricula": "0001",
            "veiculo": {
                "tipo": "Moto",
                "marca": "Biz",
                "placa": "ACB-2345"
            }
        },
        "endereco": {
            "logradouro": "Rua José Bonifácio",
            "numero": 210,
            "complemento": "Apartamento 12",
            "bairro": "Centro",
            "cidade": "Itapetininga"
        },
        "observacao": "Entregar na portaria.",
        "frete": 7,
        "valor_produtos": 19,
        "valor_total": 26,
        "status": "entregue",
        "entregue": True,
        "problema_entrega": False,
        "descricao_problema": "",
        "data_pedido": "2026-05-24",
        "hora_pedido": "16:30",
        "previsao_entrega": "17:10",
        "data_entrega": "2026-05-24",
        "hora_entrega": "17:05"
    },
    {
        "itens": [
            {
                "tipos": ["alimento", "mercearia"],
                "nome": "Arroz 5kg",
                "quantidade": 1,
                "preco_unitario": 28,
                "valor_total_item": 28
            },
            {
                "tipos": ["alimento", "mercearia"],
                "nome": "Feijão 1kg",
                "quantidade": 2,
                "preco_unitario": 9,
                "valor_total_item": 18
            }
        ],
        "comprador": {
            "nome": "João Pedro",
            "cpf": "555.666.777-88",
            "telefone": "(15) 99555-7788"
        },
        "entregador": {
            "nome": "Carlos Mendes",
            "matricula": "0002",
            "veiculo": {
                "tipo": "Moto",
                "marca": "Honda CG",
                "placa": "DEF-7788"
            }
        },
        "endereco": {
            "logradouro": "Rua das Palmeiras",
            "numero": 300,
            "complemento": "",
            "bairro": "Jardim Itália",
            "cidade": "Itapetininga"
        },
        "observacao": "Sem observações.",
        "frete": 8,
        "valor_produtos": 46,
        "valor_total": 54,
        "status": "problema",
        "entregue": False,
        "problema_entrega": True,
        "descricao_problema": "Cliente não estava no endereço.",
        "data_pedido": "2026-05-23",
        "hora_pedido": "19:15",
        "previsao_entrega": "20:00",
        "data_entrega": "2026-05-23",
        "hora_entrega": "20:05"
    },
    {
        "itens": [
            {
                "tipos": ["higiene"],
                "nome": "Sabonete",
                "quantidade": 4,
                "preco_unitario": 3.5,
                "valor_total_item": 14
            },
            {
                "tipos": ["higiene"],
                "nome": "Papel Higiênico",
                "quantidade": 1,
                "preco_unitario": 18,
                "valor_total_item": 18
            }
        ],
        "comprador": {
            "nome": "Larissa Gomes",
            "cpf": "666.777.888-99",
            "telefone": "(15) 99444-9900"
        },
        "entregador": {
            "nome": "Fernanda Alves",
            "matricula": "0003",
            "veiculo": {
                "tipo": "Carro",
                "marca": "Fiat Uno",
                "placa": "GHI-9090"
            }
        },
        "endereco": {
            "logradouro": "Rua Padre Albuquerque",
            "numero": 75,
            "complemento": "Bloco B",
            "bairro": "Vila Nastri",
            "cidade": "Itapetininga"
        },
        "observacao": "Deixar com o porteiro.",
        "frete": 6,
        "valor_produtos": 32,
        "valor_total": 38,
        "status": "em_curso",
        "entregue": False,
        "problema_entrega": False,
        "descricao_problema": "",
        "data_pedido": "2026-05-25",
        "hora_pedido": "19:00",
        "previsao_entrega": "19:45",
        "data_entrega": None,
        "hora_entrega": None
    },
    {
        "itens": [
            {
                "tipos": ["bebida"],
                "nome": "Suco de Uva",
                "quantidade": 2,
                "preco_unitario": 7,
                "valor_total_item": 14
            }
        ],
        "comprador": {
            "nome": "Eduardo Ferreira",
            "cpf": "777.888.999-00",
            "telefone": "(15) 99333-1212"
        },
        "entregador": {
            "nome": "Juliana Souza",
            "matricula": "0001",
            "veiculo": {
                "tipo": "Moto",
                "marca": "Biz",
                "placa": "ACB-2345"
            }
        },
        "endereco": {
            "logradouro": "Rua General Carneiro",
            "numero": 1020,
            "complemento": "",
            "bairro": "Centro",
            "cidade": "Itapetininga"
        },
        "observacao": "Chamar no WhatsApp ao chegar.",
        "frete": 5,
        "valor_produtos": 14,
        "valor_total": 19,
        "status": "entregue",
        "entregue": True,
        "problema_entrega": False,
        "descricao_problema": "",
        "data_pedido": "2026-05-22",
        "hora_pedido": "13:40",
        "previsao_entrega": "14:20",
        "data_entrega": "2026-05-22",
        "hora_entrega": "14:18"
    },
    {
        "itens": [
            {
                "tipos": ["alimento", "frios"],
                "nome": "Queijo Mussarela",
                "quantidade": 1,
                "preco_unitario": 22,
                "valor_total_item": 22
            },
            {
                "tipos": ["alimento", "frios"],
                "nome": "Presunto",
                "quantidade": 1,
                "preco_unitario": 18,
                "valor_total_item": 18
            }
        ],
        "comprador": {
            "nome": "Camila Ribeiro",
            "cpf": "888.999.000-11",
            "telefone": "(15) 99222-3434"
        },
        "entregador": {
            "nome": "Carlos Mendes",
            "matricula": "0002",
            "veiculo": {
                "tipo": "Moto",
                "marca": "Honda CG",
                "placa": "DEF-7788"
            }
        },
        "endereco": {
            "logradouro": "Rua Benedito Marques",
            "numero": 600,
            "complemento": "Casa verde",
            "bairro": "Jardim Fogaça",
            "cidade": "Itapetininga"
        },
        "observacao": "Não buzinar.",
        "frete": 9,
        "valor_produtos": 40,
        "valor_total": 49,
        "status": "problema",
        "entregue": False,
        "problema_entrega": True,
        "descricao_problema": "Endereço informado estava incorreto.",
        "data_pedido": "2026-05-23",
        "hora_pedido": "17:30",
        "previsao_entrega": "18:15",
        "data_entrega": "2026-05-23",
        "hora_entrega": "18:25"
    }
]

resultado = colecao.insert_many(entregas)

print(f"{len(resultado.inserted_ids)} entregas inseridas com sucesso.")