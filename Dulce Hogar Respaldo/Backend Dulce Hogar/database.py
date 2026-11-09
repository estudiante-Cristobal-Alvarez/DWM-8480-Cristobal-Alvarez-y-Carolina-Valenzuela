from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ubicación de la base de datos SQLite
DATABASE_URL = "sqlite:///./dulce_hogar.db"

# Crear conexión con la base de datos
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Crear sesiones para realizar operaciones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base para los modelos de la base de datos
Base = declarative_base()