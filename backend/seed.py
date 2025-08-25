from database import SessionLocal, engine, Base
from models import Aluno, Turma
from datetime import date

Base.metadata.create_all(bind=engine)
db = SessionLocal()

turmas = [
    Turma(nome="1º Ano A", capacidade=30),
    Turma(nome="2º Ano B", capacidade=25),
    Turma(nome="3º Ano C", capacidade=20)
]
db.add_all(turmas)
db.commit()

alunos = [
    Aluno(nome=f"Aluno {i}", data_nascimento=date(2010+i%10, 1, 10), email=f"aluno{i}@escola.com", status="ativo", turma_id=turmas[i%3].id)
    for i in range(1, 21)
]
db.add_all(alunos)
db.commit()
db.close()
