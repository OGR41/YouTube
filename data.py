import json
from client_api import youtube


class Channel:
    def __init__(self, title=None, description=None, url=None, subscriber_count=None, video_count=None,
                 view_count=None):
        self.__channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'
        self.title = title
        self.description = description
        self.url = url
        self.subscriber_count = subscriber_count
        self.video_count = video_count
        self.view_count = view_count

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self):
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def get_data(self):
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        data = json.loads(json.dumps(channel, indent=2, ensure_ascii=False))
        for i in data['items']:
            x = i.get('snippet')
            y = i.get('statistics')
            self.title = x['title']
            self.description = x['description']
            self.url = x['thumbnails']['high']['url']
            self.subscriber_count = y['subscriberCount']
            self.video_count = y['videoCount']
            self.view_count = y['viewCount']
        Channel(self.title, self.description, self.url, self.subscriber_count, self.video_count,
                self.view_count)

    def set_json(self):
        data = {'title': self.title,
                'description': self.description,
                'url': self.url,
                'subscriber_count': self.subscriber_count,
                'video_count': self.video_count,
                'view_count': self.view_count}
        with open("new_data.json", "w", encoding="windows-1251") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    @staticmethod
    def get_service():
        return youtube


vdud = Channel()

vdud.get_data()
print(vdud.title)
print(vdud.video_count)
print(vdud.url)

# vdud.channel_id = 'UC1eFXmJNkjITxPFWTy6RsWg'

print(vdud.get_service())

vdud.set_json()
