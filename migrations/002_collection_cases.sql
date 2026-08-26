-- Gestión de casos de cobranzas y trazabilidad de cambios.
-- La creación portable se realiza desde SQLAlchemy; este archivo documenta el cambio.
CREATE INDEX IF NOT EXISTS ix_collection_case_status_owner
    ON collection_cases(status, owner);
CREATE INDEX IF NOT EXISTS ix_collection_case_event_case_date
    ON collection_case_events(case_id, created_at);
