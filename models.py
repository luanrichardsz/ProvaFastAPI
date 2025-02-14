from sqlalchemy import create_engine, String, Column, Integer, ForeignKey #Importando para a criação do banco de dados
from sqlalchemy.orm import declarative_base, relationship
from database import Base

# Criando a base para os modelos ORM
#ORM = Representações de tabelas do banco de dados como classes Python.
Base = declarative_base()

#Criar dois schemas Pydantic para entrada e saida de dados
#Modelo SQLAlchemy para Empresa (representação no banco)
class Empresa(Base):
    #Declarando nome da tabela
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String,unique=True, nullable=False)
    endereco = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=False)

    #Relacionamento: uma empresa pode ter varias obrigações
    obrigacoes = relationship("ObrigacaoNecessaria", back_populates="empresa") #back_populates garante que ao acessar um relacionamento de um lado, o SQLAlchemy consiga automaticamente navegar para o outro lado

#Modelo SQLAlchemy para Obrigação Necessária
class ObrigacaoNecessaria(Base):
    __tablename__ = "obrigacao_necessarias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    periodicidade = Column(String, nullable=False) #(mensal, trimestral, anual)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False) #chave estrangeira da tabela empresa

    empresa = relationship("Empresa", back_populates="obrigacoes") #Relacionamento para obrigacoes herdar de empresas

#