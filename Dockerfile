FROM python:3.8-slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required by TensorFlow and DVC
# Adicione 'git' aqui, pois o DVC pode precisar dele para algumas operações
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    libhdf5-dev \
    libprotobuf-dev \
    protobuf-compiler \
    python3-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application code and DVC files
# Isso incluirá seu código, setup.py, .dvc/config, e o diretório 'model/' (que será populado pelo DVC pull)
COPY . .

# Install dependencies from setup.py (editable mode)
# Certifique-se de que seu setup.py lista todas as dependências necessárias para o runtime (inferência)
RUN pip install --no-cache-dir -e .

# Instale DVC e o driver para GCS dentro da imagem.
# Isso é crucial caso o application.py precise interagir com DVC ou GCS diretamente,
# ou se o modelo for carregado de um caminho DVC-tracked.
RUN pip install --no-cache-dir dvc google-cloud-storage

# REMOVA ESTA LINHA: O treinamento não deve ocorrer durante a construção da imagem.
# RUN python pipeline/pipeline_training.py

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the app
# O application.py deve carregar o modelo do diretório 'model/' (que será puxado pelo DVC)
CMD ["python", "application.py"]