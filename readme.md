# Notes Generator

A Python-based tool for converting files into notes by processing the content with GPT. The program takes a file (either `.txt` or `.wav`), processes it into smaller chunks, sends these chunks to GPT for note creation, and exports the results into a markdown file. STILL IN DEVELOPMENT.
+yt+dlp needs fmpg? so linux figure it out
## Features

- Handles both `.txt` and `.wav` files.
- Splits large texts into smaller chunks for efficient processing.
- Processes text using GPT to generate responses.
- Exports results into a markdown file (`output.md` by default).

## Usage

### Environmental Variable
```
# For running LLMs hosted by openai (gpt-4o, gpt-4o-mini, etc.)
# Get your OpenAI API key from https://platform.openai.com/
set OPENAI_API_KEY=...
```

### Command Line Arguments

| Argument           | Description                                                           |
|--------------------|-----------------------------------------------------------------------|
| `-o`, `--output`   | Specifies the output file name (default is `output.md`).              |
| `filename`         | Specifies the path of the file to process. This can be a `.txt` file or a `.wav` file. | 
| `-h`, `--help`     | Displays the help menu |

### Example Usage

1. **Process a `.txt` file**:
   
   ```bash
   python main.py yourfile.txt
   ```

   This will process `yourfile.txt` and output the notes into `output.md`.

2. **Process a `.wav` file**:
   
   ```bash
   python main.py yourfile.wav
   ```

   This will process `yourfile.wav` and output the notes into `output.md`.

3. **Specify an output file**:
   
   ```bash
   python main.py yourfile.txt -o notes_output.md
   ```

   This will process `yourfile.txt` and output the notes into `notes_output.md`.


### File Types Supported

- `.txt` files: Plain text files that are directly read and processed.
- `.wav` files: Audio files that are converted to text before processing.