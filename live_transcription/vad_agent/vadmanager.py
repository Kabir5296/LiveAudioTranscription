from .pyannote_vad import PyannoteVAD

def get_vad_agent(method = "pyannote"):
    if method.lower() == "pyannote":
        agent = PyannoteVAD()
    else:
        raise ValueError("Available VAD methods are 'pyannote'.")
    return agent