from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from . import models, schemas, crud
from .database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar Jinja2 para renderizar templates
templates = Jinja2Templates(directory="templates")

# Página inicial
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})

# Listar cursos no template
@app.get("/cursos/html")
def cursos_html(request: Request, db: Session = Depends(get_db)):
    cursos = crud.get_cursos(db)
    return templates.TemplateResponse("cursos.html", {"request": request, "cursos": cursos, "title": "Lista de Cursos"})

# Listar alunos no template
@app.get("/alunos/html")
def alunos_html(request: Request, db: Session = Depends(get_db)):
    alunos = crud.get_alunos(db)
    return templates.TemplateResponse("alunos.html", {"request": request, "alunos": alunos, "title": "Lista de Alunos"})
