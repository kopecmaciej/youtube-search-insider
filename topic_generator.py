import os
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_youtube_topic():
    topics = ["NLP", "Machine Learning", "Large Language Models"]
    prompt = f"Create a YouTube video topic about {random.choice(topics)}."

    api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a YouTube video topic searcher, create short video topic that will find the most videos possible, max 5 words.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    return  response.choices[0].message.content


print(generate_youtube_topic())
