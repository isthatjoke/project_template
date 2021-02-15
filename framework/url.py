from view import ContactsTemplateView, IndexTemplateView, AboutTemplateView


urls = {
    '/': IndexTemplateView(),
    '/about': AboutTemplateView(),
    '/contacts': ContactsTemplateView(),
}

