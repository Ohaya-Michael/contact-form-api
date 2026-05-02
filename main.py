from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model.contact_model import ContactRequest, ContactResponse
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
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173", 
        "https://michael-ohaya-my-portfolio.netlify.app"
        ],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

