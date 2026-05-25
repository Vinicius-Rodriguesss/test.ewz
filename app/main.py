from fastapi import (
    FastAPI,
    Request
)

from fastapi.exceptions import (
    RequestValidationError
)

from fastapi.responses import (
    JSONResponse
)

from app.database.connection import (
    Base,
    engine
)

from app.api.clientes import (
    router as cliente_router
)

from app.api.webhook import (
    router as webhook_router
)


Base.metadata.create_all(
    bind=engine
)


app=FastAPI()


app.include_router(
    cliente_router
)

app.include_router(
    webhook_router
)


@app.exception_handler(
    RequestValidationError
)

async def validation_handler(
    request: Request,
    exc: RequestValidationError
):

    for erro in exc.errors():

        if erro["loc"][-1]=="cliente_email":

            return JSONResponse(

                status_code=400,

                content={
                    "erro":
                    "cliente_email deve conter um e-mail válido"
                }

            )

    return JSONResponse(

        status_code=400,

        content={
            "erro":
            "Dados inválidos"
        }

    )