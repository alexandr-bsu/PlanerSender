from fastapi import APIRouter, BackgroundTasks
from services.sender import SenderService, resolve_username
import asyncio

sender_router = APIRouter(prefix='/sender')

def run_sender():
    sender = SenderService()
    asyncio.run(sender.run())

@sender_router.get('/login')
async def login():
    await resolve_username('none_user_404')
    return {'status': 'ok'}

@sender_router.get('/')
async def run_sender(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_sender)
    return {"status": "ok"}

