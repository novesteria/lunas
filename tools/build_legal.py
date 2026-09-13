#!/usr/bin/env python3
"""Build the Lunas legal pages: legal/<doc>.html plus legal/index.html (terms).

  python3 tools/build_legal.py

Eight documents (canvas LunasLegal). Each section opens with a plain-language
summary; the binding text comes from counsel and replaces the placeholder.
Until then every page carries the "Draft · pending legal review" tag.
"""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "legal"
COUNSEL = "Full text · to come from counsel (Oguz Law or CBC Law). Do not publish before review."

DOCS: dict[str, dict] = {
    "terms": {
        "title": "Terms of Service",
        "sections": [
            ("What Lunas is", "A code verification service. Core (21 checks) is free and open source; Full (75 checks) runs in a sandbox and is paid. We report what we found; we do not guarantee your software is correct."),
            ("Your account", "Google sign-in or an email link. You are responsible for what is scanned from your account. One person per account; teams use seats."),
            ("Plans, billing and renewal", "Pro $19 and Max $100 a month, Team seats $19 and $100 a month, billed monthly by Polar (merchant of record) until you cancel. Cancel any time; the plan ends at the end of the paid period."),
            ("Pay as you go", "A single Full scan is $7; five are $29 and expire 45 days after purchase. No badge, no scan on push, no priority."),
            ("Refunds", "14 days on the first payment of a plan. No refund on a started renewal or on used pay-as-you-go scans. EU consumers: you ask for immediate access at checkout and waive the withdrawal right for that period."),
            ("Fair use", "Quotas are per month and per account or team pool. Automated abuse, scanning code you have no right to, or reselling results ends the account."),
            ("Your code and your data", "Code is deleted when a scan ends. Reports, badges and metadata stay until you delete them. We never train on your code. Payment data lives with Polar."),
            ("Availability and support", "Best effort, no uptime guarantee at launch. Support by email, answered within a day."),
            ("Liability", "Lunas is a tool, not a certification. Our liability is capped at what you paid in the last 12 months."),
            ("Changes and contact", "We announce changes 14 days ahead by email. Novesteria, Inc., Delaware. legal@novesteria.com"),
        ],
    },
    "privacy": {
        "title": "Privacy Policy",
        "sections": [
            ("Who we are", "Novesteria, Inc., Delaware, runs Lunas. Polar handles payments as merchant of record and is a separate controller for payment data."),
            ("What we collect", "Your Google account email and name, or the email you sign in with. Project names, repository names, commit references, scan results and reports. Server logs with IP address and browser type."),
            ("Your code", "Code is read into an isolated sandbox for the length of a scan and destroyed with the sandbox. It is never stored, never used to train anything, and never shown to anyone at Novesteria."),
            ("Why we use it", "To run scans, keep your reports, render badges and public pages, bill plans, send the emails the service needs, and keep the service safe."),
            ("Who else sees it", "Sandboxes run on E2B. Emails go through Resend. Payments through Polar. GitHub, when you connect a repository. Each receives only what its job needs."),
            ("How long we keep it", "Reports and scan history until you delete them or your account. Accounts deleted on request are purged after 30 days. Logs are kept for 30 days."),
            ("Your rights", "Export or delete your data from Settings › Account at any time. EU and UK residents have the GDPR rights; residents of Türkiye have the KVKK rights listed in the KVKK notice."),
            ("Contact", "privacy@novesteria.com. Changes are announced 14 days ahead by email."),
        ],
    },
    "refund": {
        "title": "Refund policy",
        "sections": [
            ("Plans", "A 14-day refund on the first payment of a plan, in full, no questions. Ask by email or from Settings › Billing."),
            ("Renewals", "A renewal that has started is not refunded. Cancel before the renewal date; the plan runs to the end of the paid period and does not renew."),
            ("Pay as you go", "A single scan or a pack of five is refunded only if no scan from it has run. Used scans are not refunded. Packs expire 45 days after purchase."),
            ("Team seats", "Seats are prorated when added mid-period. Removing a seat takes effect at the end of the period; it is not refunded."),
            ("EU and UK consumers", "You ask for immediate access at checkout and acknowledge that the 14-day withdrawal right lapses for the period already used. The 14-day refund above still applies to the first payment."),
            ("How refunds are paid", "Polar, the merchant of record, returns the money to the original payment method, usually within 5 to 10 business days."),
            ("Contact", "billing@novesteria.com"),
        ],
    },
    "cookies": {
        "title": "Cookie notice",
        "sections": [
            ("What we set", "One session cookie that keeps you signed in, one short-lived cookie that remembers where to send you after sign-in, and one that remembers which workspace you were in. All first-party."),
            ("What we do not set", "No advertising cookies, no cross-site tracking, no third-party analytics scripts on the site or in the app."),
            ("Third parties", "Google sets its own cookies during sign-in. Polar sets its own during checkout. Their notices apply on their pages."),
            ("Your choices", "Blocking cookies in the browser keeps the public site working and prevents signing in to the app."),
        ],
    },
    "security": {
        "title": "Security",
        "sections": [
            ("Sandboxes", "Every scan runs in a fresh, isolated sandbox with no access to other scans or to Novesteria systems. The sandbox is destroyed when the scan ends, code included."),
            ("What the app can reach", "A connected GitHub repository is read at one commit and one check line is written back. The app never pushes, never opens pull requests, never reads other repositories."),
            ("Accounts", "Google sign-in or a one-time email link. No passwords are stored. API tokens are shown once and stored hashed; rotate or revoke them from Settings › Connections."),
            ("Data in transit and at rest", "TLS everywhere. Reports and metadata live in a managed database with encrypted storage and daily backups."),
            ("Payments", "Card data never touches Novesteria. Polar, the merchant of record, processes payments and holds card details."),
            ("Reporting a vulnerability", "security@novesteria.com. We answer within two business days and credit reporters who want it. Please do not run scans against systems you do not own."),
        ],
    },
    "pre-information": {
        "title": "Pre-information form · Türkiye",
        "intro": "Required by the Turkish Regulation on Distance Contracts before a consumer in Türkiye buys online. Shown at checkout and kept here.",
        "sections": [
            ("Seller and service provider", "Seller of record: Polar Software Inc. (merchant of record). Service provider: Novesteria, Inc., Delaware, USA. Contact: legal@novesteria.com."),
            ("The service", "Lunas code verification: Pro or Max monthly plan, Team seats, or pay-as-you-go Full scans. Digital service, delivered immediately in the account."),
            ("Price and payment", "Prices in USD as shown at checkout, VAT shown as a separate line where it applies. Paid by card through Polar. Monthly plans renew until cancelled."),
            ("Delivery", "Access starts as soon as payment is confirmed. No physical delivery."),
            ("Right of withdrawal", "Consumers may withdraw within 14 days. By asking for immediate access at checkout, the consumer accepts that the withdrawal right does not cover the period already used. The 14-day refund on the first plan payment applies regardless."),
            ("Complaints", "Consumer arbitration committees and consumer courts in Türkiye are competent within the monetary limits set each year."),
        ],
    },
    "distance-sales": {
        "title": "Distance sales agreement · Türkiye",
        "intro": "The contract formed when a consumer in Türkiye buys a Lunas plan or scans online. Polar is the seller of record; Novesteria provides the service.",
        "sections": [
            ("Parties", "The consumer named at checkout; Polar Software Inc. as seller of record; Novesteria, Inc. as the provider of the Lunas service."),
            ("Subject", "Sale of a digital service: a Lunas plan, Team seats, or pay-as-you-go Full scans, as selected at checkout."),
            ("Price, payment and renewal", "The price shown at checkout in USD, VAT as a separate line where it applies. Monthly plans renew each period until cancelled from Settings › Plan."),
            ("Delivery and performance", "The service is available in the account as soon as payment is confirmed. Scans are run on request within the quota of the plan or pack."),
            ("Right of withdrawal", "14 days from the contract date, except for the period in which the service was used with the consumer's express request for immediate access."),
            ("Consumer's obligations", "To scan only code the consumer has the right to scan and to keep account access to one person."),
            ("Disputes", "Consumer arbitration committees and consumer courts at the consumer's place of residence in Türkiye."),
        ],
    },
    "kvkk": {
        "title": "KVKK notice · Türkiye",
        "intro": "The notice required by Law No. 6698 on the Protection of Personal Data for people in Türkiye whose data Lunas processes.",
        "sections": [
            ("Data controller", "Novesteria, Inc., Delaware, USA. Contact: privacy@novesteria.com."),
            ("Data processed", "Identity and contact data (name, email), account and usage data (projects, scans, reports, tokens), transaction data (invoices; card details stay with Polar), and log data (IP address, browser)."),
            ("Purpose and legal basis", "Performing the service contract, meeting legal obligations (invoicing, tax), and the legitimate interest of keeping the service secure."),
            ("Transfers", "Data is processed on servers outside Türkiye (USA and EU) by Novesteria and its processors: E2B (sandboxes), Resend (email), Polar (payments), GitHub (when connected)."),
            ("Retention", "For the life of the account plus 30 days after deletion; invoices for the period required by tax law."),
            ("Your rights under Article 11", "To learn whether your data is processed, to request correction or deletion, to object to automated results, and to claim damages. Requests: privacy@novesteria.com, answered within 30 days."),
        ],
    },
}
ORDER = ["terms", "privacy", "refund", "cookies", "security", "pre-information", "distance-sales", "kvkk"]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#FFFFFF">
<title>{title} · Lunas</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="canonical" href="https://aegis.novesteria.com/legal/{slug}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/lunas-site.css">
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="moon" viewBox="0 0 100 100"><g transform="translate(50 50) rotate(200) translate(-50 -50)"><path d="M68.99 12.54 A42 42 0 1 0 68.99 87.46 A50 50 0 0 1 68.99 12.54 Z" fill="currentColor"/></g></symbol>
</defs></svg>

<header class="site"><div class="wrap nav">
  <a class="brand" href="/"><svg width="26" height="26" style="color:#2A3B31"><use href="#moon"/></svg><span><b>Lunas</b><span class="by">BY NOVESTERIA</span></span></a>
  <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><svg width="18" height="18" viewBox="0 0 18 18"><path d="M2 4.5h14M2 9h14M2 13.5h14" stroke="#20261F" stroke-width="1.6" stroke-linecap="round"/></svg></button>
  <nav class="nav-links"><a href="/how">How it works</a><a href="/docs">Docs</a><a href="/verified">Verification pages</a><a href="/pricing">Pricing</a><a class="btn primary sm" href="/app/login?next=/app/new">Run a scan</a></nav>
</div></header>

<main class="wrap legal">
  <nav class="legal-nav" aria-label="Legal documents">
    <span class="kicker" style="padding:14px 12px 6px">Legal</span>
{navlinks}
    <p class="hint">Türkiye pages exist because Turkish consumer law asks for them when a consumer in Türkiye buys online. Polar is the seller of record; these documents name Polar and Novesteria.</p>
  </nav>
  <article>
    <h1>{title}</h1>
    <div class="draft"><span class="tag">Draft · pending legal review</span><span>Effective date to be set on publication · Version 0.1</span></div>
    <p class="note" style="margin-bottom:26px">{intro}</p>
{sections}
  </article>
</main>

<footer class="site"><div class="wrap"><span>© 2026 Novesteria</span><nav><a href="/pricing">Pricing</a><a href="/docs">Docs</a><a href="/verified">Verification pages</a><a href="/legal/security">Security</a><a href="/legal/privacy">Privacy</a><a href="/legal/terms">Terms</a><a href="/legal/refund">Refund policy</a></nav></div></footer>
<script src="/lunas-site.js" defer></script>
</body>
</html>
"""
DEFAULT_INTRO = "Each section opens with a plain-language summary. The summary is not the contract; the binding text is the full text under it, written and checked by our lawyers. Until that text is published, this page is not live."


def build(slug: str) -> str:
    d = DOCS[slug]
    e = html.escape
    nav = "\n".join('    <a%s href="/legal/%s">%s</a>' % (' class="on"' if s == slug else "", s, e(DOCS[s]["title"])) for s in ORDER)
    secs = "\n".join(
        f'    <section class="sec"><b>{i}. {e(t)}</b><span class="kicker">Summary</span><p>{e(s)}</p><span class="lawyer">{e(COUNSEL)}</span></section>'
        for i, (t, s) in enumerate(d["sections"], 1)
    )
    desc = d["sections"][0][1]
    return HEAD.format(title=e(d["title"]), desc=e(desc), slug=slug, navlinks=nav, intro=e(d.get("intro", DEFAULT_INTRO)), sections=secs)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for slug in ORDER:
        out = OUT / f"{slug}.html"
        out.write_text(build(slug), encoding="utf-8")
        print("built", out.relative_to(ROOT))
    (OUT / "index.html").write_text(build("terms"), encoding="utf-8")
    print("built legal/index.html (terms)")


if __name__ == "__main__":
    main()
