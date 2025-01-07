from fastapi import WebSocket
import numpy as np
import webrtcvad
import logging
from typing import Optional
import wave
import io
from .transcriber_agent import get_transcriber_agent

agent = get_transcriber_agent(method="whisper")

class AudioProcessor:
    def __init__(self):
        self.vad = webrtcvad.Vad(3)
        self.sample_rate = 16000
        self.frame_duration = 30
        self.buffer = []
        self.is_speech = False
        self.silence_frames = 0
        self.speech_frames = 0
        self.frame_size = int(self.sample_rate * self.frame_duration / 1000)

    def process_audio(self, audio_chunk: np.ndarray) -> Optional[bytes]:
        try:
            # Convert to 16-bit PCM
            audio_chunk = (audio_chunk * 32767).astype(np.int16)
            frames = self._frame_generator(audio_chunk, self.frame_size)
            
            for frame in frames:
                try:
                    is_speech = self.vad.is_speech(frame.tobytes(), self.sample_rate)
                    self.buffer.append(frame)
                    
                    if is_speech:
                        self.speech_frames += 1
                        self.silence_frames = 0
                        self.is_speech = True
                    else:
                        self.silence_frames += 1
                    
                    if self.is_speech and self.silence_frames > 10:
                        if self.speech_frames > 5:
                            complete_audio = np.concatenate(self.buffer)
                            
                            # Convert to WAV format
                            wav_buffer = io.BytesIO()
                            with wave.open(wav_buffer, 'wb') as wav_file:
                                wav_file.setnchannels(1)
                                wav_file.setsampwidth(2)  # 16-bit
                                wav_file.setframerate(self.sample_rate)
                                wav_file.writeframes(complete_audio.tobytes())
                            
                            self.buffer = []
                            self.is_speech = False
                            self.speech_frames = 0
                            self.silence_frames = 0
                            return wav_buffer.getvalue()
                except Exception as e:
                    logging.error(f"VAD processing error: {e}")
                    continue
            
            return None
        except Exception as e:
            logging.error(f"Audio processing error: {e}")
            return None

    def _frame_generator(self, audio: np.ndarray, frame_size: int):
        n = len(audio)
        offset = 0
        while offset + frame_size < n:
            yield audio[offset:offset + frame_size]
            offset += frame_size

class TranscriptionManager:
    def __init__(self):
        self.audio_processor = AudioProcessor()
        
    async def process_audio_stream(self, websocket: WebSocket):
        try:
            while True:
                try:
                    audio_data = await websocket.receive_bytes()
                    audio_chunk = np.frombuffer(audio_data, dtype=np.float32)
                    wav_data = self.audio_processor.process_audio(audio_chunk)
                    if wav_data is not None:
                        transcription = await agent.get_transcription(wav_data)
                        if transcription:
                            await websocket.send_json({"text": transcription['transcription']})
                except Exception as e:
                    logging.error(f"Stream processing error: {e}")
                    break
        except Exception as e:
            logging.error(f"Audio stream error: {e}")