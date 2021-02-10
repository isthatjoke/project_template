import re
from url import urls
from view import IndexTemplateView, AboutTemplateView, ContactsTemplateView, BadReqTemplateView


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
        self.request = ''
        self.fronts = fronts

    def __call__(self, environ, start_response):
        self.request = environ['PATH_INFO']
        if re.findall(r'\w+\/$', self.request):
            self.request = self.request[:-1]
        if self.request in self.urls:
            view = self.urls[self.request]
        else:
            view = BadReqTemplateView()
        request = {}
        if self.request == '/contacts':
            self.fronts['contacts'](request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return body


application = Application(urls, fronts)


