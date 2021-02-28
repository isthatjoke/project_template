import re
import urllib
# from main import BadReqTemplateView
from framework.templater import render


def view_404(request):
    request['title'] = '404_page'
    page = render('templates/404.html', object_list=request)
    return '404 WHAT', page


class Application:

    def __init__(self, fronts):
        self.urls = {}
        self.request = {}
        self.fronts = fronts

    def __call__(self, environ, start_response):

        self.path = environ['PATH_INFO']
        if re.findall(r'\w+\/$', self.path):
            self.path = self.path[:-1]
        if self.path in self.urls:
            view = self.urls[self.path]
        else:
            view = view_404
        method = environ['REQUEST_METHOD']
        query_string = environ['QUERY_STRING']
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        request_params = self.parse_input_data(query_string)
        self.request['method'] = method
        self.request['data'] = data
        self.request['request_params'] = request_params

        if self.path == '/contacts':
            self.fronts['contacts'](self.request)
        code, body = view(self.request)

        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    def add_route(self, url):
        def inner(view):
            self.urls[url] = view
        return inner

    def parse_input_data(self, data: str):
        parsed_data = urllib.parse.parse_qs(data)
        return parsed_data

    def parse_wsgi_input_data(self, data: bytes):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_wsgi_input_data(self, environ):
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data


class DebugApplication(Application):

    def __init__(self, front_controllers):
        self.app = Application(front_controllers)
        super().__init__(front_controllers)

    def __call__(self, env, start_response):
        # print('DEBUG MODE')
        # print(env)
        return self.app(env, start_response)

    # def add_route(self, url):
    #     def inner(view):
    #         self.urlpatterns[url] = view
    #         self.application.urlpatterns[url] = view
    #
    #     return inner


class MockApplication(Application):

    def __init__(self, front_controllers):
        self.app = Application(front_controllers)
        super().__init__(front_controllers)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Mock']