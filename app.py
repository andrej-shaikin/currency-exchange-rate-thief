from apps.router import router
from fastapi import FastAPI

from conf import settings

app = FastAPI(debug=settings.DEBUG)
app.include_router(router=router)
app.state.database = settings.db


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
