# 📬 Portfolio Contact Form API

A lightweight FastAPI backend that handles contact form submissions from a personal portfolio site and delivers them to your inbox via Gmail SMTP.

---

## Features

- `POST /contact` — validates and processes contact form submissions
- `GET /health` — simple health check endpoint
- Input validation via Pydantic (name length, message length, allowed subjects, email format)
- Gmail SMTP email delivery using `smtplib`
- CORS configured for local React dev servers
- Environment variable support via `python-dotenv`
- Request logging for every submission

---

## Requirements

- Python 3.10+
- A Gmail account with [2-Step Verification](https://myaccount.google.com/security) enabled
- A Gmail [App Password](https://myaccount.google.com/apppasswords) generated for this app

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/your-username/my-portfolio-api.git
cd my-portfolio-api

# 2. Create and activate a virtual environment
python -m venv my-pf-venv
source my-pf-venv/bin/activate      # macOS/Linux
my-pf-venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install fastapi uvicorn pydantic[email] python-dotenv
```

---

## Environment Variables

Create a `.env` file in the root of the project:

```dotenv
MY_PORTFOLIO_USER="you@gmail.com"         # Gmail account used to send emails
MY_PORTFOLIO_PASS="xxxx xxxx xxxx xxxx"   # Gmail App Password (16 characters)
MY_PORTFOLIO_FROM="you@gmail.com"         # Must match MY_PORTFOLIO_USER for Gmail
MY_PORTFOLIO_TO="inbox@example.com"       # Where you want to receive messages
```

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

---

## Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## API Reference

### `POST /contact`

Submits a contact form message and sends it to your configured email.

**Request Body**

| Field     | Type   | Required | Constraints                                                                 |
|-----------|--------|----------|-----------------------------------------------------------------------------|
| `name`    | string | ✅       | Non-empty, max 100 characters                                               |
| `email`   | string | ✅       | Valid email format                                                          |
| `subject` | string | ✅       | One of: `New Project Inquiry`, `General Question`, `Collaboration`, `Other` |
| `message` | string | ✅       | Non-empty, max 5000 characters                                              |

**Example Request**

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "subject": "New Project Inquiry",
  "message": "Hi, I'd love to discuss a project with you!"
}
```

**Example Response**

```json
{
  "success": true,
  "message": "Your message has been received."
}
```

---

### `GET /health`

Returns the current status of the API.

**Response**

```json
{
  "status": "ok"
}
```

---

## CORS Configuration

By default, the API allows requests from:

- `http://localhost:3000` (Create React App)
- `http://localhost:5173` (Vite)

To allow your production frontend, update `allow_origins` in `main.py`:

```python
allow_origins=["https://your-portfolio-domain.com"]
```

---

## Project Structure

```
my-portfolio-api/
├── main.py        # FastAPI app — routes, validation, email logic
├── .env           # Environment variables (do not commit)
├── .gitignore
└── README.md
```

---

## .gitignore Recommendation

```gitignore
.env
__pycache__/
my-pf-venv/
*.pyc
```