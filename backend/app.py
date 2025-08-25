from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
from models import Aluno, Turma
from pydantic import BaseModel, EmailStr, constr
from datetime import date

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AlunoCreate(BaseModel):
    nome: constr(min_length=3, max_length=80)
    data_nascimento: date
    email: EmailStr | None = None
    status: constr(regex="^(ativo|inativo)$")
    turma_id: int | None = None

class TurmaCreate(BaseModel):
    nome: str
    capacidade: int

@app.get("/alunos", response_model=list[AlunoCreate])
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).all()

@app.post("/alunos", status_code=status.HTTP_201_CREATED)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    if db.query(Aluno).filter(Aluno.nome == aluno.nome).first():
        raise HTTPException(status_code=400, detail="Nome de aluno já existe.")
    novo = Aluno(**aluno.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@app.get("/turmas", response_model=list[TurmaCreate])
def listar_turmas(db: Session = Depends(get_db)):
    return db.query(Turma).all()

@app.post("/turmas", status_code=status.HTTP_201_CREATED)
def criar_turma(turma: TurmaCreate, db: Session = Depends(get_db)):
    if db.query(Turma).filter(Turma.nome == turma.nome).first():
        raise HTTPException(status_code=400, detail="Nome de turma já existe.")
    novo = Turma(**turma.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo
