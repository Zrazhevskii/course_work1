import json
from add_in_disk import YaUploader
import requests


with open('2.txt', 'r') as file_object:
    token_vk = file_object.read().strip()


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token_vk, version):
        self.params = {
            'access_token': token_vk,
            'v': version
        }

    def get_photos(self, owner_id=None):
        get_photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': 1,
            'count': 5
        }
        photo_info = requests.get(get_photos_url, params={**self.params, **photos_params}).json()['response']
        photos = []
        for photo in photo_info['items']:
            info = {}
            info['date'] = photo['date']
            info['likes'] = photo['likes']['count']
            sizes = {}
            for size in photo['sizes']:
                sizes[size['type']] = size['url']
            size_type = sorted(sizes.keys())[-1]
            info['url'] = sizes[size_type]
            info['size'] = size_type
            photos.append(info)
        return photos

    def back_up(self):
        photos = self.get_photos()
        with open('1.txt', 'r') as f:
            token = f.readline().rstrip()
            uploader = YaUploader(token)
        likes = []
        json_data = []
        for photo in photos:
            if photo['likes'] in likes:
                name = f"{photo['likes']} - {photo['date']}.jpeg"
            else:
                name = f"{photo['likes']}.jpeg"
                likes.append(photo['likes'])
            json_data.append(
                {
                    "file_name": name,
                    "size": photo['size'],
                }
            )
            uploader.upload_to_disk(f"netology/{name}", photo['url'])
        with open('data.json', 'w') as f:
            f.write(json.dumps(json_data, indent=4))


vk_client = VkUser(token_vk, '5.131')
vk_client.back_up()

