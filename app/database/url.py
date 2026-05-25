import os


def get_database_url() -> str:
    """Retorna a URL do banco, priorizando a variavel de ambiente."""
    return os.getenv("DATABASE_URL", "sqlite:///./client_management.db")
