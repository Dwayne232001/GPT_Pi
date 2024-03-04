import openai

# Set up your OpenAI API credentials
openai.api_key = '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'

# Define a function to send a chat message and get the model's response
def send_chat_message(message, chat_history=None):
    if chat_history is None:
        chat_history = []
    chat_history.append(message)

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',  # Specify the GPT-3.5 Turbo model
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': message}
        ],
        max_tokens=100,   # Controls the length of the response. Adjust as per your needs
        n=1,              # Number of responses to generate
        stop=None,        # Optional stop sequence to end the response
        timeout=15        # Timeout in seconds for the API call
    )
    model_reply = response.choices[0].message.content.strip()
    chat_history.append(model_reply)
    return model_reply

# Main loop to interact with the chat model
chat_history = []  # Initialize an empty chat history

while True:
    user_input = input('User: ')

    # Check for exit condition
    if user_input.lower() == 'exit':
        break

    # Send the user input and chat history to the chat model and get the response
    model_reply = send_chat_message(user_input, chat_history)
    print('ChatGPT: ' + model_reply)
