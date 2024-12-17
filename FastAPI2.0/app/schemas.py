from pydantic import BaseModel

# Schemas para Cursos
class CursoBase(BaseModel):
    nome: str
    descricao: str | None = None

class CursoCreate(CursoBase):
    pass

class CursoResponse(CursoBase):
    id: int

    class Config:
        orm_mode = True

# Schemas para Alunos
class AlunoBase(BaseModel):
    nome: str
    idade: int
    curso_id: int | None = None

class AlunoCreate(AlunoBase):
    pass

class AlunoUpdate(BaseModel):
    nome: str | None = None
    idade: int | None = None
    curso_id: int | None = None

class AlunoResponse(AlunoBase):
    id: int
    curso: CursoResponse | None = None

    class Config:
        orm_mode = True
