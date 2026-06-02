# SME - Sistema de Monitoramento de Entregas

Projeto desenvolvido para a disciplina de **Tópicos Especiais**, utilizando **Python**, **Flask**, **Tkinter** e **MongoDB**.

## Integrantes

- Ana Júlia Sanches
- Paulo Marcondes de Oliveira Filho

## Descrição do projeto

O **SME - Sistema de Monitoramento de Entregas** tem como objetivo auxiliar os responsáveis pelo acompanhamento e análise das entregas realizadas pelo Mercado Extra.

A proposta do sistema é tornar mais fácil e intuitiva a visualização dos dados das entregas, permitindo analisar informações importantes sobre uma ferramenta bastante utilizada atualmente: a entrega de produtos.

O projeto possui duas partes principais:

1. **Área do cliente**, desenvolvida com Flask, onde o cliente realiza um pedido.
2. **Sistema interno SME**, desenvolvido com Tkinter, onde o operador monitora as entregas, atualiza status e visualiza indicadores.

Os dados são armazenados em um banco de dados **MongoDB**, na coleção `Entrega`.

## Tecnologias utilizadas

- Python
- Flask
- Tkinter
- MongoDB
- MongoDB Compass
- PyMongo
- Matplotlib

## Requisitos para executar

Antes de rodar o projeto, é necessário ter instalado:

- Python
- MongoDB Server
- MongoDB Compass
- Pip

Também é necessário que o MongoDB esteja rodando na máquina.

## Instalação das dependências

No terminal, dentro da pasta do projeto, instale as bibliotecas necessárias:

```bash
pip install flask pymongo matplotlib
```

Caso exista um arquivo `requirements.txt`, também é possível usar:

```bash
pip install -r requirements.txt
```

## Banco de dados

O projeto utiliza o banco:

```text
SME_DB
```

E a coleção:

```text
Entrega
```

O MongoDB deve estar rodando em:

```text
mongodb://localhost:27017/
```

## Como popular o banco com dados de teste

Para inserir mais de 100 documentos no banco, execute o arquivo de popular dados:

```bash
python popular_banco.py
```

Esse arquivo cria vários pedidos de teste na coleção `Entrega`.

## Como executar a parte web

A parte web é a área do cliente, onde é possível selecionar produtos, preencher os dados da entrega e enviar o pedido para o MongoDB.

Para executar:

```bash
python app.py
```

Depois, abra no navegador:

```text
http://127.0.0.1:5000
```

Ao finalizar um pedido pela página web, ele será salvo no MongoDB e poderá ser visualizado no sistema SME.

## Como executar o sistema SME

O sistema SME é a parte interna utilizada pelo operador para acompanhar as entregas.

Para executar:

```bash
python main.py
```

A janela do sistema será aberta com as opções:

- Entregas em curso
- Entregas finalizadas
- Dashboard

## Ordem recomendada para usar o sistema

1. Abrir o MongoDB ou garantir que o serviço do MongoDB esteja rodando.
2. Abrir o MongoDB Compass e verificar a conexão com `localhost:27017`.
3. Rodar o arquivo `app.py` para iniciar a área web do cliente.
4. Acessar `http://127.0.0.1:5000` no navegador.
5. Criar um pedido pela página web.
6. Rodar o arquivo `main.py` para abrir o SME.
7. Visualizar o pedido em **Entregas em curso**.
8. Marcar a entrega como entregue, marcar problema ou excluir.
9. Acessar o Dashboard para visualizar os gráficos e indicadores.

## Funcionalidades implementadas

### Área web

- Seleção de produtos
- Carrinho de compras
- Cadastro dos dados do cliente
- Cadastro do endereço de entrega
- Opção de código de segurança
- Envio do pedido para o MongoDB

### Sistema SME

- Listagem de entregas em curso
- Listagem de entregas finalizadas
- Atualização de status da entrega
- Marcação de problema na entrega
- Exclusão de entrega
- Visualização de dashboard com gráficos
- Consulta dos dados armazenados no MongoDB

## Operações CRUD

O sistema realiza as quatro operações principais do CRUD:

- **Create:** criação de pedido pela página web.
- **Read:** leitura das entregas no sistema SME.
- **Update:** atualização do status da entrega para entregue ou problema.
- **Delete:** exclusão de entregas pelo sistema SME.

## Estrutura dos documentos no MongoDB

Exemplo dos principais campos utilizados na coleção `Entrega`:

```json
{
  "itens": [],
  "comprador": {},
  "entregador": {},
  "endereco": {},
  "observacao": "",
  "frete": 0,
  "valor_produtos": 0,
  "valor_total": 0,
  "codigo_seguranca": "",
  "status": "",
  "entregue": false,
  "problema_entrega": false,
  "descricao_problema": "",
  "data_pedido": "",
  "hora_pedido": "",
  "previsao_entrega": "",
  "data_entrega": "",
  "hora_entrega": "",
  "criado_em": null,
  "finalizado_em": null
}
```

A coleção possui campos de diferentes tipos, como:

- String
- Número
- Booleano
- Array
- Objeto
- Data
- Null

## Consultas e relatórios

O projeto possui consultas com filtros, operadores, projeções e agregações, utilizadas para análise dos dados das entregas.

Exemplos de consultas implementadas:

- Total de entregas por status
- Faturamento por entregador
- Produtos mais vendidos
- Problemas por bairro
- Entregas em curso com projeção de campos

Essas consultas são utilizadas principalmente no Dashboard do sistema SME.

## Observações

Para o sistema funcionar corretamente, é necessário que o MongoDB esteja rodando antes de executar o `app.py` e o `main.py`.

A parte web e o sistema SME utilizam o mesmo banco de dados. Portanto, os pedidos criados na página web aparecem automaticamente no sistema interno.