import os
import yaml
import dotenv
from llamaapi import LlamaAPI
from langchain_experimental.llms import ChatLlamaAPI
from core.chatbot import SwaggerChatbot
from langchain.agents import create_openai_functions_agent, Tool, AgentExecutor
from langchain import hub


dotenv.load_dotenv()


swagger = {}
with open("example_server/swagger.yaml") as f:
    swagger = yaml.load(f, Loader=yaml.FullLoader)

llama = LlamaAPI(os.environ.get("LLAMA_API_KEY"))
model = ChatLlamaAPI(client=llama)


chatbot = SwaggerChatbot(swagger, llm=model)

while True:
    user_input = input(">>> ")
    try:
        print("---", chatbot.invoke(user_input))
    except Exception as e:
        print(e)