import os
import random
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class OpenAIClient:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key is None:
            raise Exception("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=self.api_key)

    def generate_youtube_topic(self):
        topics = ["NLP", "Machine Learning", "Large Language Models"]
        prompt = f"Create a YouTube video topic about {random.choice(topics)}."

        response = self.client.chat.completions.create(
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

