# NovaMesh AI deployment snapshot

This directory captures the current NovaMesh AI branding and deployment assets
that are already running on the netcup server as of 2026-03-26.

It exists to solve one problem: the live site currently depends on a mix of
runtime branding files, database content, and reverse-proxy rules that are not
part of upstream `new-api`. Keeping these assets here makes the current live
state reproducible and prevents them from being lost on the next upgrade.

## What is included

- `branding/`
  - Static landing page
  - Static guide page
  - Panel shell page used by `panel.model-port.xyz`
  - Brand marks, favicon assets, and empty-state illustration
  - Exported HTML content currently used for `HomePageContent` and `About`
- `api.model-port.xyz.Caddyfile`
  - Public API reverse-proxy example
- `panel.model-port.xyz.Caddyfile`
  - Customer portal reverse-proxy example
- `compose.example.yml`
  - Sanitized runtime compose layout matching the current server structure
- `runtime-options.template.json`
  - Base option values for `SystemName`, `Logo`, `Footer`, docs link, and top-up link
- `apply_runtime.py`
  - Seeds the SQLite `options` table with NovaMesh base settings plus exported `HomePageContent` and `About`
- `bootstrap.sh`
  - Copies branding assets and applies the runtime options in one step

## What is intentionally not committed

- Runtime secrets such as:
  - `SESSION_SECRET`
  - `CRYPTO_SECRET`
  - payment keys
  - webhook secrets
- Live database contents outside the exported branding HTML
- Generated user data under `/opt/new-api/data`

## Current live architecture

- Public API:
  - `https://api.model-port.xyz/v1`
- Customer portal:
  - `https://panel.model-port.xyz`
- Runtime service:
  - `new-api` bound to `127.0.0.1:3000`
- Redis:
  - local container, append-only enabled
- Reverse proxy:
  - Caddy terminates TLS and routes the two subdomains

## How these files map to the live server

- Live branding directory:
  - `/opt/new-api/branding`
- Live reverse-proxy files:
  - applied in Caddy on the server
- Live compose file:
  - `/opt/new-api/compose.yml`

## Restore checklist

1. Deploy `new-api` with a compose file based on `compose.example.yml`.
2. Copy everything under `branding/` to `/opt/new-api/branding`.
3. Apply the two Caddy site definitions and reload Caddy.
4. Reapply the exported `newapi-home-content.html` and
   `newapi-about-content.html` into the `HomePageContent` and `About` options.
5. Reconfigure any secrets and payment providers outside Git.

## Automated bootstrap

If the new machine already has:

- `new-api` running with SQLite
- a writable `data/one-api.db`
- Python 3 available

then you can restore the NovaMesh-facing runtime layer with:

```bash
cd /path/to/new-api-lbw/deploy/novamesh
./bootstrap.sh /opt/new-api https://panel.example.com https://api.example.com/v1
```

This script will:

1. Copy the branding assets into `/opt/new-api/branding`
2. Upsert the base `options` rows into the SQLite database
3. Render domain-specific links into the stored HTML content

It does not touch secrets, users, channels, tokens, or payment credentials.

## Notes

- These assets document the live customized state.
- They do not yet replace the upstream frontend implementation.
- The next step should be migrating the stable customizations into source code
  where possible, and leaving only brand content and deployment examples here.
