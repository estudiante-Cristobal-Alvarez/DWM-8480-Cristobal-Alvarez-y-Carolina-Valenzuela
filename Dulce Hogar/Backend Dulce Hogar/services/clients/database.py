from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Ubicación de la carpeta clients
BASE_DIR = Path(__file__).resolve().parent

# Base de datos exclusiva del microservicio
DATABASE_URL = f"sqlite:///{(BASE_DIR / 'clients.db').as_posix()}"

# Conexión con SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Administrador de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base para los modelos
Base = declarative_base()