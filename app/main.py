"""A one-page follow-up for people we meet at a robotics show.

We don't know who will walk up to the booth, so the page is deliberately
generic: the visitor reads a draft we prepared, edits it in place, and hands
it to Gmail — they send it to us themselves. They can also book a meeting here.

    uvicorn app.main:app --reload
    http://127.0.0.1:8000/
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from .config import TEMPLATE_DIR, profile

app = FastAPI(title="Conference Follow-up Page", version="0.3.0")

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=True,
    undefined=StrictUndefined,  # a missing variable is an error, not a blank
    trim_blocks=True,
    lstrip_blocks=True,
)


def context() -> dict:
    """Everything the templates need. All of it comes from config."""
    return {
        "people": profile.people,
        "contact_email": profile.email,
        "our_company": profile.company,
        "website": profile.website,
        "calendly_url": profile.calendly_url,
        "one_liner": profile.one_liner,
        "value_props": profile.value_props,
        "event_name": profile.event_name,
    }


def render_draft(ctx: dict) -> tuple[str, str]:
    subject = env.get_template("draft.subject.j2").render(**ctx).strip()
    body = env.get_template("draft.body.j2").render(**ctx).strip()
    return subject, body


@app.get("/", response_class=HTMLResponse)
def page():
    """The page we hand out — QR code on the booth, link in the follow-up DM."""
    ctx = context()
    subject, body = render_draft(ctx)
    html = env.get_template("page.html.j2").render(
        draft_subject=subject, draft_body=body, **ctx
    )
    return HTMLResponse(html)


@app.get("/draft", response_class=PlainTextResponse)
def draft():
    """Same draft as plain text — handy for checking wording without the page."""
    subject, body = render_draft(context())
    return f"To: {profile.email}\nSubject: {subject}\n\n{body}\n"


@app.get("/health")
def health():
    return {"ok": True, "contact_email": profile.email, "calendly": profile.calendly_url}
