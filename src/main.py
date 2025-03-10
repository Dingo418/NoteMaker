import config
import gpt
import argparse
import converter
from pathlib import Path
import yt_dlp

configValues = config.config

def split_up(text : str) -> list:
    """Splits the text up into X sentences long prompts and adds them to a list"""
    chunks = []
    max_sentences = int(configValues['PREFERENCES']['max_sentences'])
    sentences = text.split(".")

    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i+max_sentences])
        chunks.append(chunk)
    return chunks

def get_text_from_file(file_path : Path) -> str:
    """Open and reads a file"""
    content = ""
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def export_md(response : list, output_path : Path) -> None:
    """Exports the desired response to a desired path"""
    with open(output_path, 'a') as file:
        file.write("".join(response))

def gpt_process(text : str, system_prompt_path : Path) -> list:
    """Sends chunks to the GPT Processes and collates the response"""
    responses = []
    chunks = split_up(text)
    for i,chunk in enumerate(chunks):
        responses.append(gpt.getGPT(chunk, system_prompt_path))
        print(f"Chunk {i} has been proccessed.")

    return responses

def get_text(file_path : Path) -> str:
    """Figure out what kind of file it is and gets it's text"""
    file_extension = file_path.suffix
    match file_extension:
        case ".txt":
            text = get_text_from_file(file_path)
        case ".wav":
            text = converter.speech_to_text(file_path)
        case _:
            raise ValueError(f"Unsupported file extension: {file_extension}") 
    return text

def get_youtube(URL : str) -> None:
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{  
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': str(Path("data/temp_audio"))
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URL)
    
    if error_code != 0:
        raise ValueError("youtube-dl error: ", error_code)

def main() -> None:
    """Main routine"""
    parser = argparse.ArgumentParser(description="The one stop program to creates notes out of anything!")
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output.md",
        help="Write to file"
    )
    parser.add_argument(
        'filename', 
        type=str, 
        help="The file to process")
    
    
    args = parser.parse_args()
    output_path_note = Path("notes_" + args.output)
    output_path_summary = Path( "summary_" + args.output)
    will_summaries = bool(configValues['PREFERENCES']['will_summarise'])

    if "https://www.youtube.com/watch?v=" in args.filename:
        get_youtube(args.filename)
        file_path = Path("data/temp_audio.wav")
    else:
        file_path = Path(args.filename)

    print("Recieving all the text from the file", file_path.name)
    text = get_text(file_path)

    print("A GPT is now processing the information")
    responses = gpt_process(text, Path("data/note_prompt.txt"))

    print("The note responses are now getting exported")
    export_md(responses, output_path_note)
    
    if will_summaries:
        print("The GPT is now summarising the complete notes")
        responses = gpt_process("".join(responses), Path("data/summarise_prompt.txt"))

        print("The note responses are now getting exported")
        export_md(responses, output_path_summary)

if __name__ == "__main__":
    main()