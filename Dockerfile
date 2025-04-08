#Imagen oficial de Python
FROM python:3.10-slim

#Directorio de trabajo
WORKDIR /app

#Copia los archivos
COPY . .

#Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

#Expone el puerto
EXPOSE 5000

# Comando para correr la app
CMD ["python", "app.py"]