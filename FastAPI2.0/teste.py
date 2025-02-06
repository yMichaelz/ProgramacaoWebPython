import requests

url = "http://127.0.0.1:8000/login"
dados = {"email": "antony@gmail.com", "senha": "123"}

resposta = requests.post(url, json=dados)
print(resposta.json())  # Para ver a resposta do servidor
