from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import connect_to_mongo, client as mongo_client
from app.core.config import settings
from app.routers import auth_router, organization_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize DB connection (Motor) when the app starts.
    """
    connect_to_mongo()
    yield
    """
    Close DB connection cleanly on shutdown.
    """
    try:
        if mongo_client:
            mongo_client.close()
    except Exception:
        pass


app = FastAPI(title=settings.app_name, lifespan=lifespan)


# Allow local testing from any origin (safe for assignment/demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# include routers
app.include_router(auth_router.router, prefix="/admin", tags=["auth"])
app.include_router(organization_router.router, prefix="/org", tags=["organization"])


@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "service": settings.app_name}
