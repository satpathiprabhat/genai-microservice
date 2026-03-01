import uvicorn
import os
from fastapi import FastAPI, HTTPException
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import logging
import google.cloud.logging
from prometheus_fastapi_instrumentator import Instrumentator
# Look for .env in the current folder OR one level up
load_dotenv() 
load_dotenv("../.env") 

# Initialize the GCP Logging Client
#client = google.cloud.logging.Client()
# Connects standard Python logging to Google Cloud
#client.setup_logging()

app = FastAPI(title="Writer API",
    description="FastAPI wrapper for the session_7.",
    version="0.1.0")

# Validate API Key exists before starting
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY not configured in environment")
else:
    print(f"DEBUG: GOOGLE_API_KEY loaded. Length={len(api_key)} Prefix={api_key[:5]}")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

@app.post("/write")
async def write_task(state: dict):
    try:
        notes = state.get("research_notes", "No research found.")
        prompt = f"Write a 1-sentence catchy headline for this research: {notes}"
        
        response = llm.invoke(prompt)
        state["draft"] = response.content
        print("SUCCESS: Writer generated content.")
        return state
    except Exception as e:
        print(f"ERROR in Writer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)