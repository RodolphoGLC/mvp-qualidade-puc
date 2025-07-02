import pytest
import json
from app import app
from model import Session, Vinho


@pytest.fixture
def client():
    """Configura o cliente de teste para a aplicação Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_wine_data():
    """Exemplo de dados para teste de vinho"""
    return {
        "fixed_acidity": 12,
        "volatile_acidity": 1.2,
        "citric_acid": 0.04,
        "residual_sugar": 10.5,
        "chlorides": 0.21,
        "free_sulfur_dioxide": 2.0,
        "total_sulfur_dioxide": 30.0,
        "density": 1.0,
        "pH": 3.01,
        "sulphates": 1.0,
        "alcohol": 10.9
    }


def test_home_redirect(client):
    """Testa se a rota home redireciona para o frontend"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/front/index.html' in response.location


def test_docs_redirect(client):
    """Testa se a rota /docs redireciona para /openapi"""
    response = client.get('/docs')
    assert response.status_code == 302
    assert '/openapi' in response.location


def test_get_vinhos_empty(client):
    """Testa a listagem de vinhos quando não há nenhum"""
    # Garantir que o banco está limpo antes
    cleanup_test_wines()

    response = client.get('/vinhos')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'vinhos' in data
    assert isinstance(data['vinhos'], list)
    assert len(data['vinhos']) == 0


def test_add_wine(client, sample_wine_data):
    response = client.post('/vinho', json=sample_wine_data)

    if response.status_code != 200:
        print("Status:", response.status_code)
        print("Vinho", sample_wine_data)
        print("Resposta do servidor:", response.data.decode())

    assert response.status_code == 200
    data = json.loads(response.data)

    for key in sample_wine_data:
        if isinstance(sample_wine_data[key], float):
            assert round(data[key], 2) == round(sample_wine_data[key], 2)
        else:
            assert data[key] == sample_wine_data[key]

    assert 'id' in data
    assert 'quality' in data


def test_get_nonexistent_wine(client):
    """Testa a busca de um vinho não existente"""
    response = client.get('/vinho?id=999999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data


def test_delete_wine(client, sample_wine_data):
    """Testa a remoção de um vinho"""

    # Primeiro limpa para garantir estado limpo
    cleanup_test_wines()

    # Adiciona o vinho com json=...
    post_resp = client.post('/vinho', json=sample_wine_data)

    # DEBUG: Veja o que foi retornado
    print("Status Code:", post_resp.status_code)
    print("Response JSON:", post_resp.get_json())

    # Extrai o JSON da resposta
    data = post_resp.get_json()
    assert isinstance(data, dict), f"Esperado dicionário, obtido: {type(data)}"

    vinho_id = data.get('id')
    assert vinho_id is not None

    delete_resp = client.delete(f'/vinho?id={vinho_id}')
    assert delete_resp.status_code == 200
    delete_data = delete_resp.get_json()
    assert 'message' in delete_data
    assert 'removido com sucesso' in delete_data['message']


def test_delete_nonexistent_wine(client):
    """Testa a remoção de um vinho não existente"""
    response = client.delete('/vinho?id=9999994324234')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data


def test_wine_quality_edge_cases(client):
    """Testa casos extremos para previsão de qualidade do vinho"""
    # Caso de valores mínimos (novos mínimos baseados no getRandom)
    min_data = {
        "fixed_acidity": 4.6,
        "volatile_acidity": 0.12,
        "citric_acid": 0.0,
        "residual_sugar": 0.9,
        "chlorides": 0.012,
        "free_sulfur_dioxide": 1.0,
        "total_sulfur_dioxide": 6.0,
        "density": 0.98711,
        "pH": 2.74,
        "sulphates": 0.33,
        "alcohol": 8.0
    }
    resp = client.post(
        '/vinho',
        json=min_data,
        content_type='application/json'
    )
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert 'quality' in data

    # Caso de valores máximos (novos máximos baseados no getRandom)
    max_data = {
        "fixed_acidity": 15.9,
        "volatile_acidity": 1.58,
        "citric_acid": 1.0,
        "residual_sugar": 15.5,
        "chlorides": 0.611,
        "free_sulfur_dioxide": 72.0,
        "total_sulfur_dioxide": 289.0,
        "density": 1.03898,
        "pH": 4.01,
        "sulphates": 2.0,
        "alcohol": 14.9
    }
    resp = client.post(
        '/vinho',
        json=max_data,
        content_type='application/json'
    )
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert 'quality' in data


def cleanup_test_wines():
    """Limpa os vinhos de teste do banco"""
    session = Session()
    test_wines = session.query(Vinho).all()
    for wine in test_wines:
        session.delete(wine)
    session.commit()
    session.close()


@pytest.fixture(autouse=True)
def run_around_tests():
    """Limpa o banco antes e depois de cada teste para evitar poluição"""
    cleanup_test_wines()
    yield
    cleanup_test_wines()
