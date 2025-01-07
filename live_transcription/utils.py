from random import randint
import os
import wave


async def save_audio_to_file(audio_data, file_name, audio_dir="audio_files", audio_format="wav"):
    """
    Saves the audio data to a file.

    :param audio_data: The audio data to save.
    :param file_name: The name of the file.
    :param audio_dir: Directory where audio files will be saved.
    :param audio_format: Format of the audio file.
    :return: Path to the saved audio file.
    """

    os.makedirs(audio_dir, exist_ok=True)

    file_path = os.path.join(audio_dir, file_name)

    with wave.open(file_path, "wb") as wav_file:
        wav_file.setnchannels(1)  # Assuming mono audio
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        wav_file.writeframes(audio_data)

    return file_path

def post_process_bn(text: str) -> str:
    '''
    Post process Bengali transcripted string.
    
    Arguements:
    -----------
        text (str): String need to be post processed.
    
    Returns:
    --------
        Post processed Bengali string.
    '''
    if len(text) <= 1:
        text = ''
        
    text = text.replace('ট্রেনিং প্রেসিডেন্ট','')
    text = text.replace('ট্রেনিং প্রেসিডেন্ট','')
    text = text.replace('প্রেসিডেন্ট প্রেসিডেন্ট','')
    text = text.replace('প্রেসিডেন্ট প্রেসিডেন্ট প্রেসিডেন্ট','')
    text = text.replace('আসসালামু আলাইকুম','')
    text = text.replace('ভারতীয় বিদ্যমান', '')
    text = text.replace('ভারতীয় বিদ্যমানের জন্য', '')
    text = text.replace('জেলার প্রধান বিভাগের', '')
    # text = bnpunct.add_punctuation(text)
    return text

def random_n(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)