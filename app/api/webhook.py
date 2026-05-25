from fastapi import APIRouter

from app.database.connection import (
    SessionLocal
)

from app.schemas.webhook_schema import (
    WebhookRequest
)

from app.services.webhook_service import (
    WebhookService
)


router = APIRouter()


@router.post(
"/webhooks/pipefy/card-updated"
)

def atualizar(
    payload:
    WebhookRequest
):

    db = SessionLocal()

    try:
        WebhookService().processar(
            db,
            payload
        )
    finally:
        db.close()


    return {

        "status":
        "Processado",

        "mensagem":
        "Webhook processado com sucesso"

    }
