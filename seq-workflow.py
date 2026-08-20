import logging
from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import SequentialBuilder
from agent_framework_devui import serve

load_dotenv()


logging.basicConfig(level=logging.INFO) # APIKEY

client = OpenAIChatClient()

researcher = Agent(
     client=client,
     name="Researcher",
     instructions=(
        "You are a research analyst. Given a topic, return exactly 5 key facts "
        "as a numbered list. Be factual and concise."
    )
)

summarizer = Agent(
    client=client,
    name="Summarizer",
    instructions=(
        "You are a summarizer. Take the numbered facts and write " 
        "a single, 3-sentence paragraph summary."
    )
)

linkedin_writer = Agent(
    client=client,
    name="LinkedInWriter",
    instructions=(
        "You are a LinkedIn content creator. Take the summary and write an engaging "
        "LinkedIn post: hook opening, 3 emoji takeaways, and a question at the end. "
        "Max 200 words."
    ),
)

workflow = SequentialBuilder(
    participants= [
        researcher,
        summarizer,
        linkedin_writer
    ],
    output_from="all"
).build()

if __name__ == "__main__":
    serve(entities=[workflow], auto_open=True)