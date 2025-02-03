import openai
import openai
import vertexai
from vertexai.generative_models import GenerativeModel
import axonius_api_client as axonapi
from axonius_api_client import Connect
import warnings

# Define Variables
# Get the model type from the user input
PROMPT_FILE = "system_bot.md"

# Replace these with your LLM model and GCP project requirements
## If you're not using ADC for authentication, you will need to modify this section to include a credentials file.
MODEL_TYPE = "gemini-1.5-flash-002"
PROJECT_ID = "PROJECT_ID"

def evaluate_prompt_vertexai(PROJECT_ID, model_type, llm_prompt):
    """
    Function to call the vertexai solution hosted in GCP 

    Parameters:
    - PROJECT_ID (str): ID for the GCP Project with VertexAI enabled
    - model_type (str): LLM Model that should be used
    - llm_prompt (str): Prompt sent to the LLM model

    Returns:
    - str: The response from the LLM model 
    """
    
    # Requires ADC https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel(model_type)
    # Look into Models, Temperature, and Output Token Limit
    response = model.generate_content(llm_prompt) 
    return response.text

def get_input(file_path):
    """
    Function to modify the prompt template with new content which will be used as a prompt to the LLM model. 

    Parameters:
    - file_path (str): The path to the template prompt file
    - new_content (str): The new content that you want to append to the file

    Returns:
    - str: The modified prompt. 
    """

    file_content = ""
    with open(file_path, 'r') as file:
        input_prompt = file.readlines()
        file_content = ''.join(input_prompt)
    return file_content


if __name__ == "__main__":
    # Send the prompt to the LLM model and retrieve the data
    try:    
        llm_prompt = get_input(PROMPT_FILE)
        llm_output = evaluate_prompt_vertexai(PROJECT_ID, MODEL_TYPE, llm_prompt)
        print(llm_output)
    except ValueError as e:
        print(f"Error: {e}")