import csv

# Variáveis para armazenar a soma das idades e rendas e contar o número de clientes
soma_idade = 0
soma_renda = 0
contador = 0

# Abrindo e lendo o arquivo CSV
with open('/home/mike/Documentos/ProgramacaoWeb/Aula001/clientes.csv', newline='') as csvfile:
    leitor = csv.reader(csvfile, delimiter=';')
    next(leitor)  # Pular o cabeçalho

    # Para cada linha no arquivo, somar idade e renda
    for linha in leitor:
        idade = int(linha[2])
        renda = float(linha[3])
        
        soma_idade += idade
        soma_renda += renda
        contador += 1

# Calculando as médias
media_idade = soma_idade / contador
media_renda = soma_renda / contador

# Mostrando as médias
print(f"Média de idade dos clientes: {media_idade:.2f}")
print(f"Média de renda mensal dos clientes: R${media_renda:.2f}")
