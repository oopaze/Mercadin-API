import random, pytest

sectors_slug = []

@pytest.mark.run(order=5)
def test_show_sector(client):
    """
        Testing if /sectors/ page is providing all sector Data
    """
    response = client.get('/sectors/')

    assert response.status_code == 200

@pytest.mark.run(order=6)
def test_insert_sector(client):
    """
        Testing if the insert route is function
        Sending a JSON like:
            {'name': 'sector-name'}
    """
    json = {'data':{'name': 'test1'}}
    response = client.post('/sectors/', json=json)

    sectors_slug.append(response.json['data']['slug'])

    assert response.status_code == 201

@pytest.mark.run(order=7)
def test_insert_already_exist(client):
    """
        Testing error in insert route: insert already exist
        Sending a JSON with data that already exists on DB
    """
    json = {'data':{'name': 'test1'}}
    response = client.post('/sectors/', json=json)

    assert response.status_code == 409

@pytest.mark.run(order=8)
def test_insert_has_wrong_data(client):
    """
        Testing insert error: Receiving wrong data params
        Sending a JSON that contains wrong params
    """
    json = {'data':{'type': 'test1'}}
    response = client.post('/sectors/', json=json)

    assert response.status_code == 406

@pytest.mark.run(order=9)
def test_update_sector(client):
    """
        Testing update a sector by ID
        Sending a JSON like:
            {'name':'newname'}
        To:
            /sectors/{item_id}
    """
    json = {'data':{'name': 'test2'}}
    response = client.put(f'/sectors/{sectors_slug[0]}', json=json)
    sectors_slug[0] = response.json['data']['slug']

    assert response.status_code == 200

@pytest.mark.run(order=10)
def test_update_unexistent_sector(client):
    """
        Testing update Error: update an unexistent sector
        SENDING a JSON like:
            {'name':'newname'}
        To:
            /sectors/{an existent id}
    """
    unexistent_slug = 'aushaushaushahsahush'
    json = {'data':{'name': 'test2'}}

    response = client.put(f'/sectors/{unexistent_slug}', json=json)

    assert response.status_code == 404

@pytest.mark.run(order=11)
def test_update_values_conflicts(client):
    """
        Testing update Error: update value conflicts with other item's value
        Sending a JSON like:
            {'name': 'an existent name'}
    """
    json = {'data':{'name': 'test1'}}

    response = client.post('/sectors/', json=json)
    sectors_slug.append(response.json['data']['slug'])

    response = client.put(f'/sectors/{sectors_slug[0]}', json=json)

    assert response.status_code == 409

@pytest.mark.run(order=12)
def test_delete_sector(client):
    """
        Testing delete a sector by ID
        Deleting both sector created on tests
    """

    response = client.delete(f'/sectors/{sectors_slug[0]}')
    response = client.delete(f'/sectors/{sectors_slug[1]}')

    response.status_code == 200

@pytest.mark.run(order=13)
def test_delete_unexistent_sector(client):
    """
        Testing delete error: Delete an unexistent sector
    """
    response = client.delete(f'/sectors/{sectors_slug[0]}')

    response.status_code == 404
