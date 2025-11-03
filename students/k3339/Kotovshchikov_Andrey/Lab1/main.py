from contextlib import asynccontextmanager
from fastapi import FastAPI
from users.routes import router as user_router
from profiles.routes import router as profile_router
from projects.routes import router as project_router
from teams.routes import router as team_router
from core.database import SQLConnection
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = SQLConnection(database_uri=str(settings.DATABASE_URI))
    app.state.connection = connection
    yield
    await connection.close()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(profile_router)
app.include_router(project_router)
app.include_router(team_router)
