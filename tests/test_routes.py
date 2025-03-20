import json
import pytest
from app.models import Imovel
from app import db

@pytest.mark.parametrize("query_param, expected_count", [
    ('', 2),
    ('?tipo=casa', 1),
    ('?tipo=apartamento', 1),
    ('?cidade=Cidade A', 1),
    ('?cidade=Cidade B', 1),
])
def test_listar_imoveis(test_client, init_database, query_param, expected_count):
    response = test_client.get(f'/imoveis{query_param}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == expected_count

@pytest.mark.parametrize("imovel_id, expected_status, expected_key", [
    (1, 200, 'id'),
    (999, 404, 'erro'),
])
def test_buscar_imovel(test_client, init_database, imovel_id, expected_status, expected_key):
    response = test_client.get(f'/imoveis/{imovel_id}')
    assert response.status_code == expected_status
    data = json.loads(response.data)
    assert expected_key in data

def test_adicionar_imovel(test_client, init_database, cleanup_database):
    new_imovel = {
        'logradouro': 'Rua Nova',
        'cidade': 'Nova Cidade',
        'tipo': 'apartamento',
        'valor': 250000.0
    }
    response = test_client.post('/imoveis', 
                                data=json.dumps(new_imovel),
                                content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['logradouro'] == 'Rua Nova'

@pytest.mark.parametrize("imovel_id, update_data, expected_status", [
    (1, {'valor': 150000.0}, 200),
    (999, {'valor': 150000.0}, 404),
])
def test_atualizar_imovel(test_client, init_database, imovel_id, update_data, expected_status):
    response = test_client.put(f'/imoveis/{imovel_id}', 
                               data=json.dumps(update_data),
                               content_type='application/json')
    assert response.status_code == expected_status
    if expected_status == 200:
        data = json.loads(response.data)
        assert data['valor'] == update_data['valor']

@pytest.mark.parametrize("imovel_id, expected_status", [
    (1, 200),
    (999, 404),
])
def test_remover_imovel(test_client, init_database, cleanup_database, imovel_id, expected_status):
    response = test_client.delete(f'/imoveis/{imovel_id}')
    assert response.status_code == expected_status
    if expected_status == 200:
        assert db.session.get(Imovel, imovel_id) is None

@pytest.mark.parametrize("route, query_param, expected_count", [
    ('/imoveis/tipo', '?tipo=casa', 1),
    ('/imoveis/tipo', '?tipo=apartamento', 1),
    ('/imoveis/cidade', '?cidade=Cidade A', 1),
    ('/imoveis/cidade', '?cidade=Cidade B', 1),
])
def test_listar_por_tipo_e_cidade(test_client, init_database, route, query_param, expected_count):
    response = test_client.get(f'{route}{query_param}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == expected_count