from fastapi import FastAPI
from routers.plan import plan_router
from routers.sender import sender_router
# import uvicorn

app = FastAPI(root_path='/api/v1')
app.include_router(plan_router)
app.include_router(sender_router)

@app.get('/healthy', status_code=200)
async def check():
    return 'OK'

# uvicorn.run(app, port=11111)