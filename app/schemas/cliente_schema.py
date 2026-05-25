from pydantic import (
BaseModel,
EmailStr
)


class ClienteRequest(
BaseModel
):

    cliente_nome:str

    cliente_email:EmailStr

    tipo_solicitacao:str

    valor_patrimonio:int