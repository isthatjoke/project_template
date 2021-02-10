from view import IndexTemplateView, AboutTemplateView, ContactsTemplateView


urls = {
    '/': IndexTemplateView(),
    '/about': AboutTemplateView(),
    '/contacts': ContactsTemplateView(),
}

