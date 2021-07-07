import asyncio
import json
from json.decoder import JSONDecodeError
from django.contrib.auth import get_user_model
from django.core.checks import messages
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from .models import Post, Comment, ClubPost

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected to post", event)

        self.me = self.scope["user"]
        self.grp_name = self.scope["url_route"]["kwargs"]["grp_name"]

        self.group_post = None
        if self.grp_name != "None":
            self.group_post = await self.get_group(self.grp_name)
        
        self.chat_room = self.grp_name

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        print(f"connected {self.grp_name}")

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
    def get_group(self, grp_name):
        return ClubPost.objects.get(name=grp_name)

    @database_sync_to_async
    def create_post(self, post):
        title = post["title"]
        content = post['content']
        return Post.objects.create(title=title, content=content, author=self.me, grp_name=self.group_post)

class CommentConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected to comment", event)

        self.me = self.scope["user"]
        post_id = self.scope["url_route"]["kwargs"]["post_id"]
        self.chat_room = "post-" + post_id

        self.post = await self.get_post(post_id)

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
            comment_data = json.loads(json_data)
           
            rep_data = {
                "comment_data" : comment_data,
                "user" : self.me.username
            }

            
            await self.create_comment(comment_data)

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type" : "comment_message",
                    "text" : json.dumps(rep_data)
                }
            )

    async def comment_message(self, event):
        await self.send({
            "type" : "websocket.send",
            "text" : event['text']
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def create_comment(self, comment):
        message = comment['message']
        return Comment.objects.create(post=self.post, user=self.me, message=message)

    @database_sync_to_async
    def get_post(self, post_id):
        return Post.objects.get(pk=post_id)