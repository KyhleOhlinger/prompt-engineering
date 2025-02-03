import os
import anthropic

PROMPT_FILE = "../Prompt Files/system_bot.md"

# Replace these with your LLM model and GCP project requirements
## If you're not using API keys for authentication, you will need to modify this section to read from environmental variables.
MODEL_TYPE = "claude-3-haiku-20240307"
API_KEY = "API_KEY"

def read_input_file(file_path):
    """
    Read input from a specified file.
    
    Args:
        file_path (str): Path to the input file.
    
    Returns:
        str: Contents of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

def interact_with_anthropic_api(input_text, api_key, model):
    """
    Send input to Anthropic API and return the response.
    
    Args:
        input_text (str): Text to send to the API.
        api_key (str, optional): Anthropic API key. 
        model (str, optional): Anthropic model to use.
    
    Returns:
        str: API response or None if an error occurs.
    """
    # Use API key from environment variable if not provided
    if api_key is None:
        api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("Error: No API key provided. Set ANTHROPIC_API_KEY environment variable or pass the key.")
        return None
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": input_text
                }
            ]
        )
        
        return response.content[0].text
    except Exception as e:
        print(f"Error interacting with Anthropic API: {e}")
        return None

if __name__ == '__main__':
    # Ensure anthropic library is installed
    try:
        llm_prompt = read_input_file(PROMPT_FILE)
        llm_output = interact_with_anthropic_api(llm_prompt, API_KEY, MODEL_TYPE)
        print(llm_output)
    except ImportError:
        print("Anthropic library not found. Please install it using:")
        print("pip install anthropic")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")