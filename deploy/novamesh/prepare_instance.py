#!/usr/bin/env python3
import argparse
import secrets
from pathlib import Path


def render_template(content: str, replacements: dict[str, str]) -> str:
    rendered = content
    for key, value in replacements.items():
        rendered = rendered.replace(key, value)
    return rendered


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare NovaMesh compose and Caddy files for a new host."
    )
    parser.add_argument(
        "--new-api-root",
        required=True,
        help="Target runtime root, e.g. /opt/new-api",
    )
    parser.add_argument(
        "--panel-domain",
        required=True,
        help="Portal hostname, e.g. panel.example.com",
    )
    parser.add_argument(
        "--api-domain",
        required=True,
        help="API hostname, e.g. api.example.com",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to write generated compose and Caddy files into",
    )
    parser.add_argument(
        "--force-compose",
        action="store_true",
        help="Overwrite compose.yml if it already exists in output-dir",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    compose_template = (script_dir / "compose.example.yml").read_text(encoding="utf-8")
    compose_output = output_dir / "compose.yml"
    if compose_output.exists() and not args.force_compose:
        raise SystemExit(
            f"{compose_output} already exists. Use --force-compose to overwrite it."
        )

    session_secret = secrets.token_urlsafe(48)
    crypto_secret = secrets.token_urlsafe(48)
    rendered_compose = (
        compose_template.replace("SESSION_SECRET: CHANGE_ME", f"SESSION_SECRET: {session_secret}")
        .replace("CRYPTO_SECRET: CHANGE_ME", f"CRYPTO_SECRET: {crypto_secret}")
    )
    compose_output.write_text(rendered_compose, encoding="utf-8", newline="\n")

    replacements = {
        "{{NEW_API_ROOT}}": args.new_api_root.rstrip("/"),
        "{{PANEL_DOMAIN}}": args.panel_domain,
        "{{API_DOMAIN}}": args.api_domain,
    }
    panel_template = (script_dir / "panel.Caddyfile.template").read_text(encoding="utf-8")
    api_template = (script_dir / "api.Caddyfile.template").read_text(encoding="utf-8")
    (output_dir / f"{args.panel_domain}.Caddyfile").write_text(
        render_template(panel_template, replacements),
        encoding="utf-8",
        newline="\n",
    )
    (output_dir / f"{args.api_domain}.Caddyfile").write_text(
        render_template(api_template, replacements),
        encoding="utf-8",
        newline="\n",
    )

    print(f"Wrote {compose_output}")
    print(f"Wrote {output_dir / f'{args.panel_domain}.Caddyfile'}")
    print(f"Wrote {output_dir / f'{args.api_domain}.Caddyfile'}")
    print("Generated fresh SESSION_SECRET and CRYPTO_SECRET in compose.yml")


if __name__ == "__main__":
    main()
