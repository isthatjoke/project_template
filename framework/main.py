
import re
import urllib
from url import urls
from view import BadReqTemplateView


def parse_input_data(data: str):
    parsed_data = urllib.parse.parse_qs(data)
    return parsed_data


def secret_front(request):
    request['secret'] = 'some secret'


def about_front(request):
    request['key'] = 'key'


def contacts_front(request):
    request['phone'] = '+7-999-123-45-67'
    request['address'] = 'Москва, Лениградское ш. 16А'


fronts = {'secret_front': secret_front, 'other_front': about_front, 'contacts': contacts_front}


class Application:

    def __init__(self, urls, fronts):
        self.urls = urls
        self.request = {}
        self.fronts = fronts

    def __call__(self, environ, start_response):
        self.path = environ['PATH_INFO']
        if re.findall(r'\w+\/$', self.path):
            self.path = self.path[:-1]
        if self.path in self.urls:
            view = self.urls[self.path]
        else:
            view = BadReqTemplateView()
        method = environ['REQUEST_METHOD']
        query_string = environ['QUERY_STRING']
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        request_params = parse_input_data(query_string)
        self.request['method'] = method
        self.request['data'] = data
        self.request['request_params'] = request_params
        print(request_params)
        if self.path == '/contacts':
            self.fronts['contacts'](self.request)
        code, body = view(self.request)
        start_response(code, [('Content-Type', 'text/html')])
        return body

    def parse_wsgi_input_data(self, data: bytes):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = parse_input_data(data_str)
        return result

    def get_wsgi_input_data(self, environ):
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data


application = Application(urls, fronts)




