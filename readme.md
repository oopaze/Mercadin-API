# Mercadin-API

Mercadin é uma API que te dá todo o controle sobre
o banco de dados de seu mercadinho/mercearia

Atenção: para usar esta API, você pode ou subir o projeto para o Heroku, criando um fork desse projeto e ligando ele a um projeto ou você pode usar ele localmente.

# Instalação

Para o uso dessa API, é necessário o python-3.7+
Se você for usar ela no heroku é necessário instalar o add-on Heroku-Postgres

**Abra o terminal na pasta que deseja trabalhar e rode os seguintes comandos**

```
Para baixar a API:
  git clone https://github.com/oopaze/Mercadin-API.git

Entrar na pasta do projeto:
  cd Mercadin-API

Instalar bibliotecas necessárias:
  pip install -r requirements.txt

Iniciliazar o banco SQLite3:
    flask db init
    flask db migrate
    flask db upgrade


Rodar a API:
  flask run
```

Neste ponto a sua API vai está rodando no endereço http://127.0.0.1:5000/

# Uso

A API no seu total segue uma estrutura de funcionamento.

Para controle de estoque, você será obrigado a manter sempre um produto ligado a um setor, já que API trás modos de acessar produtos setorialmente.
```
  setor <-> produtos
```

Para o controle de vendas, você deverá sempre seguir o fluxo abaixo:
```
  produto -> carrinho -> funcionário -> venda
```
Sempre se deve lotar carrinhos de produtos, adicionar carrinho ao funcionário e então gerar a venda desse carrinho. Qualquer tentativa de saída do fluxo, poderá ocorrer erro.


# Endpoints

Os seguintes endpoints estão configurados

## Home - não há nada aqui

- `/` - GET

## Setores

- `/sectors/` - GET - Mostra todos os setores
- `/sectors/:slug` - GET - Mostra o setor de slug enviado e os produtos contidos no mesmo
- `/sectors/` - POST - Cria um setor
- `/sectors/:slug` - PUT - Atualiza o setor de slug enviado
- `/sectors/:slug` - DELETE - Deleta um setor de slug enviado

Todo setor é composto por um name, slug porém o campo slug não necessita ser enviado, pois é gerado a partir do name. Para adição/atuaização de um setor, é necessário se enviar um JSON contendo a chave data com o campo "name"

**como por exemplo:**
```
  {
    "data": {
      "name": Nome do setor
    }
```
}

**O setor gerado terá os respectivos campos:**
```
  "name": Nome do setor
  "slug": nome_do_setor
```


## Produtos

- `/products/` - GET - Mostra todos os produtos
- `/products/:id_do_produto` - GET - Mostra o produto do ID enviado
- `/products/` - POST - Cria um produto
- `/products/many` - POST - Cria vários produto
- `/products/:id_do_produto` - PUT - Atualiza o produto de ID enviado
- `/products/:id_do_produto` - DELETE - Deleta o produto de ID enviado

Todo produto é composto por um nome, um preço, um peso, um quantidade e um setor. Para adição/atualização de um produto, é necessário se enviar um JSON contendo a chave data com as chaves "name", "price", "weight", "amount", "sector"

**como por exemplo:**
  ### Se um produto

      {
        "data":{
          "name": nome do produto -> String
          "price": preço -> Int
          "weight": peso -> Int
          "amount": quantidade -> int
          "sector": slug do setor -> String
        }
      }

  ### Se mais que um:
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


**O produto gerado terá os respectivos campos:**
```
  "name": nome
  "price": preço
  "weight": peso
  "amount": quantidade
```


## Carrinhos

- `/carts/` - GET - Mostra todos os carrinhos disponíveis
- `/carts/:id_do_carrinho` - GET - Mostra o carrinho de ID enviado e os seus produtos
- `/carts/` - POST - Cria um carrinho
- `/carts/:id_do_carrinho` - POST - Adiciona produtos ao carrinho
- `/carts/:id_do_carrinho/:id_do_produto` - DELETE - Tira produto de ID enviado do carrinho
- `/carts/:id_do_carrinho` - DELETE - Deleta carrinho de ID enviado

Todo carrinho é composto por um preço total, os produtos e um dono, porém o carrinho é inicializado vazio e vai sendo alterando ao longo do processo. Para adição de um carrinho, não é necessário a chave data no JSON e nem mesmo um JSON.

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


## Funcionários

- `/employees/` - GET - Mostra todos os funcionários
- `/employees/:id_do_funcionario` - GET - Mostra dados do funcionário de ID enviado
- `/employees/` - POST - Cria novo funcionário
- `/employees/:id_do_funcionario/:id_do_carrinho/new-cart` - POST - Adiciona ao funcionário de ID enviado o carrinho
- `/employees:id_do_funcionario/:id_do_carrinho/new-sale/` - POST - Transforma o carrinho em uma venda feita pelo funcionário de ID enviado
- `/employees/:id_do_funcionario` - PUT - Atualiza funcionário de ID enviado
- `/employees/:id_do_funcionario` - DELETE - Deleta funcionário de ID enviado
- `/employees/:id_do_funcionario/:id_do_carrinho` - DELETE - Retira do funcionário de ID enviado o carrinho

Todo funcionário é composto por um nome, uma senha e um admin. Para adição/atualização de um funcionário é necessário o envio de um JSON contendo a chave data com os campos "name", "password", "admin"

**Como por exemplo:**
```
  {
    "data": {
      "name": nome do funcionário,
      "password": senha do funcionário,
      "admin": se o funcionário é administrador
    }
  }
```

**O funcionário gerado terá os respectivos campos:**
```
  "name": nome do funcionário -> String
  "password": hash gerado a partir da senha do funcionário -> Hash
  "registration": matricula do funcionário -> Int
  "admin": boolean mostrando se o funcionário é admin -> Boolean
  "carts": todos os carts adicionados ao funcionário -> Carts
  "sales": todas as vendas feitas pelo funcionário -> Sales
```


## Vendas

- `/sales/` - GET - Mostra todas as vendas já efetuadas
- `/sales/:id_da_venda` - GET - Mostra venda de ID enviado
- `/sales/:id_da_venda/:id_do_produto` - DELETE - Retira produto de id enviado da venda
- `/sales/:id_da_venda` - DELETE - Deleta venda de ID enviado

Toda venda é composta por um cliente(argumento opcional), um preço total, produtos, um vendedor e data de quando foi efetuada. No entanto a adição de uma venda não está disponível por meios diretos. Seguindo fluxo de venda, toda venda deve ser derivada de um carrinho e gerada por um funcionário. O único campo que pode mutável(deletado) diretamente são os seus produtos.

**A venda gerada terá os respectivos campos:**
```
  "costumer": nome do cliente -> String
  "total_price": preço total da compra -> Float
  "products": produtos comprados -> Products
  "salesman": Funcionário que vendeu -> Employees
  "sold_at": Data da compra -> DateTime
```
