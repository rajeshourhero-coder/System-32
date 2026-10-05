import time
import asyncio
from typing import List
from fastapi import FastAPI, BackgroundTasks, status
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="Background Tasks (Async Email)",
    version="1.0.0"
)

class EmailRequest(BaseModel):
    recipient_email: EmailStr
    subject: str
    body: str

sent_email_logs: List[dict] = []

def send_email_background_task(recipient_email: str, subject: str, body: str):
    time.sleep(1)
    sent_email_logs.append({
        "recipient": recipient_email,
        "subject": subject,
        "status": "DELIVERED",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.get("/")
def home():
    return {"message": "Background Task Service API"}

@app.post("/send-email", status_code=status.HTTP_202_ACCEPTED)
def trigger_email_notification(
    email_data: EmailRequest,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        send_email_background_task,
        email_data.recipient_email,
        email_data.subject,
        email_data.body
    )

    return {
        "status": "Accepted",
        "message": f"Email notification to '{email_data.recipient_email}' queued in background.",
        "recipient": email_data.recipient_email
    }

@app.get("/email-logs")
def get_email_logs():
    return {
        "total_sent": len(sent_email_logs),
        "logs": sent_email_logs
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
