# Usa una imagen base ligera con Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app/backend

# Copia los archivos del proyecto al contenedor
COPY . /app/backend

# Instala Poetry y las dependencias del proyecto
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi

# Expone el puerto en el que corre la aplicación
EXPOSE 8000

# Comando para correr la aplicación
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]