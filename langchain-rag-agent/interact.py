# This script allows you to interact with ChatGPT on the command line, storing chat history in a list of messages.
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

chat = ChatOpenAI(model="gpt-4o-mini", temperature=0)
messages = []

while True:
    message = input("> ")
    usr_msg = HumanMessage(content=message)
    messages.append(usr_msg)
    ai_msg = chat(messages)
    print(ai_msg.content)
    messages.append(ai_msg)
