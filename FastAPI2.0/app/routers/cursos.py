from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Curso, Aluno
from app.schemas import CursoCreate, CursoOut

router = APIRouter()

@router.post("/", response_model=CursoOut)
def create_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    new_curso = Curso(**curso.dict())
    db.add(new_curso)
    db.commit()
    db.refresh(new_curso)
    return new_curso

@router.get("/{curso_id}", response_model=CursoOut)
def get_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return curso

@router.get("/", response_model=list[CursoOut])
def list_cursos(db: Session = Depends(get_db)):
    return db.query(Curso).all()
