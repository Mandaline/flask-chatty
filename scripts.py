from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from openai import OpenAI

client = OpenAI()

# Load environment variables
load_dotenv()

# Set OpenAI API key (ensure it's in your .env file)
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI Chat Model
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key, max_tokens=300)

# Function to generate description using LangChain and OpenAI
def generate_image_description(image_url):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          {
            "role": "user",
            "content": [
              { "type": "text", "text": "Describe the shape, style and color of the sunglasses in this image." },
              {
                "type": "image_url",
                "image_url": {
                  "url": image_url,
                },
              },
            ],
          },
        ],
        max_tokens=300,
    )
    description = response.choices[0].message["content"]
    return description

# Example usage
image_url = "../chatty-flask/images/skater-cat.webp"
description = generate_image_description(image_url)

print("Description:", description)
