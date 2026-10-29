"""HTTP smoke tests for the exact directory published by GitHub Pages."""
import functools
import http.server
import threading
import unittest
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

SITE = Path(__file__).resolve().parents[1] / 'site'


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))


class SiteSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = functools.partial(QuietHandler, directory=str(SITE))
        cls.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.origin = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def get(self, path):
        return urllib.request.urlopen(self.origin + path, timeout=5)

    def test_home_navigation_resolves_and_includes_real_projects(self):
        with self.get('/') as response:
            self.assertEqual(response.status, 200)
            page = Page(response.read().decode('utf-8'))
        for destination in page.links:
            if destination.startswith('#'):
                self.assertIn(destination[1:], page.ids)
        self.assertIn('https://github.com/Hallaka01/ygo-scanner-showcase', page.links)
        self.assertIn('https://github.com/HSMWmobil', page.links)

    def test_styles_scripts_and_all_images_are_served(self):
        for path, content_type in (
            ('/styles/base.css', 'text/css'), ('/styles/components.css', 'text/css'),
            ('/styles/responsive.css', 'text/css'), ('/scripts/main.js', 'text/javascript'),
            ('/assets/neon-city.png', 'image/png'), ('/assets/collection.png', 'image/png'),
            ('/assets/scanner.png', 'image/png'), ('/assets/social-banner.png', 'image/png'),
        ):
            with self.subTest(path=path), self.get(path) as response:
                self.assertEqual(response.status, 200)
                self.assertIn(response.headers.get_content_type(), (content_type, 'application/javascript'))
                self.assertGreater(len(response.read()), 100)

    def test_404_page_has_a_way_home(self):
        with self.get('/404.html') as response:
            page = Page(response.read().decode('utf-8'))
        self.assertIn('/', page.links)

    def test_essential_content_does_not_require_javascript(self):
        with self.get('/') as response:
            html = response.read().decode('utf-8')
        self.assertIn("I'm Finn", html)
        self.assertIn('id="work"', html)
        self.assertIn('aria-controls="site-nav"', html)
        self.assertNotIn('<form', html)


if __name__ == '__main__':
    unittest.main()
