from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field

from .database import SessionLocal, create_db
from .models import AlertDB


class AlertCreate(BaseModel):
    title: str
    description: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    source: str


class Alert(AlertCreate):
    id: int
    status: Literal["OPEN", "ACKNOWLEDGED", "RESOLVED"] = "OPEN"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AlertStatusUpdate(BaseModel):
    status: Literal["OPEN", "ACKNOWLEDGED", "RESOLVED"]


class AlertSummary(BaseModel):
    total_alerts: int
    open: int
    acknowledged: int
    resolved: int
    critical: int
    high: int
    medium: int
    low: int


create_db()


def _alert_db_to_model(alert_db: AlertDB) -> Alert:
    created_at = alert_db.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    return Alert(
        id=alert_db.id,
        title=alert_db.title,
        description=alert_db.description,
        severity=alert_db.severity,
        source=alert_db.source,
        status=alert_db.status,
        created_at=created_at,
    )


def get_alerts_data(status: str | None = None, severity: str | None = None):
    with SessionLocal() as db:
        query = db.query(AlertDB)

        if status:
            query = query.filter(AlertDB.status == status.upper())

        if severity:
            query = query.filter(AlertDB.severity == severity.upper())

        alerts_db = query.order_by(AlertDB.id).all()

    return [_alert_db_to_model(alert) for alert in alerts_db]


def create_alert_data(alert: AlertCreate):
    with SessionLocal() as db:
        alert_db = AlertDB(
            title=alert.title,
            description=alert.description,
            severity=alert.severity,
            source=alert.source,
            status="OPEN",
            created_at=datetime.now(timezone.utc),
        )
        db.add(alert_db)
        db.commit()
        db.refresh(alert_db)

    return _alert_db_to_model(alert_db)


def get_alert_by_id_data(alert_id: int):
    with SessionLocal() as db:
        alert_db = db.query(AlertDB).filter(AlertDB.id == alert_id).first()

    if alert_db is None:
        return None

    return _alert_db_to_model(alert_db)


def update_alert_status_data(alert_id: int, update: AlertStatusUpdate):
    with SessionLocal() as db:
        alert_db = db.query(AlertDB).filter(AlertDB.id == alert_id).first()
        if alert_db is None:
            return None

        alert_db.status = update.status
        db.commit()
        db.refresh(alert_db)

    return _alert_db_to_model(alert_db)


def delete_alert_data(alert_id: int):
    with SessionLocal() as db:
        alert_db = db.query(AlertDB).filter(AlertDB.id == alert_id).first()
        if alert_db is None:
            return False

        db.delete(alert_db)
        db.commit()

    return True


def get_alert_summary_data():
    with SessionLocal() as db:
        total_alerts = db.query(AlertDB).count()
        open_count = db.query(AlertDB).filter(AlertDB.status == "OPEN").count()
        acknowledged_count = db.query(AlertDB).filter(AlertDB.status == "ACKNOWLEDGED").count()
        resolved_count = db.query(AlertDB).filter(AlertDB.status == "RESOLVED").count()
        critical_count = db.query(AlertDB).filter(AlertDB.severity == "CRITICAL").count()
        high_count = db.query(AlertDB).filter(AlertDB.severity == "HIGH").count()
        medium_count = db.query(AlertDB).filter(AlertDB.severity == "MEDIUM").count()
        low_count = db.query(AlertDB).filter(AlertDB.severity == "LOW").count()

    return AlertSummary(
        total_alerts=total_alerts,
        open=open_count,
        acknowledged=acknowledged_count,
        resolved=resolved_count,
        critical=critical_count,
        high=high_count,
        medium=medium_count,
        low=low_count,
    )
