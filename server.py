import os
import os.path
import re
import urllib
import urlparse

try:
    import json
except ImportError:
    import simplejson as json

import BaseHTTPServer
import SimpleHTTPServer

CGI_BIN = '/cgi-bin/'
PAGES = '/pages/'
JSON_CONTENT_TYPE = 'application/json'

DATA = {
    'MySpace': {
        'MyPage': {
            'labels': ('mine', 'important',),
            'content': 'My page content',
        },
        'MyOtherPage': {
            'labels': ('mine', 'private',),
            'content': 'My other page content',
        },
        'YourPage': {
            'labels': ('your', 'shared',),
            'content': 'Your page content',
        },
        'Home': {
            'labels': ('home', 'important',),
            'content': '<h1>Home</h1>Home page content',
        },
    },
    'YourSpace': {
        'Home': {
            'labels': ('home',),
            'content': 'Home',
        },
    },
    'OurSpace': {
        'Home': {
            'labels': ('home',),
            'content': 'Home',
        },
    },
}

LABELS_Q_RE = re.compile('q\[\d+\]')

class LFSHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith(CGI_BIN):
            return self._handle_cgi()

        if self.path.startswith(PAGES):
            return self._handle_page()

        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def _handle_cgi(self):
        command, _ = urllib.splitquery(self.path[len(CGI_BIN):])

        fun = getattr(self, '_handle_%s' % command, None)
        if not fun:
            self.send_error(404, 'Not implemented')
            return

        data = fun()

        self._write_data(data)

    def _write_data(self, data):
        self.send_response(200)
        self.send_header('Content-Type', JSON_CONTENT_TYPE)
        self.send_header('Content-Length', len(data))
        self.end_headers()

        self.wfile.write(data)

    def _handle_listSpaces(self):
        return json.dumps(tuple(DATA.iterkeys()))

    def _handle_completion(self):
        request = urlparse.urlparse(self.path)

        query = urlparse.parse_qs(request.query)

        space = query['space'][0]
        type_ = query['type'][0]
        try:
            term = query['term'][0]
        except KeyError:
            return '[]'

        space_ = DATA[space]

        if type_ == 'title':
            print term
            titles = tuple(
                title for title in space_.iterkeys()
                if term.lower() in title.lower())
            return json.dumps(titles)
        elif type_ == 'labels':
            labels = set(label
                for page in space_.itervalues()
                for label in page['labels'])
            return json.dumps(tuple(
                label for label in labels if term in label.lower()))
        else:
            raise NotImplementedError

    def _handle_search(self):
        # This returns all pages, no actual filtering is done

        request = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(request.query)

        space = query['space'][0]
        type_ = query['type'][0]

        pages = DATA[space]

        if type_ == 'labels':
            labels = set()

            for key, value in query.iteritems():
                if LABELS_Q_RE.match(key):
                    labels.add(value[0])

            matches = tuple(name for name, data in pages.iteritems()
                if all(label in data['labels'] for label in labels))
        elif type_ == 'fulltext':
            term = query['q'][0]
            matches = tuple(name for name, data in pages.iteritems()
                if term.lower() in data['content'].lower())
        else:
            raise NotImplementedError

        data = tuple((space, page) for page in matches)

        return json.dumps(data)


    def _handle_page(self):
        request = urlparse.urlparse(self.path)
        parts = request.path.split('/')
        assert parts[0] == ''
        assert parts[1] == PAGES.replace('/', '')

        space, page = parts[2:]

        try:
            page = DATA[space][page]
        except KeyError:
            self.send_error(404, 'Not found')
            return


        data = json.dumps(page)

        self._write_data(data)


def test(HandlerClass=LFSHTTPRequestHandler,
         ServerClass=BaseHTTPServer.HTTPServer):
    orig_dir = os.getcwd()

    os.chdir(os.path.join(os.path.dirname(__file__), 'htdocs'))

    try:
        BaseHTTPServer.test(HandlerClass, ServerClass)
    finally:
        os.chdir(orig_dir)

if __name__ == '__main__':
    test()
