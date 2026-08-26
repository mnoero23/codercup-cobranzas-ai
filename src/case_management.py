from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

import pandas as pd
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from src.database import engine as default_engine
from src.models import CollectionCase, CollectionCaseEvent, Customer

CASE_STATUSES = ("pendiente", "contactado", "comprometido", "resuelto")


def load_collection_cases(target_engine: Engine = default_engine) -> pd.DataFrame:
    statement = select(
        CollectionCase.case_id,
        CollectionCase.customer_id,
        CollectionCase.status,
        CollectionCase.owner,
        CollectionCase.last_note,
        CollectionCase.promise_date,
        CollectionCase.promise_amount,
        CollectionCase.last_action_at,
        CollectionCase.updated_at,
    ).order_by(CollectionCase.updated_at.desc())
    return pd.read_sql(statement, target_engine)


def load_case_events(customer_id: int, target_engine: Engine = default_engine) -> pd.DataFrame:
    statement = (
        select(
            CollectionCaseEvent.created_at,
            CollectionCaseEvent.status,
            CollectionCaseEvent.owner,
            CollectionCaseEvent.note,
            CollectionCaseEvent.promise_date,
            CollectionCaseEvent.promise_amount,
        )
        .join(CollectionCase, CollectionCase.case_id == CollectionCaseEvent.case_id)
        .where(CollectionCase.customer_id == customer_id)
        .order_by(CollectionCaseEvent.created_at.desc())
    )
    return pd.read_sql(statement, target_engine)


def save_collection_case(
    customer_id: int,
    *,
    status: str,
    owner: str | None,
    note: str | None,
    promise_date: date | None,
    promise_amount: Decimal | None,
    target_engine: Engine = default_engine,
) -> None:
    if status not in CASE_STATUSES:
        raise ValueError(f"Estado de gestión inválido: {status}")
    if status == "comprometido" and promise_date is None:
        raise ValueError("Un caso comprometido requiere fecha de compromiso.")
    if promise_amount is not None and promise_amount < 0:
        raise ValueError("El importe comprometido no puede ser negativo.")

    clean_owner = owner.strip() if owner and owner.strip() else None
    clean_note = note.strip() if note and note.strip() else None
    now = datetime.utcnow()

    with Session(target_engine) as session, session.begin():
        if session.get(Customer, customer_id) is None:
            raise ValueError("El cliente no existe.")
        case = session.scalar(
            select(CollectionCase).where(CollectionCase.customer_id == customer_id)
        )
        if case is None:
            case = CollectionCase(customer_id=customer_id)
            session.add(case)
            session.flush()

        case.status = status
        case.owner = clean_owner
        case.last_note = clean_note
        case.promise_date = promise_date
        case.promise_amount = promise_amount
        case.last_action_at = now
        case.updated_at = now
        session.add(
            CollectionCaseEvent(
                case_id=case.case_id,
                status=status,
                owner=clean_owner,
                note=clean_note,
                promise_date=promise_date,
                promise_amount=promise_amount,
                created_at=now,
            )
        )


def enrich_queue_with_cases(queue: pd.DataFrame, cases: pd.DataFrame) -> pd.DataFrame:
    if queue.empty:
        return queue.copy()
    result = queue.merge(cases, on="customer_id", how="left")
    result["status"] = result.status.fillna("pendiente")
    result["owner"] = result.owner.fillna("Sin asignar")
    return result
