from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal
from dotenv import load_dotenv
import logging
load_dotenv()

# Logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# App 
app = FastAPI(title="Contact Form API")

# CORS 
# Update allow_origins to match your frontend URL in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema definitions
VALID_SUBJECTS = Literal[
    "New Project Inquiry",
    "General Question",
    "Collaboration",
    "Other",
]

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: VALID_SUBJECTS
    message: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name must not be empty.")
        if len(v) > 100:
            raise ValueError("Name must be 100 characters or fewer.")
        return v

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Message must not be empty.")
        if len(v) > 5000:
            raise ValueError("Message must be 5000 characters or fewer.")
        return v


class ContactResponse(BaseModel):
    success: bool
    message: str


# Routes 
@app.post("/contact", response_model=ContactResponse)
async def submit_contact(payload: ContactRequest):
    """
    Receives the contact form submission and processes it.
    Replace the body below with your real logic:
      - send an email (smtplib, SendGrid, Resend, etc.)
      - save to a database
      - post to Slack / Discord webhook
    """
    logger.info(
        "New contact submission | name=%s | email=%s | subject=%s| message=%s",
        payload.name,
        payload.email,
        payload.subject,
        payload.message[:100] + ("..." if len(payload.message) > 100 else ""),
    )

    import smtplib, os
    from email.message import EmailMessage
    msg = EmailMessage()
    msg["Subject"] = f"[Contact] {payload.subject}"
    msg["From"]    = os.environ["MY_PORTFOLIO_FROM"]
    msg["To"]      = os.environ["MY_PORTFOLIO_TO"]
    msg.set_content(f"From: {payload.name} <{payload.email}>\n\n{payload.message}")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.environ["MY_PORTFOLIO_USER"], os.environ["MY_PORTFOLIO_PASS"])
        smtp.send_message(msg)

    return ContactResponse(success=True, message="Your message has been received.")


# Health check 
@app.get("/health")
def health():
    return {"status": "ok"}

