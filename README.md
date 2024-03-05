# GPT_Pi
ChatGPT for a Raspberry Pi

This project creates a versatile AI-powered home assistant specifically designed to run on a Raspberry Pi. It leverages OpenAI's language models (GPT-4) for intelligent assistance and interaction.

**Technologies Used**

- **Tkinter**: A standard GUI (Graphical User Interface) library for Python, used for creating the application's window, buttons, text input fields, and other UI elements.
- **Threading**: A module for running tasks in separate threads to prevent the UI from becoming unresponsive during operations such as speech synthesis or API requests.
- **gtts (Google Text-to-Speech)**: A library that allows Python to interface with Google's Text to Speech API, converting text into spoken voice.
- **OpenAI**: Specifically, this refers to the integration with OpenAI's API, suggesting the use of models such as GPT-3 or GPT-4 for generating text-based responses.
- **json**: A module for parsing and generating JSON data, used here for loading and saving chat history in a JSON file format.
- **os**: A module providing a way to use operating system dependent functionality like file operations (e.g., reading, writing, and deleting files).
- **pygame**: A library used for creating video games, which includes the ability to play audio files. In this context, it is used for playing sound effects and synthesized speech.
- **speech_recognition**: A library for performing speech recognition, converting spoken words into text by using various APIs such as Google Speech Recognition.
- **pyttsx3**: A text-to-speech conversion library in Python that works offline. Unlike gtts, it does not require an internet connection.
- **requests**: A library for making HTTP requests to communicate with APIs, used here for validating the OpenAI API key and fetching images from DALL-E.
- **PIL (Python Imaging Library), also known as Pillow**: Used for opening, manipulating, and saving many different image file formats. This is useful for processing and displaying images generated by DALL-E within the application.
- **io**: A module that allows for dealing with various types of I/O (Input/Output). In this context, it's used for handling image data fetched from a web request.


**Features** 

* Text-based interaction
* Voice-based interaction
* Image generation

**Prerequisites**

* Raspberry Pi (Model 3 or newer recommended)
* Raspberry Pi OS
* Python 3
* OpenAI API key 

**Installation Instructions**

1. **Set up an OpenAI API Key:**
   * Visit the OpenAI website ([https://openai.com/api/](https://platform.openai.com/api-keys)) and create an account.
   * Navigate to your account settings and obtain your API key.

2. **Install Dependencies**
   ```bash
   sudo apt-get update
   sudo apt upgrade -y
   sudo apt-get install python3-pip 
   pip3 install openai speechrecognition pygame requests 
   python3 -m pip install --upgrade pip setuptools wheel
   pip3 install gTTS pygame SpeechRecognition pyttsx3 Pillow requests
   sudo apt install python3-tk -y
   pip3 install openai

3. **Clone the Project Repository:**
   ```bash
   git clone https://github.com/Dwayne232001/GPT_Pi.git your-repo-name

4. **Run the Project:**
   ```bash
   cd your-repo-name
   python3 application.py 

5. **Configure Your API Key:**
   * Run the application, it will automatically ask you for your API key, enter your API key there.

**Usage**

* **Text-based Interaction:** Type in prompts or commands and the system will provide text-based responses.
* **Voice-based Interaction:** Speak your prompts and the system will process them, providing either text or spoken responses (depending on your implementation).
* **Image Generation:** Describe a scene or object and the system will generate an image.

**Example Interactions**

* "What's the weather like in London?"
* "Generate an image of a cat riding a unicorn" 

**Support**

For questions or help, please open an issue on the project's GitHub repository: https://github.com/Dwayne232001/GPT_Pi.git

**Important Notes**

* **API Key Security:** Do not share your OpenAI API key publicly. Keep it in a secure location, such as an environment variable.
