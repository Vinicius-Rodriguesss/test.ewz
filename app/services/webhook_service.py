from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models.cliente import Cliente

from app.repositories.webhook_repository import (
    WebhookRepository
)

from app.services.pipefy_service import (
    PipefyService
)


class WebhookService:


    def processar(
        self,
        db,
        payload
    ):

        repo = WebhookRepository()


        # idempotência
        if repo.existe(
            db,
            payload.event_id
        ):

            raise HTTPException(

                status_code=409,

                detail="evento duplicado"

            )


        # buscar cliente
        cliente = (

            db.query(
                Cliente
            )

            .filter(
                Cliente.email
                ==
                payload.cliente_email
            )

            .first()

        )


        # cliente não encontrado
        if not cliente:

            raise HTTPException(

                status_code=404,

                detail="cliente não encontrado"

            )


        # regra de prioridade
        prioridade = (

            "prioridade_alta"

            if
            cliente.valor_patrimonio
            >=
            200000

            else

            "prioridade_normal"

        )


        # atualizar cliente
        cliente.status = (
            "Processado"
        )

        cliente.prioridade = (
            prioridade
        )

        db.commit()


        # registrar evento
        try:
            repo.salvar(
                db,
                payload.event_id
            )
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail="evento duplicado"
            ) from exc


        # gerar mutation Pipefy
        mutation = (

            PipefyService()

            .build_update_card(

                payload.card_id,

                cliente.status,

                prioridade

            )

        )


        print("\n===== PIPEFY UPDATE =====")

        print(
            mutation
        )

        print("========================\n")


        return mutation
