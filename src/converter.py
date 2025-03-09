import config
from pathlib import Path
import speech_recognition as sr 

def export_transcript(result : str) -> None:
    """UNUSED: Exports transcript of audio to desired location"""
    with open(config.ROOT_DIR + '/data/transcript.txt', 'w') as file:
        file.write(result)

def speech_to_text(file : Path) -> str:
    """Yoinks the transcript from a audio clip. It can take a minute"""
    r = sr.Recognizer()
    audio = sr.AudioFile(str(file))

    with audio as source:
        audio_data = r.record(source)  
        result = r.recognize_sphinx(audio_data)
    
    return result