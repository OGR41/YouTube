import json
from client_api import youtube
import isodate
from pprint import pprint

# channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь
# channel_id = 'UC1eFXmJNkjITxPFWTy6RsWg'    # Редакция


class Channel:
    def __init__(self, channel_id='UCMCgOm8GZkHp8zJ6l7_hIuA', title=None, description=None, url=None,
                 subscriber_count=None, video_count=None,
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


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.video_info = youtube.videos().list(id=self.video_id, part='snippet,statistics').execute()
        self.video_name = self.video_info['items'][0]['snippet']['title']
        self.video_view_count = int(self.video_info['items'][0]['statistics']['viewCount'])
        self.video_like_count = int(self.video_info['items'][0]['statistics']['likeCount'])

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.video_id}")'

    def __str__(self):
        return f'{self.video_name}'

    def print_info(self):
        print(json.dumps(self.video_info, indent=2, ensure_ascii=False))

    @property
    def _video_id(self):
        return self.video_id


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_info = youtube.playlists().list(id=self.playlist_id, part='snippet').execute()
        self.playlist_name = self.playlist_info['items'][0]['snippet']['title']

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.video_id}", "{self.playlist_id}")'

    def __str__(self):
        return f'{super().__str__()} ("{self.playlist_name}")'


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_info = youtube.playlists().list(id=self.playlist_id, part='snippet,player').execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = self.playlist_info['items'][0]['snippet']['thumbnails']['standard']['url']

    @property
    def total_duration(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails',
                                                       maxResults=50).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics,snippet,player', id=','.join(video_ids)).\
            execute()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            return duration

    def show_best_video(self):
        like_count = 0
        best_video = ''
        for i in self.video_response['items']:
            if int(i['statistics']['likeCount']) > like_count:
                best_video = i['snippet']['thumbnails']['standard']['url']
        return best_video


pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
pl.title
pl.url
duration = pl.total_duration
print(duration)
print(type(duration))
print(duration.total_seconds())
pl.show_best_video()
