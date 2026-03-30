import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# --- DYNAMIC PATH SETUP ---
# This ensures the server can see the "Models" and "Search Algorithms" folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "Models"))
SEARCH_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "Search Algorithms"))

# Add to sys.path if not already there
if MODELS_PATH not in sys.path:
    sys.path.append(MODELS_PATH)
if SEARCH_PATH not in sys.path:
    sys.path.append(SEARCH_PATH)

# Import run_navigation AFTER paths are set
try:
    from main import run_navigation
except ImportError as e:
    print(f"❌ Critical Import Error: {e}")
    print(f"Looked in: {MODELS_PATH}")
    run_navigation = None

app = FastAPI()

# --- CORS SETUP ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REQUEST MODEL ---
class RequestData(BaseModel):
    origin: int
    destination: int
    timestamp: str
    model: str = "GRU"

# --- API ROUTES ---

@app.post("/predict")
async def predict(data: RequestData):
    if run_navigation is None:
        return {"error": "Backend logic (main.py) failed to load. Check server console."}
    
    try:
        result = run_navigation(
            origin=data.origin,
            destination=data.destination,
            timestamp=data.timestamp,
            model_type=data.model
        )

        return {
            "edges": result.get("edges", []),
            "flows": result.get("flows", {}),
            "results": result.get("results", {})
        }

    except Exception as e:
        print(f"🔥 Prediction Error: {str(e)}")
        return {"error": str(e)}

@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Traffic AI Backend is running 🚀",
        "paths_loaded": [MODELS_PATH, SEARCH_PATH]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)