class TranscriberAgentInterface:
    def __init__(self):
        """ Initialize the transcriber agent. Use intended arguements. """
        
        raise NotImplementedError("This class is only intended as a framework for interfaces to be used. Inherit from it to build custom agent. Or use existing agents available here.")
    
    async def get_transcription(self, audio, language = "en"):
        """ Your agent must contain this function for transcription. Required arguements are audio and langauge. """
        
        raise NotImplementedError("This class is only intended as a framework for interfaces to be used. Inherit from it to build custom agent. Or use existing agents available here.")