from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from . import schemas, models, crud
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Carregar a chave secreta e o algoritmo do arquivo .env
SECRET_KEY = os.getenv("SECRET_KEY", "chave_secreta")  # A chave secreta deve vir do .env
ALGORITHM = "HS256"

def verificar_senha(senha_digitada: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_digitada, senha_hash)

# Definir o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Função para verificar o token
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decodificar o JWT usando a chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # Obtém o e-mail do "sub" (subject)
        
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Você pode verificar se o usuário existe no banco de dados
        # usuário = crud.get_usuario_by_email(email)  # Exemplo de consulta para buscar o usuário

        return email  # Aqui você pode retornar o ID do usuário ou outro dado relevante do token
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro ao verificar o token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def gerar_hash_senha(senha: str):
    return pwd_context.hash(senha)
