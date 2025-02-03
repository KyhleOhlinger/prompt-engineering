from openai import OpenAI
import os

PROMPT_FILE = "../Prompt Files/system_bot.md"

# Replace these with your LLM model and GCP project requirements
## If you're not using API keys for authentication, you will need to modify this section to read from environmental variables.
MODEL_TYPE = "gpt-4"
API_KEY = "API_KEY"

def read_markdown_prompt(file_path):
    """Reads the content of a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def query_openai(prompt, model, api_key):
    """Sends the prompt to OpenAI's API and returns the response."""
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable if no key provided
    
    if not api_key:
        raise ValueError("API key is required. Set OPENAI_API_KEY as an environment variable or pass it explicitly.")
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ], 
        temperature=0.6
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    try:
        llm_prompt = read_markdown_prompt(PROMPT_FILE)
        llm_output = query_openai(llm_prompt, MODEL_TYPE, API_KEY)
        print(llm_output)
    except Exception as e:
        print(f"Error: {e}")