from app.models.cliente import (
Cliente
)


class ClienteRepository:


    def salvar(
        self,
        db,
        cliente
    ):

        db.add(
            cliente
        )

        db.commit()

        db.refresh(
            cliente
        )

        return cliente