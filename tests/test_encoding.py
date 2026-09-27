from pathlib import Path

import pytest

from jev_ultrafast import demo

PAGES = {"/": "index.html", "/app.js": "app.js", "/style.css": "style.css", "/fixture.html": "fixture.html"}


@pytest.mark.parametrize("path", PAGES)
def test_static_assets_load_on_a_gbk_locale(monkeypatch, path):
    """Any read_text() left on the locale default decodes as GBK, as on Chinese Windows."""
    read_text = Path.read_text

    def gbk_default(self, encoding=None, errors=None):
        return read_text(self, encoding or "gbk", errors)

    monkeypatch.setattr(Path, "read_text", gbk_default)
    handler = demo.Handler.__new__(demo.Handler)
    handler.headers = {"Host": f"127.0.0.1:{demo.PORT}"}
    handler.path = path
    sent = {}
    handler.send = lambda status, body, mime="": sent.update(status=status)
    handler.do_GET()
    assert sent["status"] == 200
