import time

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

from app.database.url import get_database_url

load_dotenv()

DATABASE_URL = get_database_url()
IS_SQLITE = DATABASE_URL.startswith("sqlite")

engine_kwargs = {
    "pool_pre_ping": True,
}

if IS_SQLITE:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    **engine_kwargs,
)


def wait_for_db(engine, retries: int = 20, delay: float = 1.0) -> None:
    """Aguarda até que o banco de dados aceite conexões."""
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return
        except OperationalError as exc:
            last_error = exc
            if attempt == retries:
                break
            time.sleep(delay)

    raise RuntimeError(
        "Não foi possível conectar ao banco de dados após várias tentativas. "
        "Verifique se o serviço Postgres está em execução e se DATABASE_URL está correto."
    ) from last_error


if not IS_SQLITE:
    wait_for_db(engine)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
