import openai
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def  chat_response(user_query): 
    load_dotenv()

    openai.api_key = os.environ.get("OPENAI_API_KEY")

    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai.api_key, max_tokens=300)


    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

    chain = prompt | llm | StrOutputParser()


    return chain.invoke({"topic": user_query})