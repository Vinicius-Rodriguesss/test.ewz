from pydantic import (
BaseModel,
EmailStr
)


class WebhookRequest(
BaseModel
):

    event_id:str

    card_id:str

    cliente_email:EmailStr

    timestamp:str