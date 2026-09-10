from __future__ import annotations

from datetime import date, datetime, time, timedelta
from decimal import Decimal

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from src.database import engine as default_engine
from src.models import CollectionCase, CollectionCaseEvent, Customer


def seed_demo_cases(
    as_of: date,
    target_engine: Engine = default_engine,
) -> dict[str, int]:
    """Create a small, repeatable management story without overwriting user activity."""
    demo_cases = [
        {
            "customer_id": 6,
            "status": "contactado",
            "owner": "Equipo de Cobranzas",
            "note": "Se reenviaron las facturas y se solicitó una fecha estimada de pago.",
            "events": [
                (
                    2,
                    "contactado",
                    "Se reenviaron las facturas y se solicitó una fecha estimada de pago.",
                    None,
                    None,
                )
            ],
        },
        {
            "customer_id": 8,
            "status": "comprometido",
            "owner": "Equipo de Cobranzas",
            "note": "El cliente confirmó un pago parcial para la próxima semana.",
            "promise_date": as_of + timedelta(days=7),
            "promise_amount": Decimal("30000000.00"),
            "events": [
                (3, "contactado", "Se validó la documentación pendiente.", None, None),
                (
                    1,
                    "comprometido",
                    "El cliente confirmó un pago parcial para la próxima semana.",
                    as_of + timedelta(days=7),
                    Decimal("30000000.00"),
                ),
            ],
        },
        {
            "customer_id": 1,
            "status": "resuelto",
            "owner": "Equipo de Cobranzas",
            "note": "Pago acreditado y conciliado; caso cerrado.",
            "events": [
                (5, "contactado", "Se acordó cancelar el saldo vencido.", None, None),
                (1, "resuelto", "Pago acreditado y conciliado; caso cerrado.", None, None),
            ],
        },
    ]

    created_cases = 0
    created_events = 0
    with Session(target_engine) as session, session.begin():
        customer_ids = set(session.scalars(select(Customer.customer_id)))
        existing_customer_ids = set(session.scalars(select(CollectionCase.customer_id)))
        for spec in demo_cases:
            customer_id = spec["customer_id"]
            if customer_id not in customer_ids or customer_id in existing_customer_ids:
                continue
            latest_at = datetime.combine(as_of - timedelta(days=1), time(hour=10))
            case = CollectionCase(
                customer_id=customer_id,
                status=spec["status"],
                owner=spec["owner"],
                last_note=spec["note"],
                promise_date=spec.get("promise_date"),
                promise_amount=spec.get("promise_amount"),
                last_action_at=latest_at,
                created_at=latest_at,
                updated_at=latest_at,
            )
            session.add(case)
            session.flush()
            created_cases += 1
            for days_ago, status, note, promise_date, promise_amount in spec["events"]:
                session.add(
                    CollectionCaseEvent(
                        case_id=case.case_id,
                        status=status,
                        owner=spec["owner"],
                        note=note,
                        promise_date=promise_date,
                        promise_amount=promise_amount,
                        created_at=datetime.combine(
                            as_of - timedelta(days=days_ago), time(hour=10)
                        ),
                    )
                )
                created_events += 1
    return {"cases": created_cases, "events": created_events}
