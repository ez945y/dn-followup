"""Render the page to docs/index.html — that's what GitHub Pages serves.

The page has no server-side logic at request time (everything comes from
config.py, and the buttons are plain JS), so a static export behaves exactly
like the FastAPI version.

    python3 build.py
"""

from pathlib import Path

from app.config import BASE_DIR
from app.main import context, env, render_draft

OUT_DIR = BASE_DIR / "docs"


def build() -> Path:
    ctx = context()
    subject, body = render_draft(ctx)
    html = env.get_template("page.html.j2").render(
        draft_subject=subject, draft_body=body, **ctx
    )

    OUT_DIR.mkdir(exist_ok=True)
    index = OUT_DIR / "index.html"
    index.write_text(html, encoding="utf-8")
    # tell GitHub Pages not to run Jekyll over the output
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    return index


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
