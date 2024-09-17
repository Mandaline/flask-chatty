import openai
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

client = OpenAI()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key, max_tokens=300)


def chat_response(user_query): 

    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"topic": user_query})


def generate_optimized_description(image_url, user_description, title):
    print(f"image_url weeeeeeee: {image_url}")
    # Send the image URL to OpenAI Vision for optimization
    prompt = f"Create a product description for a pair of sunglasses based on the image. The title of the product is {title}. The materials used in the construction of the sunglasses are in the {user_description}. Explain the style, shape, and details of the sunglasses based on what you see in the image. Focus particularly on the shape of the frames. Include the following in the final product description: Shape of the frames: Describe the specific geometry and style of the frames, focusing on whether they are round, square, oval, aviator, or any other shape. Style: Comment on the overall aesthetic, such as whether the sunglasses are modern, retro, sporty, or elegant. Materials: Use the materials input by the user to highlight their quality, texture, and how they contribute to design and functionality."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          {
            "role": "user",
            "content": [
              { "type": "text", "text": prompt},
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
   
    # Extract the optimized description from OpenAI's response
    optimized_description = response.choices[0].message.content

    return optimized_description

def generate_keywords(description):
	keyword_prompt = f"Extract the most important keywords or key phrases from this {description}. Return the keywords as a comma-separated list."

	keyword_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          {
            "role": "user",
            "content": keyword_prompt,
          },
        ],
        max_tokens=100,
    )

	attributes = keyword_response.choices[0].message.content.strip()

	return attributes