import os
from dotenv import load_dotenv

load_dotenv()  # Cargar las variables de entorno desde el archivo .env

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
