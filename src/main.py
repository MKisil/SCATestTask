from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.spy_cats.router import router as spy_cats_router
from src.missions_targets.router import router as missions_targets_router

app = FastAPI()
app.include_router(spy_cats_router)
app.include_router(missions_targets_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
