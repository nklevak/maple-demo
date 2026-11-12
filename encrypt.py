#!/usr/bin/env python3
"""
Encrypts src/maple.html into a password-protected index.html for GitHub Pages.

The plain source (src/) is git-ignored, so only the encrypted page is published.
Visitors enter the password and their browser decrypts the page locally
(PBKDF2-SHA256, 600k iterations -> AES-256-GCM, via the Web Crypto API).

Usage:
    pip3 install cryptography
    python3 encrypt.py                 # prompts for the password
    python3 encrypt.py "my-password"   # or pass it directly
"""
import base64, getpass, json, os, sys
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).parent
SRC, OUT, TEMPLATE = ROOT / "src" / "maple.html", ROOT / "index.html", ROOT / "gate_template.html"
ITERATIONS = 600_000

password = sys.argv[1] if len(sys.argv) > 1 else getpass.getpass("Password: ")
if not password:
    sys.exit("Password can't be empty.")

salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS).derive(password.encode())
ciphertext = AESGCM(key).encrypt(iv, SRC.read_bytes(), None)

b64 = lambda b: base64.b64encode(b).decode()
payload = json.dumps({"salt": b64(salt), "iv": b64(iv), "data": b64(ciphertext), "iter": ITERATIONS})
OUT.write_text(TEMPLATE.read_text().replace("__PAYLOAD__", payload))
print(f"Wrote {OUT.name} ({OUT.stat().st_size // 1024} KB). Commit and push it to update the site.")
