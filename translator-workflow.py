import logging
from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import ConcurrentBuilder
from agent_framework_devui import serve

load_dotenv ()

logging.basicConfig(level=logging.INFO)

client = OpenAIChatClient()

urdu_translator = Agent(
    client = client,
    name = "UrdrTranslator",
    instructions="Translate the given English text to Urdu. Return ONLY the Urdu translation.",
)

arabic_translator = Agent(
    client = client,
    name = "ArabicTranslator",
    instructions="Translate the given English text to Arabic. Return ONLY the Arabic translation.",
)

spanich_translator = Agent(
    client = client,
    name = "SpanishTranslator",
    instructions="Translate the given English text to Spanish. Return ONLY the Spanish translation.",
)

workflow = ConcurrentBuilder(
    participants= [
        urdu_translator,
        arabic_translator,
        spanich_translator
    ],
    output_from="all"
).build()

if __name__ == "__main__":
    serve(entities=[workflow], auto_open=True)