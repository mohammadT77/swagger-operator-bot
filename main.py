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

# tools = [
#     Tool("Test tool", lambda x: print("X =", x), "A test tool, you should call it whatever you got.")
# ]


# hospital_agent_prompt = hub.pull("hwchase17/openai-functions-agent")
# print(hospital_agent_prompt)

# hospital_agent = create_openai_functions_agent(
#     llm=model,
#     prompt=hospital_agent_prompt,
#     tools=tools,
# )

# hospital_agent_executor = AgentExecutor(
#     agent=hospital_agent,
#     tools=tools,
#     return_intermediate_steps=True,
#     verbose=True,
# )


# print(hospital_agent_executor("What is the name of the hospital?"))