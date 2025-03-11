import config
from pathlib import Path
import speech_recognition as sr 
import yt_dlp
from pptx import Presentation

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

def get_youtube(URL : str) -> None:
    """Get's the youtube video, and returns it as wav"""
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{  
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': str(Path("data/temp_audio")),
        'quiet': False,       # Suppresses output logs
        'no_warnings': False  # Suppresses warnings
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URL)
    
    if error_code != 0:
        raise ValueError("youtube-dl error: ", error_code)
    

def extract_text_from_pptx(file_path : Path) -> str:
    prs = Presentation(file_path)
    extracted_text = []
    
    for i, slide in enumerate(prs.slides):
        slide_text = []
        
        # Extract text from slide content
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                slide_text.append(shape.text)
        
        # Extract notes
        notes_text = ""
        if slide.has_notes_slide:
            notes_slide = slide.notes_slide
            notes_text = notes_slide.notes_text_frame.text if notes_slide.notes_text_frame else ""
        
        extracted_text.append({
            "slide_number": i + 1,
            "slide_text": "\n".join(slide_text),
            "notes_text": notes_text
        })
    
    return str(extracted_text)