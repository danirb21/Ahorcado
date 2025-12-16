# app/utils/config.py
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
# --- Detección de la ruta base ---
def get_base_path():
    """Retorna la ruta base: directorio de PyInstaller o directorio del script."""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        # Entorno de desarrollo normal
        # Usamos .cwd() o el directorio del script, dependiendo de dónde se espera que esté el .env
        return Path(__file__).resolve().parent.parent

def load_environment_variables():
    """Carga variables de entorno desde el archivo .env."""
        
    base_path = get_base_path()
    dotenv_path = base_path / ".env"

    if dotenv_path.exists():
        load_dotenv(dotenv_path)
    else:
        # Advertencia en caso de que falte el .env
        print(f"❌ Advertencia: Archivo .env no encontrado en {dotenv_path}. Usando variables del sistema.")
        load_dotenv() 

# --- Función para acceder a archivos de recursos ---
def get_resource_path(relative_path):
    return get_base_path() / relative_path
            
# --- Llamada de inicialización ---
load_environment_variables()