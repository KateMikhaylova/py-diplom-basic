import requests
from progress.bar import IncrementalBar
import json
import time


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def check_files(self, folder_name, file_name):
        URL = 'https://cloud-api.yandex.net:443/v1/disk/resources/files'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        response = requests.get(URL, headers=headers)
        if response.status_code == 401:
            return 'Error'
        file_list = []
        for element in response.json()['items']:
            file_list.append((element['path'].split('/')[1:]))
        for element in file_list:
            if not folder_name:
                if file_name == element[0]:
                    return True
            if folder_name == element[0] and file_name == element[1]:
                return True

    def _create_folder(self, folder_name):
        URL = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        params = {"path": folder_name}
        response = requests.put(URL, headers=headers, params=params)
        if response.status_code == 201:
            print("Папка на ЯндексДиске успешно создана")
            return True
        if response.status_code == 409:
            return False
        response.raise_for_status()

    def _check_folder(self, folder_name):
        URL = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        params = {"path": folder_name}
        response = requests.get(URL, headers=headers, params=params)
        if response.status_code == 404:
            return False
        return True

    def choose_folder(self):
        while True:
            user_input = input('\nХотите сохранить файл в существующую папку? Если да, введите Y, если нет, введите N')
            user_input = user_input.upper()
            if user_input == 'Y':
                user_folder = input('\nВведите название существующей папки для сохранения файлов: ')
                if not self._check_folder(user_folder):
                    print('Такой папки не существует, для создания папки выберите N в пользовательском меню')
                    continue
            elif user_input == 'N':
                user_folder = input('\nВведите название новой папки для сохранения файлов: ')
                created = self._create_folder(user_folder)
                if not created:
                    print("Создание папки с таким именем не возможно")
                    continue
            else:
                print('Некорректный ввод')
                continue
            return user_folder

    def _upload_image(self, yadisk_path, image_url):
        URL = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        params = {"path": yadisk_path, "overwrite": "true", 'url': image_url}
        resp = requests.post(URL, headers=headers, params=params)
        if resp.status_code == 401:
            return False
        resp.raise_for_status()
        return True

    def upload_photos(self, photos_dictionary, folder_path):
        saved_list = []
        bar = IncrementalBar('Файлов загружено', max=len(photos_dictionary))
        for name, value in photos_dictionary.items():
            present = self.check_files(folder_path, f'{name}.jpg')
            if present == 'Error':
                print("Некорректный токен, проверьте введенные данные")
                return False
            if not present:
                uploaded = self._upload_image(f'{folder_path}/{name}.jpg', value[1])
            else:
                uploaded = self._upload_image(f'{folder_path}/{name}-{time.strftime("%Y%B%d%A%H_%M_%S")}.jpg', value[1])
                # Имя файла дополняется текущей датой, если в папке уже был файл с таким именем (например, после
                # сохранения фото предыдущего аккаунта, с таким же количеством лайков, как у текущего аккаунта)
            if not uploaded:
                print("Некорректный токен, проверьте введенные данные")
                return False
            saved_list.append({'file_name': f'{name}.jpg', 'size': value[0]})
            bar.next()
        bar.finish()
        with open('saved_files.json', 'w') as json_file:
            json.dump(saved_list, json_file)
        return True
