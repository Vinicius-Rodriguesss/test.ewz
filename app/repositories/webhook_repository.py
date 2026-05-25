from app.models.webhook_event import (
WebhookEvent
)


class WebhookRepository:


    def existe(
        self,
        db,
        event_id
    ):

        return (

            db.query(
                WebhookEvent
            )

            .filter(

                WebhookEvent.event_id
                ==
                event_id

            )

            .first()

        )


    def salvar(
        self,
        db,
        event_id
    ):

        evento=WebhookEvent(
            event_id=
            event_id
        )

        db.add(
            evento
        )

        db.commit()