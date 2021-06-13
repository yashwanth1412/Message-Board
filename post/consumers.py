import asyncio
import json
from json.decoder import JSONDecodeError
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from .models import Post, Comment

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)

        self.me = self.scope["user"]
        self.chat_room = "index"

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept",
        })
        

    async def websocket_receive(self, event):
        json_data = event.get("text", None)
        
        if json_data is not None:
            post_data = json.loads(json_data)
           
            rep_data = {
                "post_data" : post_data,
                "user" : self.me.username
            }

            
            await self.create_post(post_data)

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type" : "post_message",
                    "text" : json.dumps(rep_data)
                }
            )

    async def post_message(self, event):
        await self.send({
            "type" : "websocket.send",
            "text" : event['text']
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def create_post(self, post):
        title = post["title"]
        content = post['content']
        return Post.objects.create(title=title, content=content, author=self.me)


