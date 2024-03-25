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
        topics = [
            "NLP",
            "Machine Learning",
            "Large Language Models",
            "Deep Learning",
            "Computer Vision",
            "Reinforcement Learning",
            "Natural Language Generation",
            "Data Science",
            "Neural Network Architectures",
            "Generative Adversarial Networks",
            "Robotics and Automation",
            "Quantum Computing",
            "Bioinformatics",
            "Speech Recognition",
            "Predictive Analytics",
            "Internet of Things",
            "Blockchain Technology",
            "Augmented Reality",
        ]

        selected_topics = random.sample(topics, min(len(topics), 3))
        prompt = f"Create a YouTube video topics about {', '.join(selected_topics)}, number of topics: {len(selected_topics)}"

        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a YouTube video topic searcher, create short video topic that will find the most videos possible, max 5 words. Your input will be a list of 3 topics separated by comma, output will be an array of topics sepearted by comma",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model="gpt-3.5-turbo",
        )

        return response.choices[0].message.content
