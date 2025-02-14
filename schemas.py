from pydantic import BaseModel
from enum import Enum

#Schemas Pydantic para a entrada e saida de dados
# validação de valores possíveis para periodicidade
class PeriodicidadeEnum(str, Enum):
    mensal = "mensal"
    trimestral = "trimestral"
    anual = "anual"

##Schema de Entrada (Nao inclui ID, pois ele é gerado no banco)
class EmpresaCreate(BaseModel):
    nome: str
    cnpj: str #tem que ser unico
    endereco: str
    email: str
    telefone: str

    class Config:
        from_attributes = True #Permite converter SQALchemy para Pydantic

class ObrigacaoNecessariaCreate(BaseModel):
    nome: str
    periodicidade: str #validação para (mensal, trimestral, anual)
    empresa_id: int #FK para Empresa

    class Config:
        from_attributes = True #Permite converter SQALchemy para Pydantic

class EmpresaOut(EmpresaCreate):
    id: int #Adicionando ID gerado pelo banco

class ObrigacaoNecessariaOut(ObrigacaoNecessariaCreate):
    id: int