from fastapi import FastAPI
from celery import Celery
from celery_worker import scrape_and_process

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastAPI + Celery Dockerized Application"}

@app.post("/scrape")
async def scrape_data():
    task = scrape_and_process.delay()
    return {"message": "Scraping started", "task_id": task.id}
