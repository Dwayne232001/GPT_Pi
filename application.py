import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar
from tkinter import messagebox
import subprocess
import sys
from gtts import gTTS
import openai
import json
import os
import pygame
import threading
import speech_recognition
import pyttsx3
import requests
from PIL import Image, ImageTk
from PIL.Image import Resampling
import io


# Load OpenAI API credentials from a file
api_key_file = "api_key.txt"
with open(api_key_file, "r") as file:
    openai.api_key = file.read().strip()

is_audio_playing = False

def validate_api_key(api_key):
    """Check if the provided OpenAI API key is valid."""
    try:
        response = requests.get(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        if response.status_code == 200:
            # API key is valid
            return True
        else:
            # API key is invalid
            return False
    except Exception as e:
        print(f"Error validating API key: {e}")
        return False

def save_new_api_key(new_api_key):
    # Validate the new API key
    if validate_api_key(new_api_key):
        # Write the new API key to the file if valid
        with open(api_key_file, "w") as file:
            file.write(new_api_key.strip())
        openai.api_key = new_api_key.strip()
        
        # Clear the chat history and first aid history since the API key has changed
        clear_chat_history()
        
        tk.messagebox.showinfo("API Key Changed", "The OpenAI API key has been updated successfully and history cleared.")
    else:
        # Inform the user if the API key is invalid/not present
        tk.messagebox.showerror("API Key Error", "The provided API key is invalid/not present. Please enter a valid API key.")


def open_api_key_window():
    # Create a new top-level window
    api_key_window = tk.Toplevel(window)
    api_key_window.title("Change API Key")
    api_key_window.geometry("300x100")  # Set the size of the window

    # Create an entry widget for the new API key
    new_api_key_entry = tk.Entry(api_key_window, width=40)
    new_api_key_entry.pack(pady=10)

    # Create a save button to save the new API key
    save_button = tk.Button(api_key_window, text="Save", command=lambda: save_new_api_key(new_api_key_entry.get()))
    save_button.pack()

    # Focus the new window and wait for it to close
    api_key_window.transient(window)  # Set as a transient window of the main window
    api_key_window.grab_set()  # Grab the focus
    window.wait_window(api_key_window)  # Wait for the window to close

def validate_api_key_on_startup():
    if not validate_api_key(openai.api_key):
        messagebox.showerror("Invalid API Key", "The current OpenAI API key is invalid. Please enter a valid API key.")
        open_api_key_window()

def clear_chat_history():
    # Delete chat_history.json if it exists
    if os.path.exists("chat_history.json"):
        os.remove("chat_history.json")
    
    # Create a new empty chat_history.json
    with open("chat_history.json", "w") as file:
        history = {"chat": ""}
        json.dump(history, file)
    
    # Clear chat history in the GUI
    chat_history.configure(state=tk.NORMAL)
    chat_history.delete("1.0", tk.END)
    chat_history.configure(state=tk.DISABLED)

def show_ai_speaking_label():
    global ai_frame  # Make ai_frame global to access it in other functions
    # Create a new frame for AI speaking label and stop button
    ai_frame = tk.Frame(window, bg=themes[current_theme]['bg'])
    ai_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

    ai_speaking_label = tk.Label(ai_frame, text="AI is Speaking...",  bg=themes[current_theme]['bg'], fg=themes[current_theme]['fg'], bd=1, relief='raised', font=("Helvetica", 12))
    ai_speaking_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))  # Fill the X direction and expand as necessary

    # Create and pack the stop button inside ai_frame
    stop_button = tk.Button(ai_frame, text="Stop Speaking",  bg=themes[current_theme]['bg'], fg=themes[current_theme]['fg'], bd=1, relief='raised', font=("Helvetica", 12), command=stop_speaking)
    stop_button.pack(side=tk.RIGHT, padx=(0, 0))  # padding to the left

def hide_ai_speaking_label():
    global ai_frame
    for widget in window.winfo_children():
        if isinstance(widget, tk.Label) and widget["text"] == "AI is Speaking...":
            widget.destroy()
        if isinstance(widget, tk.Button) and widget["text"] == "Stop Speaking":
            widget.destroy()
    ai_frame.destroy()

def stop_speaking():
    global is_audio_playing
    if is_audio_playing:
        pygame.mixer.music.stop()

def Text_to_speech(text):
    def worker():
        global is_audio_playing
        # Disable buttons
        send_button.configure(state=tk.DISABLED)
        speech_button.configure(state=tk.DISABLED)

        # Show AI Speaking label
        show_ai_speaking_label()

        # Create and display the progress bar
        progress_bar = Progressbar(window, orient=tk.HORIZONTAL, mode='indeterminate')
        progress_bar.pack(fill=tk.X, padx=10, pady=5)
        progress_bar.start()

        # Perform speech synthesis
        speech = gTTS(text=text, lang='en', tld='com.au')
        speech.save('finalproj.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load('finalproj.mp3')
        is_audio_playing = True
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
        is_audio_playing = False
        pygame.mixer.music.stop()
        pygame.mixer.quit()  # Release the mixer resources
        os.remove('finalproj.mp3')  # Delete the file after playback is complete

        # Stop and remove the progress bar
        progress_bar.stop()
        progress_bar.destroy()

        # Remove AI Speaking label
        hide_ai_speaking_label()

        # Re-enable buttons
        send_button.configure(state=tk.NORMAL)
        speech_button.configure(state=tk.NORMAL)

    t = threading.Thread(target=worker)
    t.start()


def play_sound_pygame(sound_file_path):
    pygame.mixer.init()  # Initialize pygame.mixer
    # Use 'pygame' to load and play the sound
    sound = pygame.mixer.Sound(sound_file_path)
    sound.play()

# Define the 'recogniser' variable globally
recogniser = speech_recognition.Recognizer()

def show_system_message(message):
    chat_history.configure(state=tk.NORMAL)
    chat_history.insert(tk.END, f"System: {message}\n")
    chat_history.configure(state=tk.DISABLED)
    chat_history.see(tk.END)

def send_message(event=None, input_type="text"):  
    try:
        # Disable buttons at the start
        send_button.configure(state=tk.DISABLED)
        speech_button.configure(state=tk.DISABLED)

        # input_type parameter can be used to distinguish between text and speech input
        if input_type == "text":
            message = user_input.get()
            user_input.delete(0, tk.END)
        elif input_type == "speech":
            message = event  # event will be the recognized text
        else:
            # Handle case when input_type is neither "text" nor "speech"
            show_system_message("User hasn't entered a prompt")
            return

        if not message.strip():  # Check if the message is empty after stripping whitespace
            show_system_message("User hasn't entered a prompt")
            return

        chat_history.configure(state=tk.NORMAL)
        chat_history.insert(tk.END, "You: " + message + "\n")
        conversation.append({"role": "user", "content": message})
        chat_history.insert(tk.END, "AI: Typing...\n")
        chat_history.configure(state=tk.DISABLED)
        threading.Thread(target=get_ai_response).start()  # Move the request to a thread

    except Exception as e:
        # Handle exceptions
        print(f"Error in send_message: {e}")
    finally:
        # Re-enable buttons
        send_button.configure(state=tk.NORMAL)
        speech_button.configure(state=tk.NORMAL)


def start_speech_recognition():
    try:
        # Disable buttons at the start
        send_button.configure(state=tk.DISABLED)
        speech_button.configure(state=tk.DISABLED)

        # Create a new recognizer
        recogniser = speech_recognition.Recognizer()

        with speech_recognition.Microphone() as source:
            play_sound_pygame("start.wav")
            recogniser.adjust_for_ambient_noise(source, duration=1)
            audio = recogniser.listen(source)
            play_sound_pygame("end.wav")
            text = recogniser.recognize_google(audio)
            text = text.lower()
            if not text.strip():
                show_system_message("User hasn't spoken a prompt")
                return

            chat_history.configure(state=tk.NORMAL)
            chat_history.insert(tk.END, "You: " + text + "\n")
            conversation.append({"role": "user", "content": text})
            chat_history.insert(tk.END, "AI: Typing...\n")
            chat_history.configure(state=tk.DISABLED)
            threading.Thread(target=get_ai_response).start()

    except Exception as e:
        print(f"Error in start_speech_recognition: {e}")
    finally:
        # Re-enable buttons
        send_button.configure(state=tk.NORMAL)
        speech_button.configure(state=tk.NORMAL)

# Load chat history from file
def load_chat_history():
    try:
        with open("chat_history.json", "r") as file:
            history = json.load(file)
            chat_history.configure(state=tk.NORMAL)
            chat_history.insert(tk.END, history["chat"])
            chat_history.configure(state=tk.DISABLED)
    except FileNotFoundError:
        pass

# Save chat history to file
def save_chat_history():
    with open("chat_history.json", "w") as file:
        history = {"chat": chat_history.get("1.0", tk.END)}
        json.dump(history, file)

# Maintain the conversation state
conversation = []

def get_ai_response():
    # Re-enable buttons at the end
    send_button.configure(state=tk.NORMAL)
    speech_button.configure(state=tk.NORMAL)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            *conversation  # Include all previous messages in the conversation
        ]
    )

    ai_response = response.choices[0].message.content
    chat_history.configure(state=tk.NORMAL)
    chat_history.delete("end-2l linestart", "end-1l lineend")
    chat_history.insert(tk.END, "AI: " + ai_response + "\n")
    chat_history.configure(state=tk.DISABLED)
    chat_history.see(tk.END)

    save_chat_history()  # Save the chat history after each message
    # Check if speak_output is True
    if speak_output.get():
        Text_to_speech(ai_response)  # Get audio response of chat_gpt

def print_value():
    print("Speak Output is now: "+str(speak_output.get()))
    window.focus() #Fixes the speech toggle button focus issue

def on_closing():
    pygame.mixer.quit()
    window.destroy()

# Global flag to indicate if the image generation should proceed
image_generation_active = True

def generate_dalle_image(prompt):
    global image_generation_active
    if not image_generation_active:
        return None

    headers = {
        'Authorization': f'Bearer {openai.api_key}'
    }
    data = {
        'model':"dall-e-3",
        'prompt': prompt,
        'n': 1,
        'size': '1024x1024'
    }
    response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=data)
    if response.status_code == 200:
        image_data = response.json()['data'][0]
        image_url = image_data['url']
        image_response = requests.get(image_url)
        return Image.open(io.BytesIO(image_response.content))
    else:
        print("Error:", response.status_code, response.text)
        return None

def show_image_generation_label():
    global image_generation_frame, image_generation_progress_bar

    # Create a new frame for image generation label, progress bar, and stop button
    image_generation_frame = tk.Frame(window, bg=themes[current_theme]['bg'])
    image_generation_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

    # Frame for label and button
    label_button_frame = tk.Frame(image_generation_frame, bg=themes[current_theme]['bg'])
    label_button_frame.pack(fill=tk.X)

    # Label for "Image is Being Generated..."
    image_generation_label = tk.Label(
        label_button_frame, text="Image is Being Generated...", bg=themes[current_theme]['bg'], fg=themes[current_theme]['fg'], bd=1, relief='raised', font=("Helvetica", 12))
    image_generation_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Stop button
    stop_generation_button = tk.Button(label_button_frame, text="Stop Generating", bg=themes[current_theme]['bg'], fg=themes[current_theme]['fg'], bd=1, relief='raised', font=("Helvetica", 12), command=stop_image_generation)
    stop_generation_button.pack(side=tk.RIGHT, padx=(10,0))

    # Frame for progress bar
    progress_bar_frame = tk.Frame(image_generation_frame, bg=themes[current_theme]['bg'])
    progress_bar_frame.pack(fill=tk.X, pady=10)

    # Progress bar
    image_generation_progress_bar = Progressbar(
        progress_bar_frame, 
        orient=tk.HORIZONTAL, 
        mode='indeterminate'
    )
    image_generation_progress_bar.pack(fill=tk.X, expand=True)
    image_generation_progress_bar.start()

def hide_image_generation_label():
    global image_generation_frame, image_generation_progress_bar
    if image_generation_frame:
        image_generation_frame.destroy()
    if image_generation_progress_bar:
        image_generation_progress_bar.stop()

global generated_image  # Global variable to store the generated image
# Global variable to store the image view button
global view_image_button  

def setup_view_image_button():
    """Setup the view image button."""
    global view_image_button
    view_image_button = tk.Button(button_frame, text="View Generated Image", bg=bg_color, fg=fg_color, bd=1, relief='raised', font=("Helvetica", 12), state=tk.DISABLED)
    view_image_button.pack()

def open_image_window():
    """Open the image in a new popup window."""
    if generated_image:
        new_window = tk.Toplevel(window)
        new_window.title("Generated Image")
        new_image_label = tk.Label(new_window)
        new_image_label.pack()

        # Convert the image to a Tkinter-compatible image format
        tk_new_image = ImageTk.PhotoImage(generated_image)
        new_image_label.configure(image=tk_new_image)
        new_image_label.image = tk_new_image  # Keep a reference

def update_image(image):
    """Update the command for the view image button."""
    global generated_image, view_image_button
    generated_image = image
    if image:
        view_image_button.configure(command=open_image_window, state=tk.NORMAL)
    else:
        view_image_button.configure(state=tk.DISABLED)

def save_image(image, filename):
    """Save the image to the specified filename"""
    image.save(filename)

def handle_image_generation_thread():
    def worker():
        global image_generation_active
        image_generation_active = True
        show_image_generation_label()

        prompt = user_input.get()
        user_input.delete(0, tk.END)
        if prompt:
            image = generate_dalle_image(prompt)
            if image and image_generation_active:
                update_image(image)
                save_image(image, 'generated_image.png')
            else:
                show_system_message("Image generation failed or stopped")
        else:
            show_system_message("No prompt entered")

        hide_image_generation_label()
        image_generation_active = False

    t = threading.Thread(target=worker)
    t.start()

def stop_image_generation():
    global image_generation_active
    image_generation_active = False
    show_system_message("Image generation stopped. Waiting for current process to terminate.")
    hide_image_generation_label()

def toggle_theme():
    global current_theme
    themes_list = list(themes.keys())
    current_index = themes_list.index(current_theme)
    
    # Cycle to the next theme
    current_index = (current_index + 1) % len(themes_list)
    current_theme = themes_list[current_index]

    # Update the window palette
    window.tk_setPalette(background=themes[current_theme]['bg'], foreground=themes[current_theme]['fg'])

    # Update the colors of existing widgets
    for widget in window.winfo_children():
        if isinstance(widget, (tk.Text, tk.Entry, tk.Label, tk.Button)):
            widget.configure(bg=themes[current_theme]['bg'], fg=themes[current_theme]['fg'])

    # Update the checkbox style
    style.configure('Custom.TCheckbutton', background=themes[current_theme]['bg'], foreground=themes[current_theme]['fg'])
    style.map('Custom.TCheckbutton',
              background=[('selected', themes[current_theme]['bg']), ('active', themes[current_theme]['bg'])],
              )

themes = {
    'dark': {'bg': '#333333', 'fg': '#ffffff'},
    'light': {'bg': '#FDF7E4', 'fg': '#161A30'},
    'cactus': {'bg': '#FFFFEC', 'fg': '#597E52'},
    'candy': {'bg': '#FFE5E5', 'fg': '#756AB6'},
    'berry': {'bg': '#F3EDC8', 'fg': '#7D0A0A'},
}

# Add a global variable for text size
text_size = 12

# Function to change the text size
def change_text_size(new_size):
    global text_size
    if new_size<27 and new_size>7:
        text_size = new_size

        # Update the font size of chat history and user input
        chat_history.config(font=("Helvetica", text_size))
        user_input.config(font=("Helvetica", text_size))

        # Update the font size and height of all buttons
        for widget in window.winfo_children():
            if isinstance(widget, (tk.Text, tk.Entry, tk.Label, tk.Button)):
                widget.config(font=("Helvetica", text_size))
                widget.configure(height=int(text_size))

# Create the main application window
window = tk.Tk()
window.attributes('-fullscreen', True)
# Set the initial theme
current_theme = 'dark'
window.tk_setPalette(background=themes[current_theme]['bg'], foreground=themes[current_theme]['fg'])

# This variable will determine if the assistant will speak or not
speak_output = tk.BooleanVar()
speak_output.set(True)  # Setting it to 'True' so it's active by default

window.title("Home Assistant")
window.configure(bg=themes[current_theme]['bg'])

# Dark mode color scheme
bg_color = themes[current_theme]['bg']
fg_color = themes[current_theme]['fg']

# Delay the API key validation until after the main loop starts
window.after(100, validate_api_key_on_startup)

# Create a Frame for buttons
button_frame = tk.Frame(window, bg=bg_color)
button_frame.pack(padx=10, pady=(10,0))

# Create the API key change button
api_key_button = tk.Button(button_frame, text="Change API Key", bg=bg_color, fg=fg_color, bd=1, relief='raised', font=("Helvetica", 12), command=lambda: open_api_key_window())
api_key_button.pack(side=tk.LEFT, padx=(0,10))

# Create the toggle theme button
toggle_theme_button = tk.Button(button_frame, text="Toggle Theme", bg=bg_color, fg=fg_color, bd=1, relief='raised', font=("Helvetica", 12), command=toggle_theme)
toggle_theme_button.pack(side=tk.LEFT, padx=10)

# Create the text size increase button
text_size_button = tk.Button(button_frame, text="Text Size+", bg=bg_color, fg=fg_color, bd=1, relief='raised', font=("Helvetica", 12), command=lambda: change_text_size(text_size + 2))
text_size_button.pack(side=tk.LEFT, padx=10)

# Create the text size decrease button
text_size_button = tk.Button(button_frame, text="Text Size-", bg=bg_color, fg=fg_color, bd=1, relief='raised', font=("Helvetica", 12), command=lambda: change_text_size(text_size - 2))
text_size_button.pack(side=tk.LEFT, padx=10)

# Set the initial theme
initial_theme = 'dark'  # Set this to 'light' for a light theme by default
window.tk_setPalette(background=themes[initial_theme]['bg'], foreground=themes[initial_theme]['fg'])

# Create the chat history text widget
chat_history = tk.Text(window,  bg=bg_color, fg=fg_color, bd=1, relief='raised', font=("Helvetica", 12), state=tk.DISABLED)
chat_history.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create the user input entry widget
user_input = tk.Entry(window,  bg=bg_color, fg=fg_color, bd=1, relief='raised', font=("Helvetica", 12),)
user_input.pack(fill=tk.X, padx=10)

# Create a Frame for buttons
button_frame = tk.Frame(window, bg=bg_color)
button_frame.pack(padx=10, pady=10)

# Create the send button
send_button = tk.Button(button_frame, text="Send", bg=bg_color, fg=fg_color, bd=1, relief='raised', font=("Helvetica", 12), command=send_message)
send_button.pack(side=tk.LEFT)

# Create the speech button
speech_button = tk.Button(button_frame, text="Speak", bg=bg_color, fg=fg_color, bd=1, relief='raised', font=("Helvetica", 12), command=start_speech_recognition)
speech_button.pack(side=tk.LEFT, padx=10)

#Create the generate image button
generate_button = tk.Button(button_frame, text="Generate Image", bg=bg_color, fg=fg_color, bd=1, relief='raised', font=("Helvetica", 12), command=handle_image_generation_thread)
generate_button.pack(side=tk.LEFT, padx=(0, 10))

# Create the refresh button
refresh_button = tk.Button(button_frame, text="Refresh", bg=bg_color, fg=fg_color, bd=1, relief='raised', font=("Helvetica", 12), command=clear_chat_history)
refresh_button.pack(side=tk.LEFT)

# Create the speak checkbox with a raised appearance
checkbox_frame = tk.Frame(button_frame, bd=1, relief='raised', bg=bg_color)
checkbox_frame.pack(side=tk.LEFT, padx=10)

style = ttk.Style()
style.configure('Custom.TCheckbutton', background=bg_color, foreground=fg_color, font=("Helvetica", 12))
style.map('Custom.TCheckbutton',
          background=[('selected', bg_color), ('active', bg_color)],
          )

speak_checkbox = ttk.Checkbutton(checkbox_frame, text="Speak Output", variable=speak_output, style='Custom.TCheckbutton')
speak_checkbox.pack(side=tk.LEFT, padx=10)

# Call this function after checkbox_frame is defined
setup_view_image_button()

# Set the background color of the checkbox frame to adhere to the theme
checkbox_frame.configure(bg=bg_color)

# Bind this function to the checkbox toggling
speak_checkbox.config(command=print_value)

# Bind the Enter key event to the send_message function
window.bind("<Return>", send_message)

# Load chat history on startup
load_chat_history()

window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI main loop
window.mainloop()
