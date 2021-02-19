
import os
from framework.settings import BASE_DIR


def save_to_file(data):
    with open(os.path.join(BASE_DIR, 'data.txt'), encoding='utf-8') as file:
        file_data = file.read()

    with open(os.path.join(BASE_DIR,'data.txt'), 'w', encoding='utf-8') as file:
        data_to_file = file_data + '\n' + data
        file.write(data_to_file)

