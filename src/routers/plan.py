from fastapi import APIRouter, Body
from typing import Annotated
from services.planer import PlanerService

plan_router = APIRouter(prefix='/plan')

@plan_router.post('/')
async def plan_task_batch(id: Annotated[str,Body()], message: Annotated[str, Body()], recipients: Annotated[list[str], Body()]):
    planer = PlanerService()
    planer.plan_batch(id, message, recipients)
    return {'status': 'ok'}

@plan_router.post('/stop')
async def stop_task(id: str):
    planer = PlanerService()
    planer.stop_task(id)
    return {'status': 'ok'}