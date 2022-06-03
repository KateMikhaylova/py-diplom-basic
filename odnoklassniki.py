import requests
import time


class OdnoKlassniki:

    def __init__(self, application_key, session_key):
        self.application_key = application_key
        self.session_key = session_key

    def get_albums(self, user_id):
        URL = 'https://api.ok.ru/fb.do?'
        params = {'application_key': self.application_key, 'format': 'json', 'method': 'photos.getAlbums',
                  'session_key': self.session_key, 'fid': user_id}
        result = requests.get(URL, params=params)
        if 'error_code' in result.json().keys():
            return False
        for album in result.json()['albums']:
            print(f'Название альбома - {album["title"]}, id-альбома {album["aid"]}')
        return True

    def get_photo_ids(self, user_id, album_id, quantity=5):
        URL = 'https://api.ok.ru/fb.do?'
        params = {'application_key': self.application_key, 'format': 'json', 'method': 'photos.getPhotos',
                  'session_key': self.session_key, 'fid': user_id, 'aid': album_id, 'count': 100,
                  'fields': 'photo.pic_max,photo.like_count,photo.created_ms'}
        result = requests.get(URL, params=params)
        if 'error_code' in result.json().keys():
            return False
        photo_dict = {}
        for photo in result.json()['photos']:
            if str(photo['like_count']) not in photo_dict.keys():
                photo_dict[str(photo['like_count'])] = 'pic_max', photo['pic_max']
            else:
                date = time.strftime("%Y%B%d%A%H_%M_%S", time.localtime(photo["created_ms"]//1000))
                photo_dict[f'{photo["like_count"]}-{date}'] = 'pic_max', photo['pic_max']
            if len(photo_dict) == quantity:
                break
        return photo_dict
