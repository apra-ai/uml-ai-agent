# main.py
# This script creates an AI agent that can generate and edit UML diagrams based on user input.
# It uses OpenAI or Anthropic LLMs, LangChain tools, and PlantUML for rendering diagrams.
# The agent supports multi-turn conversations and can ask the user for more information if needed.

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import (
    create_class_tool,
    create_connection_tool,
    get_uml_diagram_tool,
    add_attribute_to_class_tool,
    add_function_to_class_tool,
    delete_class_tool,
    delete_attribute_tool,
    delete_function_tool,
    delete_connection_tool,
    delete_attribute,
    delete_connection,
    delete_function,
    delete_class,
    create_class,
    create_connection,
    add_attribute_to_class,
    add_function_to_class,
    get_uml_diagram,
)
from plantuml import PlantUML
import json
from pydantic import BaseModel

# Model names for LLMs
GPT_MODEL = "gpt-3.5-turbo"
CLAUDE_MODEL = "claude-3-7-sonnet-20250219"

# List of available tools for the agent
tools_available = [
    create_class_tool,
    create_connection_tool,
    get_uml_diagram_tool,
    add_attribute_to_class_tool,
    add_function_to_class_tool,
    delete_class_tool,
    delete_attribute_tool,
    delete_function_tool,
    delete_connection_tool
]

# Create a Pydantic model for the agent's response
class UMLResponse(BaseModel):
    tools_used: list[str]

def ai_agent():
    """
    This function creates and runs an AI agent that interacts with the user to build UML diagrams.
    The agent can ask follow-up questions if information is missing and uses the provided tools to modify the UML model.
    """
    # Load API keys and environment variables from .env file
    load_dotenv()

    # Choose the LLM agent (Anthropic Claude or OpenAI GPT)
    # llm = ChatOpenAI(model=GPT_MODEL)
    llm = ChatAnthropic(model=CLAUDE_MODEL)

    # Define the output format using a Pydantic parser
    parser = PydanticOutputParser(pydantic_object=UMLResponse)

    # Design the prompt template for the agent and fill in format instructions
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an assistant that exclusively helps with creating and editing UML classes.
                If you need more information or something is unclear, ask the user specific questions before proceeding.
                Answer the user query and use available tools if needed.
                Return the output strictly in this format and do not add any other text.
                {format_instructions}
                """,
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    # Create the agent with LLM, prompt template, and available tools
    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools_available
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools_available, verbose=True)

    # Start the conversation loop with the user
    query = input("What can I help you create? ")
    chat_history = []
    while True:
        # Invoke the agent with the current query and chat history
        raw_response = agent_executor.invoke({"query": query, "chat_history": chat_history})
        output = raw_response.get("output")[0]["text"]
        # Detect if the agent is asking a follow-up question
        if "?" in output or "please provide" in output.lower():
            user_reply = input("Your answer: ")
            chat_history.append({"role": "user", "content": query})
            chat_history.append({"role": "assistant", "content": output})
            query = user_reply
        else:
            break

    # Try to parse the agent's response and print the structured output
    try:
        structured_response = parser.parse(output)
        print(structured_response)
    except Exception as e:
        print("Error parsing response", e, "Raw Response - ", raw_response)

def process_uml(json_path="uml/uml.json", plantuml_path="uml/diagram.uml"):
    """
    Converts the UML JSON structure to PlantUML code and writes it to a file.
    Also sends the file to the PlantUML server for rendering.
    """
    first_line = "@startuml"
    last_line = "@enduml"
    with open(json_path, "r") as f:
        data = json.load(f)

    lines = []
    # Generate classes with attributes and functions
    for class_name, class_data in data.get("classes", {}).items():
        attributes = class_data.get("attributes", [])
        functions = class_data.get("functions", [])
        lines.append(f"class {class_name} {{")
        # Add attributes
        for attr_name in attributes:
            attr_type = attributes[attr_name]["type"]
            lines.append(f"{attr_type} {attr_name}")
        # Add functions
        for function_name in functions:
            lines.append(f"{function_name}()")
        lines.append("}")
    # Generate relationships between classes
    for from_class, class_data in data.get("classes", {}).items():
        connections = class_data.get("connections", {}) if class_data else {}
        for to_class, conn_data in connections.items():
            lines.append(f"{from_class} --|> {to_class}")

    # Write the PlantUML code to file
    with open(plantuml_path, "w") as f:
        f.write(first_line + "\n")
        for line in lines:
            f.write(line + "\n")
        f.write(last_line + "\n")
    
    # Send the PlantUML file to the PlantUML server for rendering
    server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
    server.processes_file(plantuml_path)

    return f"UML JSON converted to PlantUML and saved in {plantuml_path}"

# Run the AI agent and process the UML after the conversation
if __name__ == "__main__":
    ai_agent()
    process_uml()
