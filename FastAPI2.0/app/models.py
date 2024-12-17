from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String, nullable=True)

    # Relacionamento com alunos
    alunos = relationship("Aluno", back_populates="curso")


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
    curso_id = Column(Integer, ForeignKey("cursos.id"))

    # Relacionamento com o curso
    curso = relationship("Curso", back_populates="alunos")
