from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import numpy as np
import webrtcvad
import logging
import asyncio
from typing import Optional
import wave
import io
import soundfile as sf
from live_transcription import TranscriptionManager

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transcription_manager = TranscriptionManager()

@app.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    logging.info("New WebSocket connection request")
    await websocket.accept()
    logging.info("WebSocket connection accepted")
    
    try:
        await transcription_manager.process_audio_stream(websocket)
    except Exception as e:
        logging.error(f"WebSocket error: {e}")

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)