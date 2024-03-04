import openai
import os
from PIL import Image
import requests

# Set your OpenAI API key as an environment variable named 'OPENAI_API_KEY'
openai.api_key = "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"

def generate_image(prompt):
    try:
        response = openai.Image.create(
            model="dall-e-2",  # DALL-E 3 model
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']

        # Download and save the image (adjust filename as needed)
        image_data = requests.get(image_url).content
        with open("generated_image.jpg", "wb") as f:
            f.write(image_data)

        print(f"Image generated and saved as 'generated_image.jpg'")

    except openai.error.OpenAIError as e:
        print(f"Error generating image: {e}")


if __name__ == "__main__":
    prompt = input("Enter your image description: ")
    generate_image(prompt)
