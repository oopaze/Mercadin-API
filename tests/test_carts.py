import pytest

carts_id = []
products_id = []

@pytest.mark.run(order=24)
def test_show_all_carts(client):
    response = client.get('/carts/')

    assert response.status_code == 200

@pytest.mark.run(order=25)
def test_insert_cart(client):
    response = client.post('/carts/')
    carts_id.append(response.json['data']['id'])

    assert response.status_code == 201

@pytest.mark.run(order=26)
def test_show_one_carts(client):
    response = client.get(f'/carts/{carts_id[0]}')

    assert response.status_code == 200

@pytest.mark.run(order=27)
def test_show_unexistent_cart(client):
    unexistent_id = -1

    response = client.get(f'/carts/{unexistent_id}')
    assert response.status_code == 404

@pytest.mark.run(order=28)
def test_add_product_to_cart(client):
    client.post('/sectors/', json={"data":{'name':'test3'}})

    testprod = {'data':{'name':'test', 'price':0,
                'weight':1, 'amount':20, 'sector':'test3'}}

    response = client.post('/products/', json=testprod)

    products_id.append(response.json['data']['id'])

    json ={'data':
            {
                'product_id':products_id[0],
                'product_amount':1
            }
          }

    response = client.post(f'/carts/{carts_id[0]}', json=json)

    assert response.status_code == 201

@pytest.mark.run(order=29)
def test_add_unexisting_producting_in_a_cart(client):
    json ={'data':
            {
                'product_id':-1,
                'product_amount':1
            }
          }
    response = client.post(f'/carts/{carts_id[0]}', json=json)

    assert response.status_code == 404

@pytest.mark.run(order=30)
def test_add_producting_in_a_unexisting_card(client):
    response = client.post(f'/carts/{-1}', json={'data':{'product_id':products_id[0]}})

    assert response.status_code == 404

@pytest.mark.run(order=31)
def test_delete_product_of_cart(client):
    response = client.delete(f'/carts/{carts_id[0]}/{products_id[0]}')

    assert response.status_code == 200

@pytest.mark.run(order=32)
def test_delete_unexisting_product_of_cart(client):
    response = client.delete(f'/carts/{carts_id[0]}/{-1}')

    assert response.status_code == 404

@pytest.mark.run(order=33)
def test_delete_product_of_unexisting_cart(client):
    response = client.delete(f'/carts/{-1}/{products_id[0]}')

    assert response.status_code == 404

@pytest.mark.run(order=34)
def test_delete_cart(client):
    client.delete(f'/products/{products_id[0]}')
    client.delete('/sectors/test3')

    response = client.delete(f'/carts/{carts_id[0]}')

    assert response.status_code == 200

@pytest.mark.run(order=35)
def test_delete_unexisting_cart(client):
    response = client.delete(f'/carts/{-1}')

    assert response.status_code == 404
