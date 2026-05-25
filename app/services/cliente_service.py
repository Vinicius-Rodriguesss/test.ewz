from app.models.cliente import Cliente

from app.repositories.cliente_repository import (
ClienteRepository
)

from app.services.pipefy_service import (
PipefyService
)


class ClienteService:


    def criar(
        self,
        db,
        payload
    ):


        cliente=Cliente(

            nome=
            payload.cliente_nome,

            email=
            payload.cliente_email,

            tipo_solicitacao=
            payload.tipo_solicitacao,

            valor_patrimonio=
            payload.valor_patrimonio,

            status=
            "Aguardando Análise"
        )


        cliente=ClienteRepository().salvar(
            db,
            cliente
        )


        graphql=PipefyService().build_create_card(

            cliente.nome,

            cliente.email,

            cliente.valor_patrimonio
        )


        return {

            "cliente":
            cliente,

            "pipefy":
            graphql
        }