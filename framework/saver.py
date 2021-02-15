
def save_to_file(data):
    with open('data.txt', encoding='utf-8') as file:
        file_data = file.read()

    with open('data.txt', 'w', encoding='utf-8') as file:
        data_to_file = file_data + '\n' + data
        file.write(data_to_file)

