# Usa a imagem oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala o Django e outras dependências
RUN pip install -r requirements.txt

# Copia o projeto para o diretório de trabalho do container
COPY . .

# Expõe a porta 8000 para o servidor Django
EXPOSE 8000

# Comando para iniciar o servidor de desenvolvimento Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]