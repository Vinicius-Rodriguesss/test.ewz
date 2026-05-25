class PipefyService:
    CREATE_CARD_MUTATION = """
mutation CreateCard($input: CreateCardInput!) {
  createCard(input: $input) {
    card {
      id
    }
    clientMutationId
  }
}
""".strip()

    UPDATE_CARD_FIELD_MUTATION = """
mutation UpdateCardField($input: UpdateCardFieldInput!) {
  updateCardField(input: $input) {
    success
    clientMutationId
    card {
      id
    }
  }
}
""".strip()

    def build_create_card(
        self,
        nome,
        email,
        patrimonio
    ):
        return {
            "query": self.CREATE_CARD_MUTATION,
            "variables": {
                "input": {
                    "clientMutationId": "client-create-card",
                    "pipe_id": "PIPE_ID_AQUI",
                    "fields_attributes": [
                        {
                            "field_id": "cliente_nome",
                            "field_value": nome,
                        },
                        {
                            "field_id": "cliente_email",
                            "field_value": email,
                        },
                        {
                            "field_id": "valor_patrimonio",
                            "field_value": str(patrimonio),
                        },
                    ],
                }
            },
        }

    def build_update_card(
        self,
        card_id,
        status,
        prioridade
    ):
        return {
            "status_update": {
                "query": self.UPDATE_CARD_FIELD_MUTATION,
                "variables": {
                    "input": {
                        "clientMutationId": "client-update-status",
                        "card_id": card_id,
                        "field_id": "status",
                        "new_value": status,
                    }
                },
            },
            "priority_update": {
                "query": self.UPDATE_CARD_FIELD_MUTATION,
                "variables": {
                    "input": {
                        "clientMutationId": "client-update-priority",
                        "card_id": card_id,
                        "field_id": "prioridade",
                        "new_value": prioridade,
                    }
                },
            },
        }
