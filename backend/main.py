from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import jobs, scheduler, sources
from app.db.database import Base, engine
from app.models import job, source
from app.scheduler import start_scheduler, stop_scheduler


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Scraper")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sources.router)
app.include_router(jobs.router)
app.include_router(scheduler.router)


@app.on_event("startup")
def on_startup():
    start_scheduler()


@app.on_event("shutdown")
def on_shutdown():
    stop_scheduler()


@app.get("/")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
