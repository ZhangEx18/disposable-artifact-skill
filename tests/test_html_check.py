import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('check_html', Path(__file__).resolve().parents[1] / 'scripts/check_html.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

HEADER = '<!doctype html><html lang="zh-CN"><head><title>Example</title><meta name="viewport" content="width=device-width"></head><body>'


class ArtifactCheckTests(unittest.TestCase):
    def test_offline_resources_and_external_evidence_links(self):
        html = HEADER + '<style>.x{background:url(data:image/svg+xml;base64,AA)}</style><a href="https://example.com/source">证据</a><a href="#e1">详情</a><p id="e1">来源</p></body></html>'
        self.assertEqual(checker.check(html), [])

    def test_rejects_runtime_dependencies(self):
        for markup in ('<script src="https://example.com/chart.js"></script>', '<img src="photo.png">', '<style>@import "theme.css";</style>', '<style>.x{background:url(bg.svg)}</style>', '<iframe srcdoc="text"></iframe>'):
            with self.subTest(markup=markup):
                self.assertTrue(checker.check(HEADER + markup + '</body></html>'))

    def test_evidence_targets_are_unambiguous(self):
        for markup in ('<a href="#missing">source</a>', '<p id="same"></p><p id="same"></p>'):
            with self.subTest(markup=markup):
                self.assertTrue(checker.check(HEADER + markup + '</body></html>'))


if __name__ == '__main__':
    unittest.main()
