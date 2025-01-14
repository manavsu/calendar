from fastapi import FastAPI
from models import DB_Base
import uvicorn
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as api_router

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


if __name__ == "__main__":
    port = 8000
    print(f"Serving on http://localhost:{port}/")
    uvicorn.run(app, host="0.0.0.0", port=port)