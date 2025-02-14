from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Empresa, ObrigacaoNecessaria
from schemas import EmpresaCreate, EmpresaOut, ObrigacaoNecessariaCreate, ObrigacaoNecessariaOut
from database import get_db
from typing import List
from fastapi import Body

router = APIRouter()

# Criar Empresa (POST)
@router.post("/empresas/", response_model=EmpresaOut)
def criar_empresa(empresa: EmpresaCreate = Body(...), db: Session = Depends(get_db)):
    nova_empresa = Empresa(**empresa.model_dump())
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)
    return nova_empresa

#Listar Empresas (GET)
@router.get("/empresas/", response_model=List[EmpresaOut])
def listar_empresas(db: Session = Depends(get_db)):
    return db.query(Empresa).all()

#Criar Obrigação (Post)
@router.post("/obrigacoes/", response_model=ObrigacaoNecessariaOut)
def criar_obrigacao(obrigacao: ObrigacaoNecessariaCreate, db: Session = Depends(get_db)):
    # Verifica se a empresa existe antes de criar a obrigação
    empresa = db.query(Empresa).filter(Empresa.id == obrigacao.empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=400, detail="Empresa não encontrada")

    nova_obrigacao = ObrigacaoNecessaria(**obrigacao.model_dump())
    db.add(nova_obrigacao)
    db.commit()  # ✅ Adicionado commit para salvar no banco
    db.refresh(nova_obrigacao)
    return nova_obrigacao


# Listar Obrigações (Get)
@router.get("/obrigacoes/", response_model=List[ObrigacaoNecessariaOut])
def listar_obrigacoes(db: Session = Depends(get_db)):
    try:
        return db.query(ObrigacaoNecessaria).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar obrigações: {str(e)}")