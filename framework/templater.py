
from jinja2 import Template, Environment, FileSystemLoader


def render(template_name, **kwargs):
    # print(kwargs)
    with open(template_name, encoding='utf-8') as f:

        template = f.read()
        template = Environment(loader=FileSystemLoader("templates/")).from_string(template)
    return template.render(**kwargs)


