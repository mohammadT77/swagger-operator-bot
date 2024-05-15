# Api-chatbot

LLM Operator Chatbot with LangChain

## Overview
This project implements an LLM Operator Chatbot using LangChain. The chatbot interacts with users to perform various actions based on the provided requests. 

## Technologies Used
- LangChain
- Python
- YAML
- dotenv

## Setup
- Install dependencies
```sh
pip install -r requirements.txt
```
- Run the example server in a terminal
```sh
python example_server/app.py
```
- Run chatbot CLI in another terminal
```sh
python main.py
```


## Usage
- Input user queries to interact with the chatbot

## License
This project is licensed under the [License Name] License - see the LICENSE.md file for details.

## Example of conversations
```
>>> Hey I have a problem with my services
--- {
"action": "GET-/service",
"parameters": {},
"confidence": 60.0
}

Please provide more information about the problem you're experiencing with your services.
>>> I want to deactivate my current service and activate another
--- {
  "action": "deactivate",
  "parameters": {
    "service_id": "unknown"
  },
  "confidence": 80.0
}

{
  "action": "activate",
  "parameters": {
    "service_id": "unknown"
  },
  "confidence": 80.0
}

Please provide the service IDs for deactivation and activation.
>>> deactivate my current service 
--- {
  "action": "DELETE-/service/deactivate",
  "parameters": {
    "service_id": null
  },
  "confidence": 90.0
}

Please provide the service ID to deactivate.
>>> what are my current active services
--- Based on your request to retrieve a list of active services, I've obtained the following result:

You have a total of 5 active services. Four of them have the same ID ("1") and are named "Service One". The fifth service has an ID of "3" and is named "Service Three".

Here's a summary of the active services:

* Service One (ID: 1) - 4 instances
* Service Three (ID: 3) - 1 instance

Is there anything else you'd like to do or inquire about? Would you like to retrieve more information about a specific service, or perhaps perform another action?
>>> can you please deactivate my service 3
--- Hi there!

I've successfully deactivated your Service 3 as per your request. The result shows that the operation was completed successfully, with a status code of 200, which indicates a successful response. The response message is: `{"message": "Service deactivated successfully"}`.

This confirms that your service has been deactivated. If you need any further assistance or have other requests, please feel free to ask!
>>> and also please deactivate first of service 1
--- I'd be happy to help you understand the result.

Based on your request, I deactivated the first service as per your instruction. The result shows that the deactivation was successful, with a status code of 200, which indicates a successful operation. The response message is "Service deactivated successfully", confirming that the service has been deactivated.

Is there anything else you'd like me to assist you with? Would you like to deactivate any other services or perform a different action?
>>> what services you have in your company?
--- Based on your request, I've retrieved a list of all available services in our company. Here's the result:

We have a total of 4 services:

1. Service One with ID 1
2. Service Two with ID 2
3. Service Three with ID 3
4. Service Four with ID 4

Please note that the status of each service is not specified in this result, but we can retrieve that information if needed.

Is there anything else you'd like to know or any other action you'd like to take? Would you like to retrieve more information about a specific service, or perhaps perform a different action?
>>> now please activate the service 4 for me
--- I've successfully activated Service 4 for you. The result shows that the service was activated successfully, as indicated by the 200 status code and the confirmation message "Service activated successfully".

Is there anything else I can assist you with? Would you like to activate another service, check the status of a service, or perform a different action?
```