from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.repository_routes import router as repository_router
from routes.document_routes import router as document_router
from routes.code_routes import router as code_router
from ai_detection.routes.ai_routes import router as ai_router
from routes.admin_auth import router as admin_auth_router
app = FastAPI(
    title="Plagiarism Detection API",
    version="1.0.0",
    description="Production Ready Document & Code Plagiarism Detection"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
app.include_router(document_router)
app.include_router(repository_router)
app.include_router(code_router)
app.include_router(ai_router)
app.include_router(admin_auth_router)
@app.get("/")
def home():

    return {

        "message": "Plagiarism Detection API Running"

    }