from src import configGemini,send_message;
# configurations 
use_sys_inst = False
safe = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
    ];


if __name__=="__main__":
    try:
        model , museum_bot = configGemini(use_sys_inst, safe );
        # Main loop for user interaction
        while not museum_bot.placed_order():
            user_input = input('> ')
            response = send_message(user_input,model)
            print(response.text)

        # Here you might want to check if the order is placed and update placed_order accordingly
        # Example: if response indicates order confirmation, you could set placed_order to True

    except Exception as e:
        print(f"An error occurred: {e}")
