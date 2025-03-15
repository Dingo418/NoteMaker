import config
import gpt
import argparse
import converter
from pathlib import Path

NOTE_PROMPT_PATH = Path("data/note_prompt.txt")
SUMMARY_PROMPT_PATH = Path("data/summarize_prompt.txt")

def chunk_text_by_sentences(text: str) -> list:
    """
    Splits the text into chunks respecting sentence boundaries, within the maximum character limit.
    """
    # gets the max character limit and splits it based on sentences
    max_characters = config.MAX_CHARACTERS
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

def write_to_markdown(response : list, output_path : Path) -> None:
    """
    Exports the desired response to a desired path
    """
    with open(output_path, 'a') as file:
        file.write("".join(response))

def process_text_with_gpt(text : str, system_prompt_path : Path) -> list:
    """
    Processes text in chunks using GPT and concatenates the responses
    """
    previous_note_end = "This is the start of a new note. Ignore the previous sentence." # in the prompt there is a section to continue the note, 
    responses = []                                         # this makes it so it knows it the start of a note
    chunks = chunk_text_by_sentences(text) # splits up the text into chunks, to improve gpt performance
    
    print(f"Out of {len(chunks)-1}") # finds out how many chunks there is
    for i,chunk in enumerate(chunks):
        responses.append(gpt.getGPT(chunk, system_prompt_path, previous_note_end)) # Adds the GPT response to the responses array
        previous_note_end = responses[-1][-40:] # gets the last 40 characters of the previous note to pass through, so the gpt knows how to begin
        print(f"Chunk {i} has been proccessd.")

    return responses

def parse_arguments() -> None:
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Process files to create notes and summaries.")
    parser.add_argument("-N", action="store_true", help="Enable note creation.")
    parser.add_argument("-S", action="store_true", help="Enable summarization.")
    parser.add_argument("-o", "--output", type=str, default="output.md", help="Output file name.")
    parser.add_argument("filename", type=str, help="Input file path.")
    return parser.parse_args()

def main() -> None:
    """
    Main routine
    """
    # Configures basic parameters
    args = parse_arguments()
    will_note = args.N
    will_summarize = args.S
    output_path_note = Path("notes_" + args.output)
    output_path_summary = Path( "summary_" + args.output)
    file_path = args.filename

    # Gets text from file
    print("Recieving all the text from the file", file_path)

    responses = converter.extract_text_from_file(file_path)
    if will_note:
        print("A GPT is now processing the information")
        responses = process_text_with_gpt(responses, NOTE_PROMPT_PATH)

        print("The note responses are now getting exported")
        write_to_markdown(responses, output_path_note)
    
    if will_summarize:
        print("The GPT is now summarizing the complete notes")
        responses = process_text_with_gpt("".join(responses), SUMMARY_PROMPT_PATH)

        print("The note responses are now getting exported")
        write_to_markdown(responses, output_path_summary)

if __name__ == "__main__":
    main()