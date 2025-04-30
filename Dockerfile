# Usa una imagen base de Python 3.12
FROM python:3.12

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY ./ /app

# Instala las dependencias de sistema
RUN apt-get update && \
    apt-get install -y libmariadb-dev

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Define la variable de entorno PORT con un valor predeterminado si no se especifica
ENV PORT=${PORT:-3000}

# Define las variables de entorno
ENV RAILWAY_SERVICE_NAME=$RAILWAY_SERVICE_NAME \
    RAILWAY_TCP_PROXY_PORT=$RAILWAY_TCP_PROXY_PORT \
    RAILWAY_TCP_APPLICATION_PORT=$RAILWAY_TCP_APPLICATION_PORT 

# Muestra las variables de entorno para verificar
RUN echo $PORT
RUN echo $RAILWAY_SERVICE_NAME
RUN echo $RAILWAY_TCP_PROXY_PORT
RUN echo $RAILWAY_TCP_APPLICATION_PORT

# Ejecutar tu aplicación
CMD ["bash", "start.sh"]