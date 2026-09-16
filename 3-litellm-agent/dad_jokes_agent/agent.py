import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="openai/gpt-5.6-terra",
    api_key=os.getenv("ANY_MODEL_API")
)

def get_dad_jokes() -> str:
    jokes =[
        "why did the chicken cross the road? to get to the other side!",
        "what do you call a belt made of watches? a waist of time.",
        "what do you call a fake spagetti? an impasta!"
    ]
    return random.choice(jokes)

root_agent = Agent(
    name="dad_jokes_agent",
    model=model,
    description="Dad jokes agent",
    instruction="""
    You are a helpful assistant that can tell dad jokes. Only use the tool 'get_dad_jokes' to tell dad jokes.
    """,
    tools=[get_dad_jokes]
)