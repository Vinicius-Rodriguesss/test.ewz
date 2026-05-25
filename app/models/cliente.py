from sqlalchemy import (
Column,
Integer,
String
)

from app.database.connection import (
Base
)


class Cliente(Base):

    __tablename__="clientes"


    id=Column(
        Integer,
        primary_key=True
    )

    nome=Column(
        String,
        nullable=False
    )

    email=Column(
        String,
        nullable=False,
        unique=True
    )

    tipo_solicitacao=Column(
        String,
        nullable=False
    )

    valor_patrimonio=Column(
        Integer,
        nullable=False
    )

    status=Column(
        String,
        nullable=False
    )

    prioridade=Column(
        String,
        nullable=True
    )