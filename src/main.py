import config
import gpt
import argparse
import converter
from pathlib import Path


configValues = config.config

def split_up(text: str) -> list:
    """Splits the text into chunks of max_characters in length, preserving sentence boundaries. Not 100% accurate, but very close"""
    
    max_characters = int(configValues['PREFERENCES']['max_characters'])
    sentences = text.split(". ")
    
    chunks = []
    chunk = ""
    character_count = 0
    
    for sentence in sentences:
        sentence_length = len(sentence) + 1  # Including space after the sentence
        if character_count + sentence_length > max_characters:
            # If adding the sentence exceeds the max limit, save the current chunk and reset
            chunks.append(chunk.strip())
            chunk = sentence
            character_count = sentence_length
        else:
            # Otherwise, add sentence to the current chunk
            chunk += sentence + ". "
            character_count += sentence_length
    
    # Append the last chunk, if any
    if chunk:
        chunks.append(chunk.strip())
    
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
    previous_note_end = "This is the start of a new note."
    for i,chunk in enumerate(chunks):
        responses.append(gpt.getGPT(chunk, system_prompt_path, previous_note_end))
        previous_note_end = responses[-1][:-20] 
        print(f"Chunk {i} has been proccessed.")

    return responses

def get_text(file_path : Path) -> str:
    """Figure out what kind of file it is and gets it's text"""

    #Special case if it is a youtube video needs work
    if "youtube.com" in str(file_path):
        youtube_url = str(file_path)
        youtube_url = "https://" + youtube_url[7:] #when converting from path, the \\ turns into \. This is a quick fix
        converter.get_youtube(youtube_url)
        print("Youtube video has been converted to wav:")
        file_path = Path("data/temp_audio.wav")

    file_extension = file_path.suffix
    match file_extension:
        case ".txt":
            text = get_text_from_file(file_path)
        case ".wav":
            print("Warning, this may take a while if it is a big file.")
            text = converter.speech_to_text(file_path)
        case ".pptx":
            text = converter.extract_text_from_pptx(file_path)
        case _:
            raise ValueError(f"Unsupported file extension: {file_extension}") 
    return text

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
    file_path = Path(args.filename)

    print("Recieving all the text from the file", file_path.name)
    text = get_text(file_path)

    print("A GPT is now processing the information")
    responses = gpt_process(text, Path("data/note_prompt.txt"))

    print("The note responses are now getting exported")
    export_md(responses, output_path_note)
    
    if will_summaries == "True": # I know, the ini returns strings
        print("The GPT is now summarising the complete notes")
        responses = gpt_process("".join(responses), Path("data/summarise_prompt.txt"))

        print("The note responses are now getting exported")
        export_md(responses, output_path_summary)

if __name__ == "__main__":
    main()