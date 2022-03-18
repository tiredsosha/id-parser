#!/usr/bin/env python3.8

import asyncio
import yaml
from contextlib import AsyncExitStack, asynccontextmanager

from asyncio_mqtt import Client, MqttError
from pydantic import BaseModel


class AiohMqtt:
    def __init__(self, data) -> None:
        self.host = data.host
        self.username = data.username
        self.password = data.password
        self.id = data.id
        self.client_id = 'parser'
        self.ctopic = 'park/id/command'
        self.stopic = 'park/id/status'

    async def setup(self):
        async with AsyncExitStack() as stack:
            tasks = set()
            stack.push_async_callback(self.cancel_tasks, tasks)

            client = Client(hostname=self.host,
                            username=self.username,
                            password=self.password,
                            client_id=self.client_id)
            await stack.enter_async_context(client)

            manager = client.filtered_messages(self.ctopic)
            messages = await stack.enter_async_context(manager)
            template = f'[topic_filter="{self.ctopic}"] {{}}'
            task = asyncio.create_task(self.log_messages(messages, template))
            tasks.add(task)

            await client.subscribe(self.ctopic)

            task = asyncio.create_task(self.post(client))
            tasks.add(task)

            await asyncio.gather(*tasks)

    async def post(self, client):
        while True:
            await client.publish(self.stopic, self.id, qos=1)
            await asyncio.sleep(5)

    async def log_messages(self, messages, template):
        async for message in messages:
            msg = message.payload.decode().strip()
            self.id = msg

            def rewrite(data):
                with open('config.yaml') as f:
                    doc = yaml.safe_load(f)
                doc['id'] = data
                with open('config.yaml', 'w') as file:
                    yaml.safe_dump(doc, file)

            rewrite(msg)

    async def cancel_tasks(self, tasks):
        for task in tasks:
            if task.done():
                continue
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


class Mqtt(BaseModel):
    host: str
    username: str
    password: str
    id: str


async def main():
    with open('config.yaml') as f:
        mqtt = Mqtt(**yaml.safe_load(f))
    aioh = AiohMqtt(mqtt)
    while True:
        try:
            await aioh.setup()
        except MqttError as error:
            print(f'Error "{error}". Reconnecting in {5} seconds.')
        finally:
            await asyncio.sleep(5)


asyncio.run(main())