# Notes Generator

A Python-based tool designed to convert various file types into notes by processing the content with GPT.

## Features

- **Supports Multiple File Formats**:
  - `.csv` (Comma Separated Values)
  - `.doc` (Microsoft Word Document)
  - `.docx` (Microsoft Word Document)
  - `.eml` (Email File)
  - `.epub` (eBook Format)
  - `.gif` (Graphics Interchange Format)
  - `.htm` (Hypertext Markup Language)
  - `.html` (Hypertext Markup Language)
  - `.jpeg` (JPEG Image)
  - `.jpg` (JPEG Image)
  - `.json` (JavaScript Object Notation)
  - `.log` (Log File)
  - `.mp3` (MP3 Audio File)
  - `.msg` (Microsoft Outlook Message)
  - `.odt` (OpenDocument Text)
  - `.ogg` (Ogg Audio File)
  - `.pdf` (Portable Document Format)
  - `.png` (Portable Network Graphics Image)
  - `.ps` (PostScript File)
  - `.psv` (Pipe-Separated Values)
  - `.rtf` (Rich Text Format)
  - `.tab` (Tab-Separated Values)
  - `.tff` (TrueType Font)
  - `.tif` (Tagged Image File)
  - `.tiff` (Tagged Image File Format)
  - `.tsv` (Tab-Separated Values)
  - `.txt` (Text File)
  - `.wav` (Waveform Audio File)
  - `.xls` (Microsoft Excel Spreadsheet)
  - `.xlsx` (Microsoft Excel Spreadsheet)
  - `.pptx` (Microsoft PowerPoint Presentation)

- **Supported Web Links**:
  - Web links
  - YouTube URLs
- **Efficient Text Chunking**: Splits large text files or transcriptions into smaller chunks for more efficient processing.
- **GPT-based Summarization**: Processes extracted text to generate notes or summaries using GPT models (e.g., gpt-4, gpt-4o-mini).
- **Exports to Markdown**: Generates an output file in markdown format (`output.md` by default).

## Setup

1. **Install Required Libraries**:
   
   Use `pip` to install the necessary libraries:

   ```bash
   pip install -r requriments
   ```

   **Note**: Make sure you have `ffmpeg` installed on your system, `yt-dlp` requires it to download YouTube videos. On Linux, you can install it using:

   ```bash
   sudo apt install ffmpeg
   ```

2. **Set Up OpenAI API Key**:

   Obtain your OpenAI API key from [OpenAI](https://platform.openai.com/).

   Set the environment variable for your OpenAI API key:

   ```bash
   # Linux/macOS
   export OPENAI_API_KEY="your-api-key-here"
   
   # Windows
   set OPENAI_API_KEY="your-api-key-here"
   ```
   Or

   Edit your .env.example file and rename it to .env
   ```
   # For running LLMs hosted by openai (gpt-4o, gpt-4o-mini, etc.)
   # Get your OpenAI API key from https://platform.openai.com/
   OPENAI_API_KEY=your-openai-api-key
   ```

## Usage

### Running the Tool

To use the Notes Generator, run the script by providing the path to the file or a URL. It will process the content and generate notes in a markdown file (`output.md` by default).

```
usage: main.py [-h] [-N] [-S] [-o OUTPUT] filename

Process files to create notes and summaries.

positional arguments:
  filename             Input file path.

options:
  -h, --help           show this help message and exit
  -N                   Enable note creation.
  -S                   Enable summarization.
  -o, --output OUTPUT  Output file name.
```


### Example Command for `.txt` File noting and summarizing:
```bash
python src/main.py -NS input.txt
```

### Example Command for YouTube URL to note:
```bash
python src/main.py -N https://www.youtube.com/watch?v=your_video_id
```

### Example Command for Web Link to summarize:
```bash
python src/main.py -S https://example.com/article
```

## Environmental Variable

Make sure your OpenAI API key is set as an environmental variable before running the tool:

```bash
# For running LLMs hosted by OpenAI (gpt-4, gpt-4o-mini, etc.)
# Get your OpenAI API key from [https://platform.openai.com/](https://platform.openai.com/)

# Linux/macOS
export OPENAI_API_KEY=your-api-key-here

# Windows
set OPENAI_API_KEY=your-api-key-here
```

## Notes

- If working with **large files**, the tool splits content into smaller chunks (e.g., paragraphs) for easier processing by GPT models.
- The final output is saved in markdown format, making it easy to integrate into note-taking systems or documentation.

## Troubleshooting

- **ffmpeg**: If you encounter errors related to `ffmpeg`, ensure that it's properly installed and accessible in your system's PATH.
  
  On Linux, install it using:

  ```bash
  sudo apt install ffmpeg
  ```

- **API Key Errors**: If the tool cannot authenticate with OpenAI, double-check that the `OPENAI_API_KEY` environment variable is correctly set.
