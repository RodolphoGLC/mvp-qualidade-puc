from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

# Cria uma classe Base para o instanciamento de novos objetos.
Base: DeclarativeMeta = declarative_base()