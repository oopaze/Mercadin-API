# Mercadin-API

Mercadin é uma API que te dá todo o controle sobre
o banco de dados de seu mercadinho/mercearia

Atenção: para usar esta API, você pode ou subir o projeto para o Heroku, criando um fork desse projeto e ligando ele a um projeto ou você pode usar ele localmente.

# Instalação e uso

Para o uso local, é necessário fazer os seguintes passo:

**Abra o terminal na pasta que deseja trabalhar e rode os seguintes comandos**

```
#Para baixar a API:
  git clone https://github.com/oopaze/Mercadin-API.git

#Entrar na pasta do projeto:
  cd Mercadin-API

#Instalar os requirements:
  pip install -r requirements.txt

#Aponte o flask para a aplicação Mercadin-API:
  #Windows:
    set FLASK_APP=run.py
  #Linux:
    export FLASK_APP=run.py

#Iniciliazar o banco SQLite3:
  flask db init
  flask db migrate
  flask db upgrade

#Rodar a API:
  flask run
```

Neste ponto a sua API vai está rodando no endereço http://127.0.0.1:5000/

# Endpoints

Os seguintes endpoints estão configurados

## Home - não há nada aqui

- `/` - GET

## Setores

Todo setor é composto por um name, slug porém o campo slug não necessita ser enviado, pois é gerado a partir do name. Para adição/atuaização de um setor, é necessário se enviar um JSON contendo a chave data com o campo "name"

**como por exemplo:**
```
  {
    "data": {
      "name": Nome do setor
    }
  }
```

**O setor gerado terá os respectivos campos:**
```
  "name": Nome do setor
  "slug": nome_do_setor
```

- `/sectors/` - GET - Mostra todos os setores
- `/sectors/:slug` - GET - Mostra o setor de slug enviado e os produtos contidos no mesmo
- `/sectors/` - POST - Cria um setor
- `/sectors/:slug` - PUT - Atualiza o setor de slug enviado
- `/sectors/:slug` - DELETE - Deleta um setor de slug enviado

## Produtos

Todo produto é composto por um nome, um preço, um peso, um quantidade e um setor. Para adição/atualização de um produto, é necessário se enviar um JSON contendo a chave data com as chaves "name", "price", "weight", "amount", "sector"

**como por exemplo:**
  ```
  #Se um produto
      {
        "data":{
          "name": nome do produto -> String
          "price": preço -> Int
          "weight": peso -> Int
          "amount": quantidade -> int
          "sector": slug do setor -> String
        }
      }

  #Se mais que um:
    {
      "data":{
        "1":{
          "name": nome do produto -> String
          "price": preço -> Int
          "weight": peso -> Int
          "amount": quantidade -> int
          "sector": slug do setor -> String
        },
        "2":{
          "name": nome do produto -> String
          "price": preço -> Int
          "weight": peso -> Int
          "amount": quantidade -> int
          "sector": slug do setor -> String
        }
      }
    }
  ```

**O produto gerado terá os respectivos campos:**
```
  "name": nome
  "price": preço
  "weight": peso
  "amount": quantidade
```

- `/products/` - GET - Mostra todos os produtos
- `/products/:product_id` - GET - Mostra o produto do ID enviado
- `/products/` - POST - Cria um produto
- `/products/many` - POST - Cria vários produto
- `/products/:product_id` - PUT - Atualiza o produto de ID enviado
- `/products/:product_id` - DELETE - Deleta o produto de ID enviado

## Carrinhos

Todo carrinho é composto por um preço total, os produtos e um dono, porém o carrinho é inicializado vazio, mas vai se alterando ao longo do processo. Para adição de um carrinho, não é necessário a chave data no JSON.

**Como por exemplo:**
```
  {}
```

**O carrinho ficará no seguinte estado:**
```
total_price = preço total -> Int
owner = ID de um funcionario -> Int
products = produtos adicionado -> Products
```

Para a adição de produtos a um carrinho, basta passar um JSON contendo a chave data com os campos "product_id", "product_amount"

**Como por exemplo:**
```
  {
    "data": {
      "product_id": id do produto a ser adicionado ao carrinho,
      "product_amount": quantidade do produto a ser adicionado ao carrinho
    }
  }
```

- `/carts/` - GET - Mostra todos os carrinhos disponíveis
- `/carts/:cart_id` - GET - Mostra o carrinho de ID enviado e os produtos que ali estão
- `/carts/` - POST - Cria um carrinho
- `/carts/:cart_id` - POST - Adiciona produtos ao carrinho
- `/carts/:cart_id/:product_id` - DELETE - Deleta produto de ID eviado do carrinho de ID enviado
- `/carts/:cart_id` - DELETE - Deleta carrinho de ID enviado

## Funcionários
## Vendas
