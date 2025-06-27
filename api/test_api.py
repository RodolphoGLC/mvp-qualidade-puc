import pytest
import json
from app import app
from model import Session, Vinho  # Altere para o nome correto do modelo de vinho

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
        "fixed_acidity": 7.4,
        "volatile_acidity": 0.70,
        "citric_acid": 0.00,
        "residual_sugar": 1.9,
        "chlorides": 0.076,
        "free_sulfur_dioxide": 11.0,
        "total_sulfur_dioxide": 34.0,
        "density": 0.9978,
        "pH": 3.51,
        "sulphates": 0.56,
        "alcohol": 9.4
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
    response = client.get('/vinhos')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'vinhos' in data
    assert isinstance(data['vinhos'], list)

def test_add_wine(client, sample_wine_data):
    """Testa a adição de um vinho"""
    response = client.post(
        '/vinho',
        data=json.dumps(sample_wine_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verifica todos os campos inseridos
    for key in sample_wine_data:
        assert data[key] == sample_wine_data[key]

    # Verifica se a predição de qualidade foi feita
    assert 'quality' in data

def test_get_wine_by_id(client, sample_wine_data):
    """Testa a busca de um vinho por id"""
    # Adiciona o vinho para testar
    post_resp = client.post(
        '/vinho',
        data=json.dumps(sample_wine_data),
        content_type='application/json'
    )
    data = json.loads(post_resp.data)
    vinho_id = data.get('id')
    assert vinho_id is not None

    # Realiza a busca por id
    response = client.get(f'/vinho?id={vinho_id}')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert data['id'] == vinho_id
    for key in sample_wine_data:
        assert data.get(key) == sample_wine_data.get(key)

def test_get_nonexistent_wine(client):
    """Testa a busca de um vinho não existente"""
    response = client.get('/vinho?id=999999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data

def test_delete_wine(client, sample_wine_data):
    """Testa a remoção de um vinho"""
    # Adiciona o vinho para depois deletá-lo
    post_resp = client.post(
        '/vinho',
        data=json.dumps(sample_wine_data),
        content_type='application/json'
    )
    data = json.loads(post_resp.data)
    vinho_id = data.get('id')
    assert vinho_id is not None

    delete_resp = client.delete(f'/vinho?id={vinho_id}')
    assert delete_resp.status_code == 200
    delete_data = json.loads(delete_resp.data)
    assert 'mensagem' in delete_data
    assert 'removido com sucesso' in delete_data['mensagem']

def test_delete_nonexistent_wine(client):
    """Testa a remoção de um vinho não existente"""
    response = client.delete('/vinho?id=999999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'mensagem' in data

def test_wine_quality_edge_cases(client):
    """Testa casos extremos para previsão de qualidade do vinho"""
    # Caso de valores mínimos
    min_data = {
        "fixed_acidity": 4.0,
        "volatile_acidity": 0.1,
        "citric_acid": 0.0,
        "residual_sugar": 0.5,
        "chlorides": 0.01,
        "free_sulfur_dioxide": 1.0,
        "total_sulfur_dioxide": 10.0,
        "density": 0.9900,
        "pH": 2.5,
        "sulphates": 0.3,
        "alcohol": 8.0
    }
    resp = client.post(
        '/vinho',
        data=json.dumps(min_data),
        content_type='application/json'
    )
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert 'quality' in data

    # Caso de valores máximos típicos
    max_data = {
        "fixed_acidity": 15.0,
        "volatile_acidity": 1.5,
        "citric_acid": 1.0,
        "residual_sugar": 15.0,
        "chlorides": 0.5,
        "free_sulfur_dioxide": 72.0,
        "total_sulfur_dioxide": 250.0,
        "density": 1.0040,
        "pH": 4.0,
        "sulphates": 2.0,
        "alcohol": 14.5
    }
    resp = client.post(
        '/vinho',
        data=json.dumps(max_data),
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

def test_cleanup():
    """Limpa dados de teste"""
    cleanup_test_wines()
