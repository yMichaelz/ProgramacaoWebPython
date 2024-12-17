from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Aluno, Curso
from app.schemas import AlunoCreate, AlunoOut

router = APIRouter()

@router.post("/", response_model=AlunoOut)
def create_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    new_aluno = Aluno(**aluno.dict())
    db.add(new_aluno)
    db.commit()
    db.refresh(new_aluno)
    return new_aluno

@router.get("/{aluno_id}", response_model=AlunoOut)
def get_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.get("/", response_model=list[AlunoOut])
def list_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).all()
