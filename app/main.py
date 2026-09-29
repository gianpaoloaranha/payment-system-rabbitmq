from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import auth, users
from app.infrastructure.database import Base, engine
from app.models import revoked_token, user 


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Payment Service", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)