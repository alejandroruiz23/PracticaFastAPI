from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field

#Modelos me permiten validar informacion que ingresa y en este caso, al heredar de sqlmodel, me permitirá mapear para tener en cuenta para la bd
class CustomerBase(SQLModel):
    
    name:str = Field(default=None)
    #el pipe me permite decirle que puede usar cualquiera de los dos tipos
    description:str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

#al heredar de la clase base, y poner table en true, estoy indicando que me cree la tabla en la bd con las propiedades heredadas sumado a la propiedad que le agregue a esta, ID. Par que un campo se guarde en la bd se tiene que tener FIELD
class Customer( CustomerBase, table = True):
    id: int | None  = Field(default=None, primary_key=True)

class TransactionBase(SQLModel):
    ammount: int
    description: str

class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")#acceso a la foreing key de id de la tabla customer

class Invoice(BaseModel):
    id : int
    customer : Customer
    transactions: list[Transaction]
    total: int
    
    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)