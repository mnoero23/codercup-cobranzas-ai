from datetime import date
from decimal import Decimal

import pandas as pd
import pytest
from sqlalchemy.orm import Session

from src.case_management import (
    enrich_queue_with_cases,
    load_case_events,
    load_collection_cases,
    save_collection_case,
)
from src.models import Customer


def add_customer(test_engine) -> None:
    with Session(test_engine) as session, session.begin():
        session.add(
            Customer(
                customer_id=10,
                customer_name="Cliente de gestión",
                tax_id="30-70000000-1",
                segment="Mayorista",
                province="Córdoba",
                region="Centro",
                credit_limit=Decimal("1000000.00"),
                payment_terms_days=30,
            )
        )


def test_save_collection_case_persists_current_state_and_history(test_engine):
    add_customer(test_engine)

    save_collection_case(
        10,
        status="contactado",
        owner="Matías",
        note="Solicitó reenvío de factura.",
        promise_date=None,
        promise_amount=None,
        target_engine=test_engine,
    )
    save_collection_case(
        10,
        status="comprometido",
        owner="Matías",
        note="Confirmó pago.",
        promise_date=date(2026, 9, 5),
        promise_amount=Decimal("250000.00"),
        target_engine=test_engine,
    )

    cases = load_collection_cases(test_engine)
    events = load_case_events(10, test_engine)

    assert len(cases) == 1
    assert cases.iloc[0].status == "comprometido"
    assert cases.iloc[0].promise_amount == Decimal("250000.00")
    assert len(events) == 2
    assert events.iloc[0].note == "Confirmó pago."


def test_committed_case_requires_promise_date(test_engine):
    add_customer(test_engine)

    with pytest.raises(ValueError, match="fecha de compromiso"):
        save_collection_case(
            10,
            status="comprometido",
            owner=None,
            note=None,
            promise_date=None,
            promise_amount=None,
            target_engine=test_engine,
        )


def test_enrich_queue_uses_defaults_and_saved_case_state():
    queue = pd.DataFrame(
        [
            {"customer_id": 10, "customer_name": "Gestionado"},
            {"customer_id": 20, "customer_name": "Nuevo"},
        ]
    )
    cases = pd.DataFrame(
        [
            {
                "customer_id": 10,
                "status": "resuelto",
                "owner": "Matías",
            }
        ]
    )

    result = enrich_queue_with_cases(queue, cases)

    assert result.loc[result.customer_id == 10, "status"].item() == "resuelto"
    assert result.loc[result.customer_id == 20, "status"].item() == "pendiente"
    assert result.loc[result.customer_id == 20, "owner"].item() == "Sin asignar"
