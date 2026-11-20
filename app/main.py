from fastapi import FastAPI

from app.routers import me, teams

app = FastAPI()

app.include_router(teams.router)
app.include_router(me.router)
