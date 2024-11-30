'''Esto es estandar para la creación de modelos y uso de bases de datos en cualquier proyecto con fastapi.

- Si requiero cambiar el tipo de motor o gestor de base de datos, lo podría cambiar en el nombre de la base de datos
'''
# session es para crear sesion y el engine es para indicar el motor de la bd
from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends, FastAPI


sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url)

#creo una funcion para el inicio de la sesion el cual estará disponible para ser usado en los endpoint cuando de requiera, por eso se requiere el uso de las anotaciones y dependencia de fastapi.
#para poder crear las tablas requiero d un comando 

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    with Session(engine) as session:
        yield session


#Posteriormente, se importa la SessionDep cuando requiera uso en los endpoints, los cuales van a requir que sessiondep sea un argumento que se pase para poder hacer uso de este
SessionDep = Annotated[Session, Depends(get_session)]




