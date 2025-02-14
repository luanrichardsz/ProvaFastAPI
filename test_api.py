from fastapi.testclient import TestClient
from ProvaFastAPI import app
import pytest
from database import Base, engine, get_db
from sqlalchemy.orm import sessionmaker

# Criar uma sessão de testes
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Criar as tabelas antes de rodar os testes
    Base.metadata.create_all(bind=engine)

    # Criar uma nova sessão para os testes
    session = TestingSessionLocal()
    yield session

    # Fechar a sessão após o teste
    session.close()

client = TestClient(app)

# Teste: Criar Empresa
def test_criar_empresa():
    response = client.post("/empresas/", json={
        "nome": "Empresa Teste",
        "cnpj": "12345678000100",
        "endereco": "Rua Teste, 123",
        "email": "empresa@teste.com",
        "telefone": "11999999999"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa Teste"

# Teste: Listar Empresas
def test_listar_empresas():
    response = client.get("/empresas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Teste: Criar Obrigação Acessória
def test_criar_obrigacao():
    # Criar uma empresa antes para vincular a obrigação
    empresa_response = client.post("/empresas/", json={
        "nome": "Empresa para Obrigação",
        "cnpj": "98765432000100",
        "endereco": "Avenida Principal, 456",
        "email": "empresa@teste.com",
        "telefone": "11999999998"
    })
    empresa_id = empresa_response.json()["id"]

    response = client.post("/obrigacoes/", json={
        "nome": "Obrigação Teste",
        "periodicidade": "mensal",
        "empresa_id": empresa_id
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Obrigação Teste"

# Teste: Listar Obrigações Acessórias
def test_listar_obrigacoes():
    response = client.get("/obrigacoes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

#
