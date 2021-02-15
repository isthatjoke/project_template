import quopri
from templater import render
from saver import save_to_file


def decode_value(val):
    val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
    val_decode_str = quopri.decodestring(val_b)
    return val_decode_str.decode('UTF-8')


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
        if request['method'] == 'POST':
            data = request['data']
            title = ''.join(data['title'])
            text = ''.join(data['text'])
            email = ''.join(data['email'])
            print(f'{title}, {text}, {email}')
            if title or text or email:
                save_to_file(f'{title}, {text}, {email}')
        return '200 OK', [page]


class BadReqTemplateView:
    def __call__(self, request):
        request['title'] = '404_page'
        page = render('templates/404.html', object_list=request).encode('utf-8')
        return '404 WHAT', [page]


