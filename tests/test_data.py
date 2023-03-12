import pytest
from data import Channel, Video, PLVideo, PlayList, Except
import datetime
import json
from client_api import youtube
import isodate


@pytest.mark.parametrize('channel', [(Channel(channel_id='UCMCgOm8GZkHp8zJ6l7_hIuA', title=None, description=None,
                                              url=None, subscriber_count=None, video_count=None, view_count=None))])
class TestChannel:
    def test_init(self, channel):
        assert channel.channel_id == 'UCMCgOm8GZkHp8zJ6l7_hIuA'
        channel.get_data()
        assert channel.__repr__() == 'Channel("вДудь")'
        assert channel.__str__() == 'Youtube-канал: вДудь'


@pytest.mark.parametrize('video', [(Video(video_id='NHUYIdIjEx0'))])
class TestVideo:
    def test_init(self, video):
        assert video.__repr__() == 'Video("NHUYIdIjEx0")'
        assert video.__str__() == 'Смертельная битва: Карты'
        assert video._video_id == 'NHUYIdIjEx0'


@pytest.mark.parametrize('plv', [(PLVideo(video_id='NHUYIdIjEx0', playlist_id='PL4A6D27CF0F8074FD'))])
class TestPLVideo:
    def test_init(self, plv):
        assert plv.__repr__() == 'PLVideo("NHUYIdIjEx0", "PL4A6D27CF0F8074FD")'
        assert plv.__str__() == 'Смертельная битва: Карты ("Смертельная битва: Android vs iOS")'


@pytest.mark.parametrize('pl', [PlayList(playlist_id='PL4A6D27CF0F8074FD')])
class TestPlayList:
    def test_init(self, pl):
        assert pl.total_duration == datetime.timedelta(seconds=763)
        assert pl.show_best_video() == 'https://i.ytimg.com/vi/LN2XOkVXR-4/sddefault.jpg'




# print(TestChannel.)