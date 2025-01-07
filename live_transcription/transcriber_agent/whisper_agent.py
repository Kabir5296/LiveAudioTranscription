from transformers import pipeline
from transformers.utils import is_flash_attn_2_available
import torch, os, torchaudio, io, gc
import warnings
from fastapi import HTTPException
from random import randint
from ..utils import post_process_bn, random_n
from .agent_interface import TranscriberAgentInterface
warnings.filterwarnings("ignore")
HF_TOKEN = os.getenv("HF_TOKEN")

temp_folder = 'Temp'
if not os.path.exists(temp_folder):
    os.mkdir(temp_folder)
    
class WhisperAgent(TranscriberAgentInterface):
    def __init__(self, model_name = "aci-mis-team/Whisper-BN-Medium-TUGSTUGI", token = HF_TOKEN):
        self.TOKEN = token
        self.device = "cuda"
        self.torch_dtype = torch.float16
        self.chunk_length_s=30
        self.batch_size=12
        self.transcription_pipeline = pipeline(
            task="automatic-speech-recognition",
            model=model_name,
            torch_dtype=self.torch_dtype,
            device=self.device,
            model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"},
            token=self.TOKEN,
            )

    async def get_transcription(self, audio, language = "bn"):
        file_name = temp_folder+f'/audio_chunk_{random_n(8)}.mp3'
        byte_stream = io.BytesIO(audio)
        byte_stream.seek(0)
        
        waveform, sample_rate = torchaudio.load(byte_stream)
        if waveform.dim() == 2:  # Stereo
            waveform = waveform.mean(dim=0, keepdim=True)  # Convert to mono
        byte_stream.seek(0)
        
        torchaudio.save(file_name, waveform, sample_rate)
        
        try:
            if language == 'bn':
                transcriptions = self.transcription_pipeline(file_name,
                                                        batch_size=self.batch_size,
                                                        chunk_length_s=self.chunk_length_s,
                                                        return_timestamps=False,
                                                        )
                if type(transcriptions) == dict:
                    transcriptions = post_process_bn(transcriptions['text'])
                elif type(transcriptions) == list:
                    for transcription in transcriptions:
                        transcription['text'] = post_process_bn(transcription['text'])
                torch.cuda.empty_cache()
                gc.collect()
                os.unlink(file_name)
                return {"transcription" : transcriptions}
        except Exception as e:
            torch.cuda.empty_cache()
            gc.collect()
            os.unlink(file_name)
            raise HTTPException(400, f"Transcriber Failed: {e}")