import config
import gpt
import argparse
import converter
from pathlib import Path


configValues = config.config

def split_up(text: str) -> list:
    """Splits the text into chunks of max_characters in length, preserving sentence boundaries. Not 100% accurate, but very close"""
    # gets the max character limit and splits it based on sentences
    max_characters = int(configValues['PREFERENCES']['max_characters'])
    sentences = text.split(". ")
    
    chunks = []
    chunk = ""
    character_count = 0
    
    for sentence in sentences:
        sentence_length = len(sentence) + 1  # Including space after the sentence since I got rid of it with the split
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
    # Just opens 
    with open(output_path, 'a') as file:
        file.write("".join(response))

def gpt_process(text : str, system_prompt_path : Path) -> list:
    """Sends chunks to the GPT Processes and collates the response"""
    previous_note_end = "This is the start of a new note." # in the prompt there is a section to continue the note, 
    responses = []                                         # this makes it so it knows it the start of a note
    chunks = split_up(text) # splits up the text into chunks, to improve gpt performance
    
    print(f"Out of {len(chunks)-1}") # finds out how many chunks there is
    for i,chunk in enumerate(chunks):
        responses.append(gpt.getGPT(chunk, system_prompt_path, previous_note_end)) # Adds the GPT response to the responses array
        previous_note_end = responses[-1][:-20] # gets the last 20 characters of the previous note to pass through, so the gpt knows how to begin
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

    # Checks the suffix of a file, depending on the file suffix it will extract text in different ways
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
    
    # Configures basic parameters
    args = parser.parse_args()
    output_path_note = Path("notes_" + args.output)
    output_path_summary = Path( "summary_" + args.output)
    will_summarize = configValues['PREFERENCES']['will_summarize']
    will_note = configValues['PREFERENCES']['will_note']
    file_path = Path(args.filename)

    # Gets text from file
    print("Recieving all the text from the file", file_path.name)
    responses = get_text(file_path)
    
    # If the config says note, spin up a gpt using the text file and note_prompt.txt
    if will_note == "True": #I know, the ini returns strings
        print("A GPT is now processing the information")
        responses = gpt_process(responses, Path("data/note_prompt.txt"))

        print("The note responses are now getting exported")
        export_md(responses, output_path_note)
    
    # If the config says summarize, spin up a gpt with the summarize prompt, and the response of the previous code
    if will_summarize == "True": # I know, the ini returns strings
        print("The GPT is now summarizing the complete notes")
        responses = gpt_process("".join(responses), Path("data/summarize_prompt.txt"))

        print("The note responses are now getting exported")
        export_md(responses, output_path_summary)

if __name__ == "__main__":
    main()