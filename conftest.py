import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from fastapi.testclient import TestClient
from ProvaFastAPI import app

# Criar um banco de dados em memória para testes
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar as tabelas no banco de testes
Base.metadata.create_all(bind=engine)

# Criar uma sessão de teste
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Substituir a dependência do banco na API para usar o banco de testes
app.dependency_overrides[get_db] = override_get_db

# Criar um cliente de teste
client = TestClient(app)

# Criar um fixture para usar nos testes
@pytest.fixture
def test_client():
    return client
#