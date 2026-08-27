import pandas as pd

from src.cobranzas import (
    _priority_label,
    collection_message,
    prioritize_receivables,
)


def sample_receivables() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "invoice_id": 1,
                "customer_id": 10,
                "customer_name": "Cliente crítico",
                "balance": 800_000,
                "credit_limit": 500_000,
                "days_past_due": 120,
                "derived_status": "vencida",
            },
            {
                "invoice_id": 2,
                "customer_id": 20,
                "customer_name": "Cliente preventivo",
                "balance": 100_000,
                "credit_limit": 1_000_000,
                "days_past_due": 0,
                "derived_status": "pendiente",
            },
        ]
    )


def test_prioritize_receivables_puts_highest_risk_first():
    queue = prioritize_receivables(sample_receivables())

    assert queue.customer_name.tolist() == ["Cliente crítico", "Cliente preventivo"]
    assert queue.iloc[0].priority == "Crítica"
    assert queue.iloc[0].priority_score > queue.iloc[1].priority_score
    assert "120 días" in queue.iloc[0].explanation
    assert queue.priority_score.between(0, 100).all()
    contribution_columns = [
        "overdue_contribution",
        "arrears_contribution",
        "credit_contribution",
        "concentration_contribution",
    ]
    assert queue.iloc[0].priority_score == queue.iloc[0][contribution_columns].sum()


def test_priority_thresholds_include_exact_boundaries():
    assert _priority_label(44.9) == "Seguimiento"
    assert _priority_label(45.0) == "Alta"
    assert _priority_label(69.9) == "Alta"
    assert _priority_label(70.0) == "Crítica"


def test_zero_credit_and_inconsistent_balances_are_safe():
    receivables = sample_receivables()
    receivables.loc[0, "credit_limit"] = 0
    receivables.loc[1, "balance"] = -100

    queue = prioritize_receivables(receivables)

    assert queue.customer_name.tolist() == ["Cliente crítico"]
    assert queue.iloc[0].credit_utilization == 0
    assert queue.priority_score.between(0, 100).all()


def test_relative_normalization_can_change_score_but_preserves_explainability():
    base = prioritize_receivables(sample_receivables())
    expanded_items = pd.concat(
        [
            sample_receivables(),
            pd.DataFrame(
                [
                    {
                        "invoice_id": 3,
                        "customer_id": 30,
                        "customer_name": "Cliente dominante",
                        "balance": 2_000_000,
                        "credit_limit": 2_000_000,
                        "days_past_due": 60,
                        "derived_status": "vencida",
                    }
                ]
            ),
        ],
        ignore_index=True,
    )
    expanded = prioritize_receivables(expanded_items)

    base_score = base.loc[base.customer_id == 10, "priority_score"].iloc[0]
    expanded_score = expanded.loc[expanded.customer_id == 10, "priority_score"].iloc[0]
    assert expanded_score != base_score
    assert expanded.loc[expanded.customer_id == 10, "explanation"].iloc[0]


def test_prioritize_receivables_returns_defined_empty_shape():
    empty = sample_receivables().assign(balance=0)

    assert prioritize_receivables(empty).empty
    assert "priority_score" in prioritize_receivables(empty).columns


def test_collection_message_keeps_human_reviewable_context():
    message = collection_message("Cliente crítico", 800_000, 120)

    assert "Cliente crítico" in message
    assert "$800.000" in message
    assert "120 días" in message
    assert "fecha prevista de pago" in message
