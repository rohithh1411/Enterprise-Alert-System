from fastapi import Depends, FastAPI, HTTPException

from .alert_service import (
    Alert,
    AlertCreate,
    AlertStatusUpdate,
    AlertSummary,
    create_alert_data,
    delete_alert_data,
    get_alert_by_id_data,
    get_alert_summary_data,
    get_alerts_data,
    update_alert_status_data,
)

from .auth import get_api_key, require_admin

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Alert Management System is running"
    }


@app.get("/alerts", response_model=list[Alert], dependencies=[Depends(get_api_key)])
def get_alerts(status: str | None = None, severity: str | None = None):
    return get_alerts_data(status=status, severity=severity)


@app.post("/alerts", response_model=Alert, dependencies=[Depends(get_api_key)])
def create_alert(alert: AlertCreate):
    return create_alert_data(alert)


@app.get("/alerts/summary", response_model=AlertSummary, dependencies=[Depends(get_api_key)])
def get_alert_summary():
    return get_alert_summary_data()


@app.get("/alerts/{alert_id}", response_model=Alert, dependencies=[Depends(get_api_key)])
def get_alert_by_id(alert_id: int):
    alert = get_alert_by_id_data(alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@app.patch("/alerts/{alert_id}", response_model=Alert, dependencies=[Depends(get_api_key)])
def update_alert_status(alert_id: int, update: AlertStatusUpdate):
    alert = update_alert_status_data(alert_id, update)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@app.delete("/alerts/{alert_id}", dependencies=[Depends(require_admin)])
def delete_alert(alert_id: int):
    deleted = delete_alert_data(alert_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": f"Alert {alert_id} deleted successfully"}