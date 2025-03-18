import pytest
from unittest.mock import MagicMock, patch
from flask import Flask, jsonify

# Cria uma instância do Flask para testes (tipo um "fake" do Flask)
@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True  # Ativa o modo de teste, pra não dar ruim
    with app.test_client() as client:
        yield client  # Entrega o cliente de teste pra gente usar

# Mock do modelo Imovel (um "fingimento" de imóvel pra testar sem banco de dados)
class MockImovel:
    def _init_(self, id, logradouro, cidade, tipo, valor):
        self.id = id
        self.logradouro = logradouro
        self.cidade = cidade
        self.tipo = tipo
        self.valor = valor

    def to_dict(self):
        # Transforma o imóvel num dicionário (pra ficar bonito no JSON)
        return {
            "id": self.id,
            "logradouro": self.logradouro,
            "cidade": self.cidade,
            "tipo": self.tipo,
            "valor": self.valor
        }

# Teste para listar imóveis (vamos ver se tá tudo certo com a listagem)
def test_listar_imoveis(client):
    # Mock da resposta do banco de dados (fingindo que tem uns imóveis lá)
    mock_imoveis = [
        MockImovel(1, "Rua A", "São Paulo", "Casa", 500000.0),
        MockImovel(2, "Rua B", "Rio de Janeiro", "Apartamento", 700000.0)
    ]

    # Mock do método query.all() pra retornar a lista de imóveis (faz de conta que o banco tá funcionando)
    with patch('app.Imovel.query') as mock_query:
        mock_query.all.return_value = mock_imoveis

        # Simula a rota /imoveis (faz um GET pra ver se tá tudo certo)
        response = client.get('/imoveis')
        assert response.status_code == 200  # Espera que o status seja 200 (tudo certo)

        # Verifica se a resposta contém os imóveis mockados (se tá vindo o que a gente espera)
        data = response.get_json()
        assert len(data) == 2  # Tem que ter 2 imóveis na lista
        assert data[0]['logradouro'] == "Rua A"  # O primeiro imóvel tem que ser da Rua A
        assert data[1]['cidade'] == "Rio de Janeiro"  # O segundo tem que ser do Rio

# Teste para obter um imóvel por ID (vamos ver se pega o imóvel certo)
def test_obter_imovel(client):
    # Mock de um imóvel específico (fingindo que tem um imóvel com ID 1)
    mock_imovel = MockImovel(1, "Rua A", "São Paulo", "Casa", 500000.0)

    # Mock do método query.get_or_404 pra retornar o imóvel mockado (faz de conta que o banco tá funcionando)
    with patch('app.Imovel.query') as mock_query:
        mock_query.get_or_404.return_value = mock_imovel

        # Simula a rota /imoveis/1 (faz um GET pra pegar o imóvel com ID 1)
        response = client.get('/imoveis/1')
        assert response.status_code == 200  # Espera que o status seja 200 (tudo certo)

        # Verifica se a resposta contém o imóvel mockado (se tá vindo o que a gente espera)
        data = response.get_json()
        assert data['id'] == 1  # O ID tem que ser 1
        assert data['logradouro'] == "Rua A"  # O logradouro tem que ser "Rua A"
        assert data['tipo'] == "Casa"  # O tipo tem que ser "Casa"

# Teste para adicionar um novo imóvel (vamos ver se tá salvando direitinho)
def test_adicionar_imovel(client):
    # Mock dos dados do novo imóvel (um imóvel novo pra testar)
    novo_imovel = {
        "logradouro": "Rua Nova",
        "cidade": "Belo Horizonte",
        "tipo": "Apartamento",
        "valor": 600000.0
    }

    # Mock do método db.session.add e db.session.commit (faz de conta que tá salvando no banco)
    with patch('app.db.session.add'), patch('app.db.session.commit'):
        # Simula a rota POST /imoveis (faz um POST pra adicionar o imóvel)
        response = client.post('/imoveis', json=novo_imovel)
        assert response.status_code == 201  # Espera que o status seja 201 (criado com sucesso)

        # Verifica se a resposta contém os dados do novo imóvel (se tá vindo o que a gente mandou)
        data = response.get_json()
        assert data['logradouro'] == "Rua Nova"  # O logradouro tem que ser "Rua Nova"
        assert data['cidade'] == "Belo Horizonte"  # A cidade tem que ser "Belo Horizonte"

# Teste para atualizar um imóvel (vamos ver se tá atualizando direitinho)
def test_atualizar_imovel(client):
    # Mock de um imóvel existente (fingindo que tem um imóvel com ID 1)
    mock_imovel = MockImovel(1, "Rua Antiga", "São Paulo", "Casa", 500000.0)

    # Mock do método query.get_or_404 pra retornar o imóvel mockado (faz de conta que o banco tá funcionando)
    with patch('app.Imovel.query') as mock_query:
        mock_query.get_or_404.return_value = mock_imovel

        # Mock do método db.session.commit (faz de conta que tá salvando no banco)
        with patch('app.db.session.commit'):
            # Dados atualizados do imóvel (vamos mudar o logradouro e o valor)
            dados_atualizados = {
                "logradouro": "Rua Nova",
                "valor": 600000.0
            }

            # Simula a rota PUT /imoveis/1 (faz um PUT pra atualizar o imóvel)
            response = client.put('/imoveis/1', json=dados_atualizados)
            assert response.status_code == 200  # Espera que o status seja 200 (tudo certo)

            # Verifica se a resposta contém os dados atualizados (se tá vindo o que a gente mandou)
            data = response.get_json()
            assert data['logradouro'] == "Rua Nova"  # O logradouro tem que ser "Rua Nova"
            assert data['valor'] == 600000.0  # O valor tem que ser 600000.0

# Teste para remover um imóvel (vamos ver se tá deletando direitinho)
def test_remover_imovel(client):
    # Mock de um imóvel existente (fingindo que tem um imóvel com ID 1)
    mock_imovel = MockImovel(1, "Rua A", "São Paulo", "Casa", 500000.0)

    # Mock do método query.get_or_404 pra retornar o imóvel mockado (faz de conta que o banco tá funcionando)
    with patch('app.Imovel.query') as mock_query:
        mock_query.get_or_404.return_value = mock_imovel

        # Mock do método db.session.delete e db.session.commit (faz de conta que tá deletando no banco)
        with patch('app.db.session.delete'), patch('app.db.session.commit'):
            # Simula a rota DELETE /imoveis/1 (faz um DELETE pra remover o imóvel)
            response = client.delete('/imoveis/1')
            assert response.status_code == 204  # Espera que o status seja 204 (deletado com sucesso)

            # Verifica se o imóvel foi removido (faz um GET pra ver se o imóvel ainda existe)
            response = client.get('/imoveis/1')
            assert response.status_code == 404  # Espera que o status seja 404 (não encontrado)