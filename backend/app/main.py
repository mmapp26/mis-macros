from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth import router as auth_router, create_tables
from .routers.users import router as users_router
from .routers.foods import router as foods_router
from .routers.logs import router as logs_router
from .routers.stats import router as stats_router

app = FastAPI(title="Mis Macros API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(foods_router)
app.include_router(logs_router)
app.include_router(stats_router)

@app.get("/")
def root():
    return {"ok": True, "service": "mis-macros"}