import pytest

products_id = []

@pytest.mark.run(order=14)
def test_show_products(client):
    response = client.get('/products/')

    assert response.status_code == 200

@pytest.mark.run(order=15)
def test_insert_product(client):
    client.post('/sectors/', json={'name':'test3'})
    testprod = {'name':'test', 'price':0,
                'weight':1, 'amount':20, 'sector':'test3'}

    response = client.post('/products/', json=testprod)

    products_id.append(response.json['Data']['id'])

    assert response.status_code == 201

@pytest.mark.run(order=16)
def test_insert_with_wrong_data(client):
    testprod = {'nome':'test', 'price':0,
                'weight':1, 'amount':20,
                'sector':'test3'}

    response = client.post('/products/', json=testprod)

    assert response.status_code == 406

@pytest.mark.run(order=17)
def test_update_product(client):
    testprod = {'name':'test', 'price':0,
                'weight':1, 'amount':30,
                'sector':'test3'}

    response = client.put(f'/products/{products_id[0]}', json=testprod)

    assert response.status_code == 200

@pytest.mark.run(order=18)
def test_update_unexistent_product(client):
    testprod = {'name':'test', 'price':0,
                'weight':1, 'amount':30,
                'sector':'test3'}

    unexistent_id = -1
    response = client.put(f'/products/{unexistent_id}', json=testprod)

    assert response.status_code == 404

@pytest.mark.run(order=19)
def test_update_product_with_wrong_data(client):
    testprod = {'nome':'test', 'price':0,
                'weight':1, 'amount':30,
                'sector':'test3'}

    response = client.put(f'/products/{products_id[0]}', json=testprod)

    assert response.status_code == 406

@pytest.mark.run(order=20)
def test_update_sector_of_product(client):

    client.post('/sectors/', json={'name':'test4'})
    response = client.put(f'/products/{products_id[0]}/test4')

    assert response.status_code == 200

@pytest.mark.run(order=21)
def test_update_sector_of_product_with_invalid_param(client):

    response = client.put(f'/products/{products_id[0]}/test6')

    assert response.status_code == 404

@pytest.mark.run(order=22)
def test_delete_product(client):
    client.delete('/sectors/test3')
    client.delete('/sectors/test4')

    response = client.delete(f'/products/{products_id[0]}')

    assert response.status_code == 200

@pytest.mark.run(order=23)
def test_delete_unexistent_product(client):

    response = client.delete(f'/products/{products_id[0]}')

    assert response.status_code == 404
