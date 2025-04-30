from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import os
from datetime import datetime

app = FastAPI()

# Path to the CSV file where events will be stored
events_file = "events.csv"

@app.on_event("startup")
async def startup_event():
    # Ensure the CSV exists (with headers) on startup
    if not os.path.exists(events_file) or os.stat(events_file).st_size == 0:
        df = pd.DataFrame()
        df.to_csv(events_file, index=False)

@app.post("/events")
async def receive_event(request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # Add a received timestamp in UTC
    payload["received_at"] = datetime.utcnow().isoformat() + "Z"

    # Convert to DataFrame and append to CSV
    df = pd.DataFrame([payload])
    file_exists_and_not_empty = os.path.exists(events_file) and os.stat(events_file).st_size > 0
    df.to_csv(
        events_file,
        mode="a",
        header=not file_exists_and_not_empty,
        index=False
    )

    return {"status": "success", "received_at": payload["received_at"]}

@app.get("/events")
async def get_events():
    # Return all events as JSON
    try:
        df = pd.read_csv(events_file)
        records = df.to_dict(orient="records")
        return {"events": records}
    except Exception:
        raise HTTPException(status_code=500, detail="Could not read events file")

@app.get("/events/csv")
async def get_events_csv():
    # Return the raw CSV file
    if not os.path.exists(events_file):
        raise HTTPException(status_code=404, detail="Events file not found")
    def iterfile():
        with open(events_file, mode="r", encoding="utf-8") as f:
            for line in f:
                yield line
    return StreamingResponse(iterfile(), media_type="text/csv")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
