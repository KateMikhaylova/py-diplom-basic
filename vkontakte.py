import requests
import time


class Vkontakte:

    def __init__(self, token):
        self.token = token

    def get_id(self, nickname):
        URL = 'https://api.vk.com/method/users.get'
        params = {'user_ids': nickname, 'access_token': self.token, 'v': '5.131'}
        result = requests.get(URL, params=params)
        if not result.json()['response']:
            return result.json()['response']
        uid = result.json()['response'][0]['id']
        return uid

    def get_albums(self, uid):
        URL = 'https://api.vk.com/method/photos.getAlbums'
        params = {'owner_id': uid, 'access_token': self.token, 'v': '5.131'}
        result = requests.get(URL, params=params)
        if 'error' in result.json().keys():
            if result.json()['error']['error_msg'] == 'This profile is private':
                print('Этот профиль скрыт настройками приватности')
                return False
            if result.json()['error']['error_msg'] == 'User was deleted or banned':
                print('Этот профиль удален или забанен')
                return False
            if (result.json()['error']['error_msg'] == 'Access denied: user is deactivated' or
                                                       'invalid: owner_id not integer'):
                print('Этот профиль удален или еще не создан')
                return False
        album_ids = {}
        for item in result.json()['response']['items']:
            album_ids[item['id']] = item['title']
        for aid, name in album_ids.items():
            print(f'Название альбома - "{name}", id-альбома - {aid}')
        return True

    def get_users_photos(self, uid, album_id, photos_quantity=5):
        URL = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': uid, 'album_id': album_id, 'extended': '1', 'access_token': self.token, 'v': '5.131'}
        info = requests.get(URL, params=params).json()
        if 'error' in info.keys():
            if (info['error']['error_msg'] == 'Access denied' or
                    'One of the parameters specified was missing or invalid: album_id is invalid'):
                return False
        return get_photos(info, photos_quantity)

    def get_users_photos_marked(self, uid, photos_quantity=5):
        URL = 'https://api.vk.com/method/photos.getUserPhotos'
        params = {'user_id': uid, 'extended': '1', 'access_token': self.token, 'v': '5.131'}
        info = requests.get(URL, params=params).json()
        if 'error' in info.keys():
            if info['error']['error_msg'] == 'Permission to perform this action is denied':
                return False
        return get_photos(info, photos_quantity)


def get_photos(response, quantity):
    photos_dict = {}
    items = response['response']['items']
    for item in items:
        likes = str(item['likes']['count'])
        date = time.strftime('%Y%B%d%A%H_%M_%S', time.localtime(item['date']))
        square = 0
        url = str()
        size = str()
        for element in item['sizes']:
            if element['height'] * element['width'] >= square:
                square = element['height'] * element['width']
                url = element['url']
                size = element['type']
        if likes not in photos_dict.keys():
            photos_dict[likes] = size, url
        else:
            photos_dict[f'{likes}-{date}'] = size, url
        if len(photos_dict) == quantity:
            break
    return photos_dict
