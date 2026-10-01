# Enterprise Alert Management System

This project is a simple FastAPI-based alert management service.

## Project structure

- `app/main.py` - FastAPI application
- `app/requirements.txt` - project dependencies
- `run.bat` - Windows batch launcher
- `run.ps1` - PowerShell launcher

## Run the app

From the project root:

```powershell
.\run.bat
```

or:

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

The app will run on:

- http://127.0.0.1:8010
- http://127.0.0.1:8010/docs

## Authentication

The alert endpoints require an API key in the `X-API-Key` header.

Available keys:

```text
dev-alert-key
admin-key
operator-key
```

The role mapping is:

- `admin-key` → admin access
- `operator-key` → operator access
- `dev-alert-key` → default local access

To override the default key for your environment:

```powershell
$env:ALERT_API_KEY="your-custom-key"
```

## Available endpoints

- `GET /` - Health check
- `GET /alerts` - List all alerts
- `POST /alerts` - Create a new alert
- `GET /alerts/{alert_id}` - Get a specific alert
- `PATCH /alerts/{alert_id}` - Update alert status
- `DELETE /alerts/{alert_id}` - Delete an alert
- `GET /alerts/summary` - Get overall alert totals by status and severity

## Example alert payload

```json
{
  "title": "Login Failure",
  "description": "Multiple failed login attempts detected",
  "severity": "HIGH",
  "source": "Authentication Service"
}
```

## Example status update

```json
{
  "status": "ACKNOWLEDGED"
}
```

## Example summary response

```json
{
  "total_alerts": 2,
  "open": 1,
  "acknowledged": 1,
  "resolved": 0,
  "critical": 1,
  "high": 1,
  "medium": 0,
  "low": 0
}
```
