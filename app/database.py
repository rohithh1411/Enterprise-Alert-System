from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import AlertDB, Base

DATABASE_URL = "sqlite:///./app/alerts.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        if db.query(AlertDB).count() == 0:
            sample_alerts = [
                AlertDB(
                    title="Login Failure",
                    description="Multiple failed login attempts were detected for a user account.",
                    severity="HIGH",
                    source="Authentication Service",
                    status="OPEN",
                    created_at=datetime.now(timezone.utc),
                ),
                AlertDB(
                    title="Malware Detected",
                    description="A suspicious process was identified on a production host.",
                    severity="CRITICAL",
                    source="Endpoint Protection",
                    status="ACKNOWLEDGED",
                    created_at=datetime.now(timezone.utc),
                ),
            ]
            db.add_all(sample_alerts)
            db.commit()
