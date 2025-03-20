import pytest
from app import create_app, db
from app.models import Imovel

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope='function')
def init_database(test_client):
    db.create_all()
    imovel1 = Imovel(logradouro='Rua A', cidade='Cidade A', tipo='casa', valor=100000.0)
    imovel2 = Imovel(logradouro='Rua B', cidade='Cidade B', tipo='apartamento', valor=200000.0)
    db.session.add(imovel1)
    db.session.add(imovel2)
    db.session.commit()
    yield
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='function')
def cleanup_database():
    yield
    db.session.query(Imovel).delete()
    db.session.commit()