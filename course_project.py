from yadisk import YandexDisk
from vkontakte import Vkontakte
from odnoklassniki import OdnoKlassniki
from pprint import pprint


def get_id_from_input():
    user_input = input('\nВведите id или уникальное имя пользователя vk: ')
    try:
        uid = int(user_input)
    except ValueError:
        uid = vk.get_id(user_input)
    return uid


def run_vk(vk_instance):
    while True:
        user_id = get_id_from_input()
        if not user_id:
            print('Такого пользователя не существует, проверьте введенные данные')
            continue
        if user_id < 1:
            print('Такого пользователя не существует, проверьте введенные данные')
            continue
        albums = vk_instance.get_albums(user_id)
        if not albums:
            print('Возникла ошибка, попробуйте скачать фотографии с другого профиля')
            continue
        album = input('''\nВыберите альбом из списка выше и введите его номер. 
Если список отсутствует, значит пользователь не создал ни одного альбома или они скрыты.
Если Вы хотите загрузить аватарки, введите profile вместо номера.
Если Вы хотите загрузить фотографии со стены, введите wall вместо номера.
Если Вы хотите загрузить сохраненные фотографии, введите saved вместо номера.
Если Вы хотите загрузить фотографии, на которых отмечен пользователь, введите marked вместо номера. ''').lower()
        quantity = input('''\nВведите количество фотографий для сохранения. 
При отсутствии ввода будет скачано стандартное количество фотографий. ''')
        if album == 'marked':
            if not quantity:
                photos = vk_instance.get_users_photos_marked(user_id)
            else:
                try:
                    quantity = int(quantity)
                except ValueError:
                    print('Некорректное количество, проверьте введенные данные')
                    continue
                if quantity < 1:
                    print('Некорректное количество, проверьте введенные данные')
                    continue
                photos = vk_instance.get_users_photos_marked(user_id, quantity)
        else:
            if not quantity:
                photos = vk_instance.get_users_photos(user_id, album)
            else:
                try:
                    quantity = int(quantity)
                except ValueError:
                    print('Некорректное количество, проверьте введенные данные')
                    continue
                if quantity < 1:
                    print('Некорректное количество, проверьте введенные данные')
                    continue
                photos = vk_instance.get_users_photos(user_id, album, quantity)
        if not photos:
            print('''Попробуйте другой альбом. 
    Указанный альбом или не существует, или не содержит фотографий, или доступ к нему ограничен настройками приватности''')
            continue
        return photos


def run_ok(ok_instance):
    while True:
        user_id = input('\nВведите id  пользователя Одноклассники: ')
        if not user_id:
            print('Такого пользователя не существует, проверьте введенные данные')
            continue
        albums = ok_instance.get_albums(user_id)
        if not albums:
            print('Неверный id пользователя. Проверьте вводимую информацию')
            continue
        album = input('''\nВыберите альбом из списка выше и введите его номер. 
Если Вы хотите загрузить личные фотографии пользователя, ничего не вводите, просто нажмите Enter.
Если Вы хотите загрузить фотографии, на которых отмечен пользователь, введите tags вместо номера. ''').lower()
        quantity = input('''\nВведите количество фотографий для сохранения. 
При отсутствии ввода будет скачано стандартное количество фотографий. ''')
        if not quantity:
            photos = ok_instance.get_photo_ids(user_id, album)
        else:
            try:
                quantity = int(quantity)
            except ValueError:
                print('Некорректное количество, проверьте введенные данные')
                continue
            if quantity < 1:
                print('Некорректное количество, проверьте введенные данные')
                continue
            photos = ok_instance.get_photo_ids(user_id, album, quantity)
        if not photos:
            print('Проверьте вводимую информацию. Указанный альбом или не существует или не содержит фотографий')
            continue
        return photos


def run(vk_instance, ok_instance):
    while True:
        choice = input('Выберите социальную сеть для загрузки фотографий (ВКонтакте или Одноклассники): ').lower()
        if choice == 'вконтакте':
            photos = run_vk(vk_instance)
        elif choice == 'одноклассники':
            photos = run_ok(ok_instance)
        else:
            print('Некорректное название социальной сети. Проверьте правильность ввода.')
            continue
        token_ya = input('\nВведите токен с Полигона Яндекс.Диска: ')
        # with open('token_yandexdisk.txt') as file:
        #     token_ya = file.read()
        ya = YandexDisk(token_ya)
        folder = ya.choose_folder()
        uploaded = ya.upload_photos(photos, folder)
        if not uploaded:
            continue
        return '\nФайл(ы) успешно сохранены'


if __name__ == '__main__':
    with open('token_vk_netology.txt') as token_file:
        token_vk = token_file.read()
    vk = Vkontakte(token_vk)
    with open('ok.txt') as key_file:
        application_key = key_file.readline().strip()
        session_key = key_file.readline().strip()
    ok = OdnoKlassniki(application_key, session_key)
    print(run(vk, ok))
