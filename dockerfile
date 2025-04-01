# Usando Python como base
FROM python:3.9

# Usando Python como base
FROM python:3.9

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando os arquivos para dentro do container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o código da API
COPY . .

# Expondo a porta onde o Flask vai rodar
EXPOSE 5000

# Comando para rodar a API
CMD ["python", "app.py"]

