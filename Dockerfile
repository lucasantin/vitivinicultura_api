# Usar uma imagem base do Python 3.8
FROM python:3.8-slim

# Definir argumentos de build
ARG PROJECT_DIR=/app

# Definir o diretório de trabalho dentro do contêiner
WORKDIR ${PROJECT_DIR}

# Copiar o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expor a porta que a aplicação usará
EXPOSE 5000

# Definir o comando padrão para executar a aplicação
CMD ["python", "run.py"]
