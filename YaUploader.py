import requests
from pprint import pprint


class YaUploader:

    def __init__(self, token):
        self.token = token

    def upload(self, file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        params = {"path": file_path, "owerwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload_to_disk(self, file_path, source):
        href = self.upload(file_path=file_path).get('href', '')
        response = requests.put(href, data=requests.get(source).content)
        response.raise_for_status()



