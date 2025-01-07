from .api_agent import APIAgent
from .whisper_agent import WhisperAgent
import os

class CONFIG:
    model_name = "aci-mis-team/Whisper-BN-Medium-TUGSTUGI"
    transcriber_endpoint = "transcribe"
    api = "http://192.168.101.230:9803"
    HF_TOKEN = os.getenv("HF_TOKEN")
    API_KEY = os.getenv("API_KEY")
    
def get_transcriber_agent(method = "whisper", CONFIG = CONFIG):
    if method.lower() == "whisper":
        agent = WhisperAgent(model_name=CONFIG.model_name, token=CONFIG.HF_TOKEN)
    elif method.lower() == "api":
        agent = APIAgent(api = CONFIG.api, transcriber_endpoint_name=CONFIG.transcriber_endpoint, api_key=CONFIG.API_KEY)
    else:
        raise ValueError("Only 'whisper' and 'api' methods are available.")
    return agent