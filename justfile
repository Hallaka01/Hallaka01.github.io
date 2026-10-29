default:
    @just --list

setup:
    lefthook install

dev:
    python3 -m http.server 8767 --bind 127.0.0.1 --directory site

check:
    python3 scripts/check_site.py
    node --check site/scripts/main.js

test:
    python3 -m unittest discover -s tests -v
