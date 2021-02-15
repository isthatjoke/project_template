import os

from jinja2 import Template, Environment, FileSystemLoader


def render(template_name, **kwargs):
    # file_path = os.path.join(folder, template_name)
    with open(template_name, encoding='utf-8') as f:
        template = f.read()
        template = Environment(loader=FileSystemLoader("templates/")).from_string(template)
        # template = Template(f.read())
    return template.render(**kwargs)


