from typing import Annotated

from sqlmodel import Field, Session, SQLModel, create_engine, select

class Server(SQLModel, table=True):
    __tablename__ = "server"
    id = int | None = Field(default=None, primary_key=True)


class Order(SQLModel, table=True):
    __tablename__ = "order"
    