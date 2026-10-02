"""Check one self-contained HTML artifact. Browser behavior still needs testing."""
from html.parser import HTMLParser
from pathlib import Path
import argparse
import re
import sys


class ArtifactParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.errors = []
        self.ids = set()
        self.fragment_links = []
        self.title = ''
        self.in_title = False
        self.styles = []
        self.in_style = False
        self.lang = None
        self.viewport = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        identifier = attributes.get('id')
        if identifier:
            if identifier in self.ids:
                self.errors.append('duplicate element id: ' + identifier)
            self.ids.add(identifier)
        if tag == 'html':
            self.lang = attributes.get('lang')
        if tag == 'meta' and attributes.get('name', '').lower() == 'viewport':
            self.viewport = bool(attributes.get('content'))
        self.in_title = self.in_title or tag == 'title'
        self.in_style = self.in_style or tag == 'style'
        if tag in ('iframe', 'frame', 'object', 'embed'):
            self.errors.append('embedded document requires manual review: ' + tag)
        for key in ('src', 'srcset', 'poster'):
            if attributes.get(key) and not attributes[key].startswith('data:'):
                self.errors.append(f'non-embedded {tag}[{key}]')
        if tag in ('link', 'image', 'use'):
            for key in ('href', 'xlink:href'):
                value = attributes.get(key, '')
                if value and not value.startswith(('data:', '#')):
                    self.errors.append(f'non-embedded {tag}[{key}]')
        if tag == 'a' and attributes.get('href', '').startswith('#'):
            self.fragment_links.append(attributes['href'][1:])
        if attributes.get('style'):
            self.styles.append(attributes['style'])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'style':
            self.in_style = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_style:
            self.styles.append(data)


def check(source):
    parser = ArtifactParser()
    parser.feed(source)
    if not source.lstrip().lower().startswith('<!doctype html>'):
        parser.errors.append('missing HTML doctype')
    if not parser.lang:
        parser.errors.append('missing document language')
    if not parser.title.strip():
        parser.errors.append('missing title')
    if not parser.viewport:
        parser.errors.append('missing viewport')
    for fragment in parser.fragment_links:
        if fragment and fragment not in parser.ids:
            parser.errors.append('broken source/fragment link: #' + fragment)
    css = '\n'.join(parser.styles)
    if re.search(r'@import\b', css, re.I):
        parser.errors.append('CSS import is not self-contained')
    for url in re.findall(r'url\(\s*([^)]*)\)', css, re.I):
        if not url.strip(' \t\r\n\'"').startswith(('data:', '#')):
            parser.errors.append('CSS URL is not embedded')
    return parser.errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path)
    args = parser.parse_args()
    errors = check(args.html.read_text(encoding='utf-8'))
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print('HTML static check: PASS; browser, dynamic requests and evidence still require review')
    return 0


if __name__ == '__main__':
    sys.exit(main())
