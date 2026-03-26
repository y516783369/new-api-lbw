#!/usr/bin/env python3
import argparse
import json
import sqlite3
from pathlib import Path


def render_placeholders(content: str, panel_base: str, api_base: str) -> str:
    return (
        content.replace("https://panel.model-port.xyz", panel_base)
        .replace("https://api.model-port.xyz/v1", api_base)
        .replace("{{PANEL_BASE}}", panel_base)
        .replace("{{API_BASE}}", api_base)
    )


def upsert_option(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        """
        INSERT INTO options(key, value) VALUES(?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """,
        (key, value),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply NovaMesh runtime branding/options to a new-api SQLite DB."
    )
    parser.add_argument("--db", required=True, help="Path to one-api.db")
    parser.add_argument(
        "--branding-dir",
        default=str(Path(__file__).resolve().parent / "branding"),
        help="Path to the branding asset directory",
    )
    parser.add_argument(
        "--options-file",
        default=str(Path(__file__).resolve().parent / "runtime-options.template.json"),
        help="JSON file containing base runtime options",
    )
    parser.add_argument(
        "--panel-base",
        required=True,
        help="Portal base URL, e.g. https://panel.example.com",
    )
    parser.add_argument(
        "--api-base",
        required=True,
        help="API base URL including /v1, e.g. https://api.example.com/v1",
    )
    args = parser.parse_args()

    db_path = Path(args.db)
    branding_dir = Path(args.branding_dir)
    options_file = Path(args.options_file)

    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")
    if not branding_dir.exists():
        raise SystemExit(f"Branding directory not found: {branding_dir}")
    if not options_file.exists():
        raise SystemExit(f"Options file not found: {options_file}")

    with options_file.open("r", encoding="utf-8") as f:
        options = json.load(f)

    with (branding_dir / "newapi-home-content.html").open("r", encoding="utf-8") as f:
        home_content = render_placeholders(f.read(), args.panel_base, args.api_base)

    with (branding_dir / "newapi-about-content.html").open("r", encoding="utf-8") as f:
        about_content = render_placeholders(f.read(), args.panel_base, args.api_base)

    rendered_options = {
        key: render_placeholders(value, args.panel_base, args.api_base)
        for key, value in options.items()
    }
    rendered_options["HomePageContent"] = home_content
    rendered_options["About"] = about_content

    conn = sqlite3.connect(db_path)
    try:
        for key, value in rendered_options.items():
            upsert_option(conn, key, value)
        conn.commit()
    finally:
        conn.close()

    print(f"Applied {len(rendered_options)} runtime options into {db_path}")


if __name__ == "__main__":
    main()
