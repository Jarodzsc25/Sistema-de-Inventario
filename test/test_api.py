import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_status(client):
    """Prueba que la ruta '/' responde correctamente."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'API del Sistema de Ventas en funcionamiento' in response.data

def test_api_rol_get(client):
    """Prueba GET en la ruta de roles."""
    response = client.get('/api/rol/')  # <- Ajustado con el prefijo correcto
    assert response.status_code == 200  # Ajusta si tu endpoint devuelve otro código

def test_api_rol_post(client):
    """Prueba POST en la ruta de roles."""
    data = {"nombre": "RolPrueba"}
    response = client.post('/api/rol/', json=data)  # <- Ajustado con el prefijo correcto
    assert response.status_code in (200, 201)
