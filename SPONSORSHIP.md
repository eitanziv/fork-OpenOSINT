# OpenOSINT — Sponsorship Prospectus

OpenOSINT is an open-source AI-powered OSINT framework used by security researchers, OSINT practitioners, and developers evaluating intelligence APIs. This document describes the sponsorship tiers, the referral funnel, and current audience metrics.

## Audience

| Metric | Value |
|--------|-------|
| GitHub stars | 232 |
| GitHub forks | 51 |
| PyPI downloads / month | 3,119 |
| Website visits / month | <!-- TODO: from analytics --> |
| Content reach | <!-- TODO: TikTok 300k, dev.to, freeCodeCamp, LinkedIn --> |

## Referral funnel

OpenOSINT's documentation and interactive REPL link users directly to each provider's API sign-up or pricing page during the configuration step. The path from "install" to "paying customer" has four stages:

1. User installs OpenOSINT from PyPI or source.
2. User reads the Configuration table or tool documentation.
3. Links route them to the provider's sign-up or pricing page.
4. User sets an API key and activates the integration.

**Featured Integration** sponsors are named as the recommended provider for their category, appearing in the badge row, the Integrations table, and the tool-specific documentation — maximizing visibility at every stage of this funnel.

## Tiers

All tiers are **recurring placements** (monthly or annual). There are no one-off slots.

### Featured Integration

The highest-visibility tier. Your product becomes the named, recommended integration for a tool category.

**Placements included:**
- Dedicated "Featured Integration" block in the README `### Current sponsors` section (auto-rendered from `sponsors.json`)
- Badge in the README badge row
- "Featured (sponsored)" label in the Integrations table
- A live code integration (`openosint/<tool>` command and AI agent tool)
- One line in the CLI startup banner (`Featured integrations: <your name>`)
- `openosint sponsors` subcommand lists you with a link
- `/api/sponsors` web API endpoint exposes your entry to the Web UI footer
- Listed first for your category in all docs
- Listed in this document under **Current sponsors**

**Pricing (recurring):**

| Billing | Rate |
|---------|------|
| Monthly | <!-- set monthly rate --> Contact for rates |
| Annual  | <!-- set annual rate --> Contact for rates |

---

### Integration

A code integration exists (or will be built) and your logo/link appears in the sponsors grid.

**Placements included:**
- Logo + link in the README sponsors grid (auto-rendered from `sponsors.json`)
- A live code integration (`openosint/<tool>` command)
- `openosint sponsors` subcommand lists you with a link
- `/api/sponsors` web API endpoint exposes your entry to the Web UI
- Listed in this document under **Current sponsors**

**Pricing (recurring):**

| Billing | Rate |
|---------|------|
| Monthly | <!-- set monthly rate --> Contact for rates |
| Annual  | <!-- set annual rate --> Contact for rates |

---

### Supporter

Logo and link in the README sponsors grid — no code integration required.

**Placements included:**
- Logo + link in the README sponsors grid (auto-rendered from `sponsors.json`)
- `openosint sponsors` subcommand lists you with a link
- Listed in this document under **Current sponsors**

**Pricing (recurring):**

| Billing | Rate |
|---------|------|
| Monthly | <!-- set monthly rate --> Contact for rates |

---

## How to add or update a sponsor (maintainer guide)

All sponsor data lives in [`sponsors.json`](sponsors.json) at the repo root.  
Adding, updating, or removing a sponsor is a **one-file change**.

Add an entry to `sponsors.json`:

```json
{
  "name": "Acme Corp",
  "tagline": "Short description of what your product does",
  "url": "https://acme.example.com/?utm_source=openosint",
  "logo": "https://img.shields.io/badge/Acme-sponsored-blue?style=flat-square",
  "tier": "featured",
  "tool": "search_acme",
  "category": "Your Category"
}
```

Then regenerate the README block:

```bash
python scripts/render_sponsors.py
```

That's it. CLI banner, Web UI, and `openosint sponsors` update automatically at runtime.

## Current sponsors

**[IP2Location.io](https://www.ip2location.io)** — Featured Integration (enhanced IP intelligence category)

## Contact

- Email: [openosint@yahoo.com](mailto:openosint@yahoo.com?subject=OpenOSINT%20Sponsorship%20Inquiry)
- GitHub: [open an issue](https://github.com/OpenOSINT/OpenOSINT/issues)
- Website: [openosint.tech/#sponsors](https://openosint.tech/#sponsors)

---

*OpenOSINT is for authorized security research only. See [DISCLAIMER.md](DISCLAIMER.md).*
