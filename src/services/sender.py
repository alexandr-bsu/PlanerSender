from time import sleep

from src.repositories.consumer import ConsumerRepo
from src.repositories.log import QueueLogRepository

from pyrogram import Client as pyro_client
from pyrogram.raw.functions.contacts import ResolvePhone, ResolveUsername

import random

async def resolve_username(username: str):
    pyro = pyro_client(
        api_id='26698245',
        api_hash='eff1cbc9369c401acc08d2d887fab7c4',
        name='hranitelitesttools')

    user_id = None
    async with pyro:
        r = await pyro.invoke(ResolveUsername(username=username))
        if r.users:
            user_id = r.users[0].id
    del pyro
    return user_id


async def resolve_phone(phone: str):
    pyro = pyro_client(
        api_id='26698245',
        api_hash='eff1cbc9369c401acc08d2d887fab7c4',
        name='hranitelitesttools')

    user_id = None
    async with pyro:
        r = await pyro.invoke(ResolvePhone(phone=phone))
        if r.users:
            user_id = r.users[0].id
    del pyro
    return user_id


def contains_only_digits(contact: str):
    contact = contact.replace('-', '').replace('+', '').replace('@', '').replace('_', '').replace(' ', '')
    return contact.isdigit()


async def resolve_contact(contact: str):
    contact = contact.replace('@', '')
    user_id = None
    try:
        if contains_only_digits(contact):
            user_id = await resolve_phone(contact)

        if user_id is None:
            user_id = await resolve_username(contact)

        return {'user_id': user_id}

    except:
        return {'user_id': None}


class SenderService:
    def __init__(self):
        self.consumer = ConsumerRepo()
        self.log = QueueLogRepository()


    async def run(self):
        pyro = pyro_client(
            api_id='26698245',
            api_hash='eff1cbc9369c401acc08d2d887fab7c4',
            name='hranitelitesttools')

        while True:
            message = self.consumer.pop()
            if message:
                id, message = message[0]['msg_id'], message[0]['message']
                user = await resolve_contact(message['username'])
                if user:
                   async with pyro:
                        try:
                            await pyro.send_message(user['user_id'], message['message'])
                            self.log.update_by_queue_id(id, {'state': 'successful'})
                        except:
                            self.log.update_by_queue_id(id, {'state': 'error'})
                            self.consumer.send(message)

            sleep(random.randint(60, 180))

