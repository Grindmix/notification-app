from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class NotificationConsumer(JsonWebsocketConsumer):
    
    def connect(self):

        self.group_name = 'notification'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def notify(self, event):
        self.send_json(event['content'])