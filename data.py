import json
from client_api import youtube

# channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь
# channel_id = 'UC1eFXmJNkjITxPFWTy6RsWg'    # Редакция


class Channel:
    def __init__(self, channel_id='UCMCgOm8GZkHp8zJ6l7_hIuA', title=None, description=None, url=None, subscriber_count=None, video_count=None,
                 view_count=None):
        self.__channel_id = channel_id
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

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.title}")'

    def __str__(self):
        return f'Youtube-канал: {self.title}'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __lt__(self, other):
        if not isinstance(other, (int, Channel)):
            raise TypeError('Неверный тип для сравнения')

        s_c = other if isinstance(other, int) else other.subscriber_count
        return self.subscriber_count > s_c


ch1 = Channel()
ch1.get_data()
print(ch1)
ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
ch2.get_data()
print(ch2)

ch1 > ch2
ch1 < ch2
ch1 + ch2
