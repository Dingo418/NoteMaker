import config
from pathlib import Path
from openai import OpenAI

def get_system_prompt(system_prompt_path : Path) -> str:
    """
    Gets the system prompt from data/..._prompt
    """
    with open(system_prompt_path, 'r') as file:
        return file.read()

def openAi(given_text : str, system_prompt_path : Path, previous_note_end : str) -> str:
    """
    Connects to openAI and yoinks the response to the prompts
    """
    client = OpenAI(api_key=config.OPENAI_API_KEY) # Connects to openai's api
    completion = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        store=True,
        messages=[{
            "role": "system",
                "content": [
                    {
                        "type"  : "text",
                        "text"  : get_system_prompt(system_prompt_path) + previous_note_end
                    }
                ] 
            },
            {"role": "user", 
                "content": [
                    {
                        "type"  : "text",
                        "text"  : given_text
                    }
                ]
            }
        ]
    )
    # Returns the text response
    return completion.choices[0].message.content


    
def getGPT(given_text : str, system_prompt_path : Path, previous_note_end : str) -> str:
    """
    Figures out which LLM-Provider to use
    """
    # Chooses prefered model provider, can be expanded upon in the future 
    match config.PROVIDER:
        case "openai":
            return openAi(given_text, system_prompt_path, previous_note_end)
        case _:
            raise ValueError("Please use a supported provider in the config.ini file")