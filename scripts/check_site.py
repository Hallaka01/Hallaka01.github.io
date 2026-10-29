#!/usr/bin/env python3
"""Validate the static publishing boundary, HTML references, and source files."""
import re
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.references = []
        self.images = []
        self.language = None
        self.feed(text)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == 'html':
            self.language = attrs.get('lang')
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        for attr in ('src', 'href'):
            if attrs.get(attr):
                self.references.append(attrs[attr])
        if tag == 'img':
            self.images.append(attrs)


def check():
    errors = []
    for name in ('index.html', '404.html', 'assets/neon-city.png',
                 'assets/social-banner.png', 'assets/collection.png', 'assets/scanner.png'):
        if not (SITE / name).is_file():
            errors.append('Missing publishing file: ' + name)
    for path in SITE.rglob('*'):
        if not path.is_file():
            continue
        relative = path.relative_to(SITE)
        if path.is_symlink() or path.suffix in ('.key', '.p12', '.sqlite', '.store') or path.name.startswith('.env'):
            errors.append('Unexpected publishing file: ' + str(relative))
        if path.stat().st_size > 8_000_000:
            errors.append('Oversized asset: ' + str(relative))
        if path.suffix == '.png':
            raw = path.read_bytes()
            if raw[:8] != b'\x89PNG\r\n\x1a\n':
                errors.append('Invalid PNG: ' + str(relative))
            elif path.name == 'neon-city.png':
                width, height = struct.unpack('>II', raw[16:24])
                if width < 1500 or not 1.6 < width / height < 1.9:
                    errors.append('Unexpected city background size')
            continue
        text = path.read_text(encoding='utf-8')
        if not text.endswith('\n') or any(line.rstrip() != line for line in text.splitlines()):
            errors.append('Whitespace or missing final newline: ' + str(relative))
        if re.search(r'/(?:Users|Volumes|private/tmp)/|gh[pousr]_[A-Za-z0-9]{30,}', text):
            errors.append('Machine path or possible credential: ' + str(relative))
        if path.suffix == '.html':
            document = Document(text)
            if document.language != 'en' or len(document.ids) != len(set(document.ids)):
                errors.append('Invalid language or duplicate IDs: ' + str(relative))
            for picture in document.images:
                if not picture.get('alt') or not picture.get('width') or not picture.get('height'):
                    errors.append('Image lacks an alternative or dimensions: ' + str(relative))
            for reference in document.references:
                url = urlsplit(reference)
                if url.scheme or url.netloc:
                    if url.scheme != 'https':
                        errors.append('Unexpected external reference: ' + reference)
                    continue
                if not url.path:
                    if url.fragment and url.fragment not in document.ids:
                        errors.append('Broken anchor: ' + reference)
                    continue
                target = ((SITE / unquote(url.path.lstrip('/'))) if url.path.startswith('/')
                          else (path.parent / unquote(url.path))).resolve()
                if not target.is_relative_to(SITE) or not target.exists():
                    errors.append('Broken local reference: ' + reference)
        if path.suffix == '.css':
            for reference in re.findall(r'url\(["\']?([^"\')]+)', text):
                if not (path.parent / reference).resolve().is_file():
                    errors.append('Broken CSS image: ' + reference)
    return errors


if __name__ == '__main__':
    problems = check()
    if problems:
        print('\n'.join(problems), file=sys.stderr)
        sys.exit(1)
    print('Static site checks passed: publishing files, links, anchors, images, and source hygiene.')
