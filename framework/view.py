from templater import render


class IndexTemplateView:
    def __call__(self, request):
        request['title'] = 'Главная'
        page = render('templates/index.html', object_list=request).encode('utf-8')
        return '200 OK', [page]


class AboutTemplateView:
    def __call__(self, request):
        request['title'] = 'О нас'
        page = render('templates/about.html', object_list=request).encode('utf-8')
        return '200 OK', [page]


class ContactsTemplateView:
    def __call__(self, request):
        request['title'] = 'Контакты'
        page = render('templates/contacts.html', object_list=request).encode('utf-8')
        return '200 OK', [page]


class BadReqTemplateView:
    def __call__(self, request):
        request['title'] = '404_page'
        page = render('templates/404.html', object_list=request).encode('utf-8')
        return '404 WHAT', [page]


