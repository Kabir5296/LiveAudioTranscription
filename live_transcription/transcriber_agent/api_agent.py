import os, torchaudio, io, aiohttp
from random import randint
from fastapi import HTTPException
from .agent_interface import TranscriberAgentInterface
from ..utils import random_n

temp_folder = 'Temp'
if not os.path.exists(temp_folder):
    os.mkdir(temp_folder)
    
class APIAgent(TranscriberAgentInterface):
    def __init__(self, api = "http://192.168.101.230:9803",transcriber_endpoint_name = "transcribe", api_key = os.getenv("API_KEY")):
        self.api = api
        self.endpoints = {
            "transcriber": transcriber_endpoint_name,
        }
        self.TOKEN = api_key
        
    async def get_transcription(self, audio, language = "en"):
        file_name = temp_folder+f'/audio_chunk_{random_n(8)}.mp3'

        byte_stream = io.BytesIO(audio)
        byte_stream.seek(0)
        
        waveform, sample_rate = torchaudio.load(byte_stream)
        if waveform.dim() == 2:  # Stereo
            waveform = waveform.mean(dim=0, keepdim=True)  # Convert to mono
        byte_stream.seek(0)
        
        torchaudio.save(file_name, waveform, sample_rate)
        url = f'{self.api}/{self.endpoints["transcriber"]}'
        
        try:
            async with aiohttp.ClientSession() as session:
                with open(file_name, 'rb') as audio_file:
                    data = aiohttp.FormData()
                    data.add_field('file', audio_file)
                    data.add_field('language', language)
                    
                    headers = {
                        "Authorization": f"Bearer {self.TOKEN}"
                    }
                    
                    async with session.post(
                        url=url,
                        data=data,
                        headers=headers,
                        ssl=False
                    ) as response:
                        if response.status != 200:
                            raise HTTPException(400, "Transcriber Failed.")
                        result = await response.json()
        finally:
            if os.path.exists(file_name):
                os.unlink(file_name)
                
        return result['content']