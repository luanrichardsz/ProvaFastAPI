from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Conexão com o banco de dados postgresql
engine = create_engine("postgresql://postgres:admin@127.0.0.1:5432/postgres")

#Toda a sessão esta conectada com meu banco local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criando a base para os modelos ORM
#ORM = Representações de tabelas do banco de dados como classes Python.
Base = declarative_base()

#Função para obter uma sessão de banco de dados (para ser usada com depends no FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db #Permite que o FastAPI continue executando a requisição
    finally:
        db.close()