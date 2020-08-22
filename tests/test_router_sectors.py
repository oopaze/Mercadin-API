import random

sectors_id = []

def test_show_sector(client):
    """
        Testing if /sectors/ page is providing all sector Data
    """
    response = client.get('/sectors/')

    assert response.status_code == 200

def test_insert_sector(client):
    """
        Testing if the insert route is function
        Sending a JSON like:
            {'name': 'sector-name'}
    """
    json = {'name': 'test1'}
    response = client.post('/sectors/', json=json)

    sectors_id.append(response.json['Data']['id'])

    assert response.status_code == 201

def test_insert_already_exist(client):
    """
        Testing error in insert route: insert already exist
        Sending a JSON with data that already exists on DB
    """
    json = {'name': 'test1'}
    response = client.post('/sectors/', json=json)

    assert response.status_code == 409

def test_insert_has_wrong_data(client):
    """
        Testing insert error: Receiving wrong data params
        Sending a JSON that contains wrong params
    """
    json = {'type': 'test1'}
    response = client.post('/sectors/', json=json)

    assert response.status_code == 406

def test_update_sector(client):
    """
        Testing update a sector by ID
        Sending a JSON like:
            {'name':'newname'}
        To:
            /sectors/{item_id}
    """
    json = {'name': 'test2'}
    response = client.put(f'/sectors/{sectors_id[0]}', json=json)

    assert response.status_code == 200

def test_update_unexistent_sector(client):
    """
        Testing update Error: update an unexistent sector
        SENDING a JSON like:
            {'name':'newname'}
        To:
            /sectors/{an existent id}
    """
    unexistent_id = 100
    json = {'name': 'test2'}

    response = client.put(f'/sectors/{unexistent_id}', json=json)

    assert response.status_code == 404

def test_update_values_conflicts(client):
    """
        Testing update Error: update value conflicts with other item's value
        Sending a JSON like:
            {'name': 'an existent name'}
    """
    json = {'name': 'test1'}

    response = client.post('/sectors/', json=json)
    sectors_id.append(response.json['Data']['id'])

    response = client.put(f'/sectors/{sectors_id[0]}', json=json)

    assert response.status_code == 409

def test_delete_sector(client):
    """
        Testing delete a sector by ID
        Deleting both sector created on tests
    """

    response = client.delete(f'/sectors/{sectors_id[0]}')
    response = client.delete(f'/sectors/{sectors_id[1]}')

    response.status_code == 200

def test_delete_unexistent_sector(client):
    """
        Testing delete error: Delete an unexistent sector
    """
    response = client.delete(f'/sectors/{sectors_id[0]}')

    response.status_code == 404
