# Maple demo

Password-protected prototype hosted on GitHub Pages.

- `src/maple.html` — the real site (plain source, **git-ignored**, never published)
- `index.html` — encrypted version that gets published; the browser decrypts it after the password is entered
- `gate_template.html` — the password screen
- `encrypt.py` — rebuilds `index.html` from the source

## Making changes

1. Edit `src/maple.html` (open it directly in a browser to preview).
2. Re-encrypt: `python3 encrypt.py` (asks for the password; needs `pip3 install cryptography` once).
3. Commit and push `index.html`.

To change the password, just run `encrypt.py` again with a new one.
