from fastapi.testclient import TestClient

from app.database.connection import Base, SessionLocal, engine
from app.main import app
from app.models.cliente import Cliente
from app.models.webhook_event import WebhookEvent


client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_criar_cliente_valido_salva_no_banco():
    response = client.post(
        "/clientes",
        json={
            "cliente_nome": "Test User",
            "cliente_email": "test@example.com",
            "tipo_solicitacao": "Consultoria",
            "valor_patrimonio": 100000,
        },
    )

    assert response.status_code == 200

    db = SessionLocal()
    try:
        cliente = db.query(Cliente).filter(Cliente.email == "test@example.com").first()
        assert cliente is not None
        assert cliente.nome == "Test User"
        assert cliente.status == "Aguardando Análise"
    finally:
        db.close()


def test_webhook_aplica_prioridade_alta_quando_patrimonio_maior_ou_igual_a_200_mil():
    client.post(
        "/clientes",
        json={
            "cliente_nome": "Webhook User",
            "cliente_email": "webhook@example.com",
            "tipo_solicitacao": "Consultoria",
            "valor_patrimonio": 250000,
        },
    )

    response = client.post(
        "/webhooks/pipefy/card-updated",
        json={
            "event_id": "evt-123",
            "card_id": "card-123",
            "cliente_email": "webhook@example.com",
            "timestamp": "2026-05-23T14:30:00Z",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Processado"

    db = SessionLocal()
    try:
        cliente = db.query(Cliente).filter(Cliente.email == "webhook@example.com").first()
        evento = db.query(WebhookEvent).filter(WebhookEvent.event_id == "evt-123").first()
        assert cliente is not None
        assert cliente.status == "Processado"
        assert cliente.prioridade == "prioridade_alta"
        assert evento is not None
    finally:
        db.close()


def test_webhook_bloqueia_evento_duplicado():
    client.post(
        "/clientes",
        json={
            "cliente_nome": "Duplicate Event",
            "cliente_email": "duplicate@example.com",
            "tipo_solicitacao": "Consultoria",
            "valor_patrimonio": 150000,
        },
    )

    payload = {
        "event_id": "evt-duplicado",
        "card_id": "card-456",
        "cliente_email": "duplicate@example.com",
        "timestamp": "2026-05-18T12:00:00Z",
    }

    first_response = client.post("/webhooks/pipefy/card-updated", json=payload)
    second_response = client.post("/webhooks/pipefy/card-updated", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "evento duplicado"

    db = SessionLocal()
    try:
        eventos = db.query(WebhookEvent).filter(WebhookEvent.event_id == "evt-duplicado").all()
        cliente = db.query(Cliente).filter(Cliente.email == "duplicate@example.com").first()
        assert len(eventos) == 1
        assert cliente is not None
        assert cliente.prioridade == "prioridade_normal"
    finally:
        db.close()
