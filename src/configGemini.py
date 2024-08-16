from dotenv import load_dotenv
import os
from google.api_core import retry
import google.generativeai as genai
from . import backtobasic as bb;

# cofiguring model api 
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# a function which configure gemini bot and send 2 var 1 is medium to char and 2nd is the class 
def configGemini(
    use_sys_inst, safe ,
):
    # Alternative encodings to try if UTF-8 doesn't work
    MUSEUM_BOT_PROMPT = open("new_prompt.txt", "r", encoding="ISO-8859-1").read()
    # defineing the class and creating all the functionalities 
    museum_bot = bb.museum_bot();

    # Define the ordering system tools/functions
    ordering_system = [

    museum_bot.name,

    museum_bot.age,

    museum_bot.nationality,

    museum_bot.date,

    museum_bot.get_order,

    museum_bot.remove_item,

    museum_bot.clear_order,

    museum_bot.confirm_order,

    museum_bot.place_order

]

    # Toggle this to switch between Gemini 1.5 with a system instruction, or Gemini 1.0 Pro.
    # Select the model name based on the toggle
    model_name = 'gemini-1.5-flash' if use_sys_inst else 'gemini-1.0-pro'
    # Initialize the model with safety settings
    if use_sys_inst:
        model = genai.GenerativeModel(
            # creating the model
        model_name, tools=ordering_system, system_instruction=MUSEUM_BOT_PROMPT, safety_settings=safe)
            # returning the bot class and chat func output
        return model.start_chat(enable_automatic_function_calling=True), museum_bot ;
    else:
        model = genai.GenerativeModel(model_name, tools=ordering_system, safety_settings=safe)
        return model.start_chat(
        history=[
            {'role': 'user', 'parts': [MUSEUM_BOT_PROMPT]},
            {'role': 'model', 'parts': ['OK I understand. I will do my best!']}
        ],
        enable_automatic_function_calling=True
    ),museum_bot ;

@retry.Retry(initial=30)
def send_message(message,model):
    """Send a message to the conversation and return the response."""
    return model.send_message(message)


# Initialize order tracking

