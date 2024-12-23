from channels.generic.websocket import WebsocketConsumer
import json
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from channels.layers import get_channel_layer

from django.dispatch import Signal, receiver
from asgiref.sync import async_to_sync
class Notification(WebsocketConsumer):
    def connect(self):
        self.group_name = 'notification'
        self.user= self.scope['user']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        print('accept')
        self.accept()
    
    def receive(self, text_data=None, bytes_data=None):
        # print(text_data, 'text data')
        text_data_json = json.loads(text_data)
        
        author = self.user
        event = {
            'type': 'message_handler',
            'message': text_data_json,
            'author' : author,
        }
        return async_to_sync(self.channel_layer.group_send)(self.group_name, event)
    def message_handler(self, event):
        content = event.get('notification') or f"""
<div hx-swap-oob="beforeend:#text">
<p>info: {event['message']['id']}, by {event['author']} </p>
</div>
"""
        self.send(text_data=content)
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        # return self.disconnect(code)
    
    # def send(self, text_data=None, bytes_data=None, close=False, *args, **kwargs):
    #     return self.send(text_data=text_data)

@receiver(signal=[post_save], sender=User)
def signal_reciever(*args, **kwargs):
    notification = get_channel_layer()
    content = f"""
        <div hx-swap-oob="beforeend:#text">
        <p>info: {kwargs.get('instance').is_active} {kwargs}</p>
        </div>
        """
    notification_handeler = {
            'type': 'message_handler',
            'notification': content,
        }
    print('it ran')
    async_to_sync(notification.group_send)(
        'notification', notification_handeler
    )

