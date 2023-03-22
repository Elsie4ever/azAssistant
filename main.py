import os
import json
import openai

# Load config values
with open(r'config.json') as config_file:
    config_details = json.load(config_file)
    
# Setting up the deployment name
chatgpt_model_name = config_details['CHAT_GPT_MODEL']

# This is set to `azure`
openai.api_type = "azure"

# The API key for your Azure OpenAI resource.
openai.api_key = os.getenv("OPENAI_API_KEY")

# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
openai.api_base = config_details['OPENAI_API_BASE']

# Currently OPENAI API have the following versions available: 2022-12-01
openai.api_version = config_details['OPENAI_API_VERSION']

# This will correspond to the custom name you chose for your deployment when you deployed a model.
deployment_id='gpt-35-turbo' 

# Prompts Azure OpenAI with a request and synthesizes the response.
def ask_openai(prompt):

    # Ask Azure OpenAI
    response = openai.ChatCompletion.create(
        engine=deployment_id,
        messages = [
            {
                "role":"system",
                "content":"You are an Assistant that helps users turn a natural language scenario into azure cli commands. After users input a user scenario, When user ask complicated scenario, you will:\n1. list out(in bullet points) all Azure CLI command group with no args that would be useful for the scenario, followed by brief introduction the command\n2.add a disclaimer to end: \"the result is powered by OpenAI model, it's only for reference and might not be correct, for more information, please look into https://learn.microsoft.com/en-us/cli/azure/iot?view=azure-cli-latest\""
            },
            {
                "role":"user",
                "content":"How do I route IoT device message using iot hub and save them into azure storage?"
            },
            {
                "role":"assistant",
                "content":"To route IoT device messages to Azure Storage using IoT Hub, the following Azure CLI commands might be useful: (Disclaimer: the result is powered by OpenAI model, it's only for reference and might not be correct, for more information, please look into https://learn.microsoft.com/en-us/cli/azure/iot?view=azure-cli-latest)\n1. az iot hub routing-endpoint create - This command add an endpoint to your IoT Hub\n2. az iot hub route create - This command create a route in IoT Hub\n3. az iot device send-d2c-message - This command send an mqtt device-to-cloud message"
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0,
        max_tokens=800,
        top_p=0,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    text = response['choices'][0]["message"]["content"]
    # colorize the output to blue
    print("\033[94mAssistant: \033[0m\n" + text)

# Continuously get typed input and send as text to Azure OpenAI
def chat_with_open_ai():
    print("\033[94mAssistant: \033[0m Hi! This is AzAssistant powered by OpenAI model. Enter 'stop' or Ctrl-Z to end the conversation.")
    while True:
        try:
            # Get user typed input
            prompt = input("\033[94mUser: \033[0m")

            # stop the conversation in lowercase
            if prompt.lower() == "stop":
                print("\033[94mAssistant: \033[0m Conversation ended, see you next time.")
                break
            else:
                ask_openai(prompt)
                
        except EOFError:
            break

# Main

try:
    chat_with_open_ai()
except Exception as err:
    print("Encountered exception. {}".format(err))