from flask import Flask

import pytest
from unittest.mock import patch, MagicMock
from api import app, connect_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("api.connect_db") 

def test_get_todos_imoveis(mock_connect_db, client):

    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configuramos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        (1, 'Vanessa', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488423.52, '2017-07-29'),
        (2, 'Luisa', 'Travessa', 'Colonton', 'North Garyville', '93354', 'casa em condominio', 260069.89, '2021-11-30'),
    ]


    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis")

    assert response.status_code == 200

    expected_response = {
        "imoveis": [
            {"id": 1, "logradouro": "Vanessa", "tipo_logradouro": 'Travessa', 'bairro':'Lake Danielle', 'cidade':'Judymouth','cep':
             '85184','tipo':'casa em condominio',' valor':488423.52, 'data_aquisicao':'2017-07-29'},
            {"id": 2, "logradouro": "Luisa", "tipo_logradouro": 'Travessa', 'bairro':'Colonton', 'cidade':'North Garyville','cep':
             '93354','tipo':'casa em condominio',' valor':260069.89, 'data_aquisicao':'2021-11-30'},
        ]
    }
    assert response.get_json() == expected_response

def teste_get_todos_imoveis_vazio(mock_connect_db, client):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    mock_connect_db.return_value = mock_conn
    response = client.get("/imoveis")
    assert response.status_code == 404

