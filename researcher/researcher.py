import uvicorn
from fastapi import FastAPI, HTTPException
import os
app = FastAPI(title="Researcher API",
    description="FastAPI wrapper for the session_7.",
    version="0.1.0")

@app.post("/research")
async def research_task(state: dict):
    try:
        topic = state.get("topic", "AI")
        # Adding some logic to ensure state is updated correctly
        state["research_notes"] = f"Deep research on {topic}: Microservices allow independent scaling of LLM nodes."
        print(f"SUCCESS: Researcher processed {topic}")
        return state
    except Exception as e:
        print(f"ERROR in Researcher: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)