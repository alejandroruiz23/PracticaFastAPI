from fastapi import APIRouter, HTTPException, status
from models import Customer, CustomerCreate, CustomerUpdate
from db import SessionDep
from sqlmodel import select

router = APIRouter()

'''Para que en la documentación se me dividan los modulos de los router, le agrego tags a cada endpoint en este caso con el nombre customers'''

@router.post("/customers", response_model=Customer, tags=["customers"])
async def create_customer(customer_data : CustomerCreate, session : SessionDep):
    #es para validar la información que entra
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def list_customer(session : SessionDep):
    print(session)
    return session.exec(select(Customer)).all()


@router.get("/customers/{customer_id}", response_model = Customer, tags=["customers"])
async def read_customer(customer_id: int,session : SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="El cliente no existe")
    return customer_db

@router.delete("/customers/{customer_id}", tags=["customers"])
async def delete_customer(customer_id: int,session : SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="El cliente no existe")
    session.delete(customer_db)
    session.commit()
    return {"detail":"OK"}

@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["customers"])
async def update_customer(customer_id: int, customer_data: CustomerUpdate ,session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="El cliente no existe")
    #model dump toma la data del body y la convierte dict o"json".
    #con el exclude unset solo actualiza los campos que vengan en el body
    
    print("Muestro customer_db")
    print(customer_db)


    print("Muestro customer_data")
    print(customer_data)

    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    print("Muestro customer_data_dict")
    print(customer_data_dict)

    
    customer_db.sqlmodel_update(customer_data_dict)
    

    session.add(customer_db)
    session.commit()
    #refresh para actualizar con los nuevos valores
    session.refresh(customer_db)
    
    return customer_db