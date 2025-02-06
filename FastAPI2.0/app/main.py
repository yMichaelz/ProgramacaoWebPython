from fastapi import FastAPI, Depends, HTTPException, Request, Form, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from . import models, schemas, crud
from .database import engine, Base, get_db
import shutil
from jose import JWTError, jwt  # Para validar o JWT, se necessário
import os
from fastapi.responses import RedirectResponse
from . import auth
from .auth import verificar_token  # Importar a função de verificação do token
from .models import Usuario
from .schemas import Login


Base.metadata.create_all(bind=engine)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

# Configurar Jinja2 para renderizar templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "Home"})



@app.get("/cursos/html")
def cursos_html(request: Request, token: str = Depends(auth.verificar_token), db: Session = Depends(get_db)):
    cursos = crud.get_cursos(db)
    return templates.TemplateResponse("cursos.html", {"request": request, "cursos": cursos, "title": "Lista de Cursos"})

@app.get("/alunos/html")
def alunos_html(request: Request, token: str = Depends(auth.verificar_token), db: Session = Depends(get_db)):
    if not token:
        return templates.TemplateResponse("login.html", {"request": request})

    alunos = crud.get_alunos(db)
    return templates.TemplateResponse("alunos.html", {"request": request, "alunos": alunos, "title": "Lista de Alunos"})

#Cadastro de Usuário
# Rota GET para exibir o formulário de cadastro
@app.get("/register")
def show_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "title": "Cadastro de Usuário"})

# Rota POST para processar o formulário de cadastro
@app.post("/register")
def register_usuario(email: str = Form(...), senha: str = Form(...), db: Session = Depends(get_db)):
    # Lógica para verificar se o usuário já existe, se a senha é válida, etc.
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    # Criar e salvar o novo usuário no banco de dados
    senha_hash = auth.gerar_hash_senha(senha)
    novo_usuario = models.Usuario(email=email, senha_hash=senha_hash)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return RedirectResponse(url="/login", status_code=303)  # Redireciona para a página de login após o cadastro

# Login com JWT
@app.post("/login")
async def login(request: Request):
    data = await request.json()  # Captura os dados brutos recebidos
    print("Dados recebidos no backend:", data)  # Depuração
    return {"debug": data}  # Retorna o que foi recebido


@app.post("/upload-foto/")
def upload_foto(foto: UploadFile = File(...), token: str = Depends(auth.verificar_token), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Não autorizado")

    usuario = db.query(models.Usuario).filter(models.Usuario.email == token).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    caminho_foto = f"{UPLOAD_DIR}/{usuario.id}_{foto.filename}"
    with open(caminho_foto, "wb") as buffer:
        shutil.copyfileobj(foto.file, buffer)

    usuario.foto_perfil = caminho_foto
    db.commit()
    return {"mensagem": "Foto enviada com sucesso"}

@app.get("/perfil")
def perfil(request: Request, token: str = Depends(auth.verificar_token), db: Session = Depends(get_db)):
    email = token  # O email já foi extraído na verificação do token
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    cursos = db.query(models.Curso).all()
    return templates.TemplateResponse("perfil.html", {"request": request, "usuario": usuario, "cursos": cursos})


# Criar um curso
@app.post("/cursos/")
def create_curso(nome: str = Form(...), descricao: str = Form(None), db: Session = Depends(get_db)):
    novo_curso = models.Curso(nome=nome, descricao=descricao)
    db.add(novo_curso)
    db.commit()
    db.refresh(novo_curso)
    return RedirectResponse(url="/perfil", status_code=303)

# Atualizar curso
@app.post("/cursos/{curso_id}")
def update_curso(curso_id: int, nome: str = Form(None), descricao: str = Form(None), db: Session = Depends(get_db)):
    curso = db.query(models.Curso).filter(models.Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    if nome:
        curso.nome = nome
    if descricao:
        curso.descricao = descricao

    db.commit()
    return RedirectResponse(url="/perfil", status_code=303)

# Remover curso
@app.post("/cursos/{curso_id}/delete")
def delete_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(models.Curso).filter(models.Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    db.delete(curso)
    db.commit()
    return RedirectResponse(url="/perfil", status_code=303)

@app.get("/register")
def show_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "title": "Cadastro de Usuário"})

@app.get("/login")
def show_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "Login"})
