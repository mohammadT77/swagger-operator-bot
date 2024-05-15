from .parse_swagger import get_all_actions
import json
from typing import Dict, Any
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.prompts import (
    PromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models.base import BaseChatModel
import requests





# messages = [
#     SystemMessage(
#         content="""You're an operator chatbot for a organization. 
#         A detailed actions description will be given to you and 
#         you must first try to understand what clients want and perform the required actions as described."""
#     ),
#     HumanMessage(
#         content="""Hi."""
#     ),
# ]

# try:
#     print(model.invoke(messages))
# except Exception as e:
#     print(e)

class SwaggerChatbot:
    def __init__(self, swagger, llm: BaseChatModel, **options ) -> None:
        self.swagger = swagger
        self.llm = llm
        self.options = options
        self._history = []

    def invoke(self, messages: str) -> Any:
        # Step 1: Interpret the client messages using the LLM
        prompt = self.create_prompt(messages)

        try:
            response = self.llm.invoke(prompt)
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            e.add_note("Failed to process your message, please try again.")
            raise e

        # Step 2: Parse the LLM response to determine the action
        try:
            action, params, conf = self.parse_response(response.content)
        except ValueError as e:
            # self._history.append(response.content)
            return e.args[0]

        # Step 3: Map the action to the corresponding Swagger endpoint
        # endpoint, method = self.map_action_to_endpoint(action)
        method, _, endpoint = action.partition("-")

        # Step 4: Perform the action using the appropriate HTTP method
        result = self.perform_action(endpoint, method, params)

        prompt = self.create_prompt(messages, {
            "action":json.dumps(get_all_actions(self.swagger)[action]), 
            "result":json.dumps({"text":result.text,"status_code:":result.status_code}),
        })

        try:
            return self.llm.invoke(prompt).content
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            e.add_note("Failed to process your message, please try again.")
            raise e
        

    def create_prompt(self, messages: str, result=None) -> str:
        # Create a prompt that includes the Swagger specification to ask the LLM for the action to perform
        swagger_tools = json.dumps(get_all_actions(self.swagger))

        history_messages = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self._history])

        confidence_threshold = 0.8 * 100

        template = """
        You are our company chatbot interfacing with the following Swagger API specification:
        {swagger_tools}

        Here is the conversation history:
        {history_messages}

        User Input: {messages}

        """
        if result is None:
            template += """
            Based on the above, determine the action to perform and the necessary parameters.
            Respond with the action, parameters, and confidence in JSON format. If confidence is less than {confidence_threshold} percent, ask for more clarifications.
            """
            prompt_template = PromptTemplate(template=template, input_variables=["messages", "swagger_tools", "confidence_threshold", "history_messages"])
            prompt = prompt_template.format(messages=messages, swagger_tools=swagger_tools, confidence_threshold=confidence_threshold, history_messages=history_messages)
        else:
            template += """
            The action taken:
            {action}

            And the result is:
            {result}

            Now, take a look at the result and explain it to them. Also ask them if they want other things to do.
            """
            prompt_template = PromptTemplate(template=template, input_variables=["messages", "swagger_tools", "history_messages", "action", "result"])
            prompt = prompt_template.format(messages=messages,
                                            swagger_tools=swagger_tools,
                                            history_messages=history_messages, 
                                            action=json.dumps(result["action"]),
                                            result=json.dumps(result["result"]))

        return prompt
    
    def parse_response(self, response: str) -> (str, Dict[str, Any]):
        # Parse the LLM response to extract the action and parameters
        try:
            response_json = json.loads(response)
            action = response_json.get("action")
            params = response_json.get("parameters", {})
            conf = response_json.get("confidence", {})
        except Exception:
            msg = response.replace(r'\{(\s|\r|\n)*"action"(.|\s|\r|\n)*\}', "")
            raise ValueError(msg)

        return action, params, conf
    
    def map_action_to_endpoint(self, action: str) -> (str, str):
        # Map the action to the corresponding Swagger endpoint and HTTP method
        for path, methods in self.swagger["paths"].items():
            for method, details in methods.items():
                if details.get("operationId") == action:
                    return path, method.upper()

        raise ValueError(f"Action '{action}' not found in Swagger endpoints")

    def perform_action(self, endpoint: str, method: str, params: Dict[str, Any]) -> Any:
        url = self.swagger["servers"][0]["url"] + endpoint
        headers = {"Content-Type": "application/json"}

        # TODO: use general request here instead of ifelse
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=params)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, json=params)
        else:
            raise ValueError(f"Unsupported HTTP method '{method}'")

        return response

