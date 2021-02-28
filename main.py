import quopri
from framework.core import Application, DebugApplication, MockApplication
from framework.templater import render
from framework.saver import save_to_file
from models import WebInterface
from framework.log import Logger


def secret_front(request):
    request['secret'] = 'some secret'


def about_front(request):
    request['key'] = 'key'


def contacts_front(request):
    request['phone'] = '+7-999-123-45-67'
    request['address'] = 'Москва, Лениградское ш. 16А'


fronts = {'secret_front': secret_front, 'other_front': about_front, 'contacts': contacts_front}

# app = Application(fronts)
app = DebugApplication(fronts)
# app = MockApplication(fronts)
web = WebInterface()
logger = Logger('main')


def decode_value(val):
    val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
    val_decode_str = quopri.decodestring(val_b)
    return val_decode_str.decode('UTF-8')


@app.add_route('/')
def view_index(request):
    logger.log('view_index')
    request['title'] = 'Главная'
    print(request)
    return '200 OK', render('templates/index.html', object_list=request)


@app.add_route('/about')
def view_about(request):
    logger.log('view_about')
    request['title'] = 'О нас'
    return '200 OK', render('templates/about.html', object_list=request)


@app.add_route('/contacts')
def view_contacts(request):
    logger.log('view_contacts')
    request['title'] = 'Контакты'
    if request['method'] == 'POST':
        data = request['data']
        title = ''.join(data['title'])
        text = ''.join(data['text'])
        email = ''.join(data['email'])
        print(f'{title}, {text}, {email}')
        if title or text or email:
            save_to_file(f'{title}, {text}, {email}')
    return '200 OK', render('templates/contacts.html', object_list=request)


@app.add_route('/categories')
def view_create_category(request):
    logger.log('view_create_category')
    request['title'] = 'Категории'
    request['categories'] = web.categories
    if request['method'] == 'POST':
        data = request['data']
        try:
            name = data['name']
        except:
            return '400 BAD_REQUEST', render('templates/categories.html', object_list=request)
        new_category = web.create_category(name)
        web.categories.append(new_category)
        request['categories'] = web.categories
        return '201 CREATED', render('templates/categories.html', object_list=request)
    return '200 OK', render('templates/categories.html', object_list=request)


@app.add_route('/create_course')
def view_create_course(request):
    logger.log('view_create_course')
    request['title'] = 'Создать курс'
    request['categories'] = web.categories
    if request['method'] == 'POST':
        data = request['data']
        try:
            name = data['name']
        except:
            return '400 BAD_REQUEST', render('templates/categories.html', object_list=request)
        category_id = data.get('category_id')
        if category_id:
            category = web.find_category_by_id(int(category_id[0]))
            course = web.create_course('record', name, category)
            web.courses.append(course)
        request['categories'] = web.categories
    return '200 OK', render('templates/create_course.html', object_list=request)


@app.add_route('/courses')
def view_list_courses(request):
    logger.log('view_list_courses')
    request['title'] = 'Курсы'
    request['courses'] = web.courses
    return '200 OK', render('templates/list_course.html', object_list=request)


