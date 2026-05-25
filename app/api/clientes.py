from fastapi import (
APIRouter
)

from app.schemas.cliente_schema import (
ClienteRequest
)

from app.services.cliente_service import (
ClienteService
)

from app.database.connection import (
SessionLocal
)


router=APIRouter()


@router.post(
"/clientes"
)

def criar(
payload:
ClienteRequest
):

    db=SessionLocal()

    try:
        resultado=ClienteService().criar(
            db,
            payload
        )
    finally:
        db.close()


    return {

        "id":
    resultado["cliente"].id,

    "nome":
    resultado["cliente"].nome,

    "email":
    resultado["cliente"].email,

    "status":
    resultado["cliente"].status,

    "mensagem":
    "Cliente criado e mapeamento Pipefy gerado"
    }
