import config
from pathlib import Path
import speech_recognition as sr 
import yt_dlp
from pptx import Presentation

def read_file_content(file_path : Path) -> str:
    """
    Open and reads a file
    """
    try:
        with open(file_path, 'r') as f:
            responses = f.read()
        return responses
    except Exception as e:
        print(f"An error occured while reading the file: {e}")
        return None

def speech_to_text(file : Path) -> str:
    """
    Yoinks the transcript from a audio clip. It can take a minute
    """

    r = sr.Recognizer()
    audio = sr.AudioFile(str(file))

    with audio as source:
        audio_data = r.record(source)  
        result = r.recognize_sphinx(audio_data)
    
    return result

def get_youtube(URL : str) -> None:
    """
    Get's the youtube video, and returns it as wav
    """
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{  
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': str(Path("data/temp_audio")),
        'quiet': True,       # Suppresses output logs
        'no_warnings': True  # Suppresses warnings
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URL)

    # If the rip is not successful, raise a exception with the error code
    if error_code != 0:
        raise ValueError("youtube-dl error: ", error_code)

def extract_text_from_pptx(file_path : Path) -> str:
    """
    Extract text on the slide and the notes of a powerpoint
    """
    prs = Presentation(file_path)
    extracted_text = []
    
    # Goes into each slide and rips all the text out
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
    
    return str(extracted_text) # Returns it as string



def extract_text_from_file(file_path : Path) -> str:
    """
    Extracts text from various file types.
    """
    #Special case if it is a youtube video needs work
    if "youtube.com" in str(file_path):
        youtube_url = str(file_path)
        youtube_url = "https://" + youtube_url[7:] #when converting from path, the \\ turns into \. This is a quick fix
        get_youtube(youtube_url)
        print("Youtube video has been converted to wav:")
        file_path = Path("data/temp_audio.wav")

    # Checks the suffix of a file, depending on the file suffix it will extract text in different ways
    file_extension = file_path.suffix
    match file_extension:
        case ".txt" | ".md":
            text =  read_file_content(file_path)
        case ".wav":
            print("Warning, this may take a while if it is a big file.")
            text = speech_to_text(file_path)
        case ".pptx":
            text = extract_text_from_pptx(file_path)
        case _:
            raise ValueError(f"Unsupported file extension: {file_extension}") 
    return text