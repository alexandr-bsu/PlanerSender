from fastapi import APIRouter, BackgroundTasks
from src.services.sender import SenderService
import asyncio

sender_router = APIRouter(prefix='/sender')

def run_sender():
    sender = SenderService()
    asyncio.run(sender.run())

@sender_router.get('/')
async def get_orders_report(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_sender)
    return {"status": "ok"}

