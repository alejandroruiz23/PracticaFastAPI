import datetime

from fastapi import FastAPI
from sqlmodel import select
from models import Transaction, Invoice
from db import create_all_tables
from .routers import customers

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)

@app.get("/saludar/{nombre}")
async def saludar(nombre: str):
    nombreUp = nombre.upper()
    return {"saludo":f"Hola, bienvenido/a {nombreUp}"}

@app.get("/hora")
async def hora():
    return {"Hora":datetime.datetime.now()}






@app.post("/transactions")
async def create_transaction(transaction_data : Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data : Invoice):
    return invoice_data