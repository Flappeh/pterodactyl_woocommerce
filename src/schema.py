from pydantic import BaseModel
from typing import List


class OrderItems(BaseModel):
    id: int
    name: str
    product_id: int
    quantity: int
    
class Customer(BaseModel):
    first_name: str
    last_name: str

class Billing(BaseModel):
    first_name: str
    last_name: str
    email: str

class UpdateOrder(BaseModel):
    id: int
    status: str
    line_items: List[OrderItems]
    billing: Billing
    
class Server(BaseModel):
    id: int
    name: str
    ram: int
    cpu: int
    disk: int
    database: int
    allocation: int
    backup: int
    
class PanelUser(BaseModel):
    id: int | None
    username: str
    email: str
    first_name: str
    last_name: str
    password: str | None