# Mercadin-API

Mercadin é uma API que te dá todo o controle sobre
o banco de dados de seu mercadinho/mercearia

Atenção: para usar esta API, você pode ou subir o projeto para o Heroku, criando um fork desse projeto e ligando ele a um projeto ou você pode usar ele localmente.

# Instalação e uso

Para o uso local, é necessário fazer os seguintes passo:

```
#Para baixar a API:
  git clone https://github.com/oopaze/Mercadin-API.git

#Entar na pasta do projeto:
  cd Mercadin-API

#Instalar os requirements:
  pip install -r requirements.txt

#Iniciliazar o banco SQLite3:
  flask db init
  flask db migrate
  flask db upgrade

#Rodar a API:
  flask run
```

Neste poto a sua API vai dá rodando no endereço http://127.0.0.1:5000/

# Endpoints

Os seguintes endpoints estão configurados

## Home - não há nada aqui

- `/` - GET

## Setores

Todo setor é composto por um name, slug porém o campo slug não necessita ser enviado, pois é gerado a partir do name. Para adição/atuaização de um setor, é necessário se enviar um JSON contendo a chave data como por exemplo:
```
  {
    "data": {
      "name": Nome do setor
    }
  }
```

O setor gerado terá os respectivos campos:
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

Todo produto é composto por um nome, um preço, um peso, um quantidade e um setor. Para adição/atualização de um produto, é necessário se enviar um JSON contendo a chave data como por exemplo:
  ```
  {
    "data":{
      "name": nome do produto -> String
      "price": preço -> Int
      "weight": peso -> Int
      "amount": quantidade -> int
      "sector": slug do setor -> String
    }
  }
  ```

O produto gerado terá os respectivos campos:
```
  "name": nome
  "price": preço
  "weight": peso
  "amount": quantidade
```

- `/products/` - GET - Mostra todos os produtos
- `/products/:product_id` - GET - Mostra o produto do ID enviado
- `/products/` - POST - Cria um produto
- `/products/:product_id` - PUT - Atualiza o produto de ID enviado
- `/products/:product_id` - DELETE - Deleta o produto de ID enviado

## Carrinhos
## Funcionários
## Vendas
