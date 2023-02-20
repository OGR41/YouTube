import json
from client_api import youtube

channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь
# channel_id = 'UC1eFXmJNkjITxPFWTy6RsWg'    # Редакция


class Channel:

    def __init__(self, channel_id):
        self.channel_id = channel_id

    def print_info(self):
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))


vdud = Channel(channel_id)
vdud.print_info()
