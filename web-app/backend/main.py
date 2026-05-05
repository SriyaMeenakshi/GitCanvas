import sys
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add the parent directory to sys.path so we can import GitCanvas core modules
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the main FastAPI app from the GitCanvas api module
from api.main import app as main_app
from utils import github_api
from ai.ai_roast_service import generate_profile_roast
from ai.description_generator import generate_github_description

class AIRequest(BaseModel):
    username: str
    theme: str = "Default"
    tone: str = "professional"

# Mount AI routes onto the existing main_app
@main_app.post("/api/ai/roast")
async def get_ai_roast(req: AIRequest):
    try:
        # Fetch profile data
        profile_data = github_api.get_live_github_data(req.username, raise_errors=True)
        # Generate roast
        result = generate_profile_roast(profile_data)
        return result
    except Exception as e:
        return {"success": False, "error": str(e), "roast": "Failed to generate roast."}

@main_app.post("/api/ai/description")
async def get_ai_description(req: AIRequest):
    try:
        # Fetch profile data
        profile_data = github_api.get_live_github_data(req.username, raise_errors=True)
        # Generate description
        result = generate_github_description(profile_data, req.theme, req.tone)
        return result
    except Exception as e:
        return {"success": False, "error": str(e), "description": "Failed to generate description."}

# Make sure CORS allows localhost since the frontend will be served from file:// or localhost
# The main_app already has CORSMiddleware, but we might need to ensure it allows all for local testing
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# Export the app for uvicorn
app = main_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
