from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Cursos
@app.post("/cursos/", response_model=schemas.CursoResponse)
def create_curso(curso: schemas.CursoCreate, db: Session = Depends(get_db)):
    return crud.create_curso(db, curso)

@app.get("/cursos/", response_model=list[schemas.CursoResponse])
def read_cursos(db: Session = Depends(get_db)):
    return crud.get_cursos(db)

@app.get("/cursos/{curso_id}", response_model=schemas.CursoResponse)
def read_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = crud.get_curso(db, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return curso

@app.delete("/cursos/{curso_id}")
def delete_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = crud.delete_curso(db, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return {"detail": "Curso deletado"}

# Alunos
@app.post("/alunos/", response_model=schemas.AlunoResponse)
def create_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    return crud.create_aluno(db, aluno)

@app.get("/alunos/", response_model=list[schemas.AlunoResponse])
def read_alunos(db: Session = Depends(get_db)):
    return crud.get_alunos(db)

@app.get("/alunos/{aluno_id}", response_model=schemas.AlunoResponse)
def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = crud.get_aluno(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@app.put("/alunos/{aluno_id}", response_model=schemas.AlunoResponse)
def update_aluno(aluno_id: int, aluno: schemas.AlunoUpdate, db: Session = Depends(get_db)):
    updated_aluno = crud.update_aluno(db, aluno_id, aluno)
    if not updated_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return updated_aluno

@app.delete("/alunos/{aluno_id}")
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = crud.delete_aluno(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"detail": "Aluno deletado"}
