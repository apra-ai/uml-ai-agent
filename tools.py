# tools.py
# This file defines all tools (functions) for manipulating the UML model and exposes them as LangChain Tools.
# Each tool operates on the uml/uml.json file and updates the UML structure accordingly.

from langchain.tools import Tool, StructuredTool
from pydantic import BaseModel
import json

# Tool: Create a new class in the UML model
def create_class(class_name: str):
    data_file_path = "uml/uml.json"

    with open(data_file_path, "r") as datei:
        data = json.load(datei)
    
    if class_name in data["classes"]:
        return "Class already exists in the diagram.uml file."
    
    data["classes"][class_name] = {}
    data["classes"][class_name]["connections"] = {}
    
    with open(data_file_path, "w") as datei:
        json.dump(data, datei, indent=4)

    return f"Class {class_name} created in diagram.uml file."

create_class_tool = Tool(
    name="create_class",
    func=create_class,
    description="Saves new Class into uml file.",
)

# Tool: Create a connection between two classes
def create_connection(connection_from_first_class: str, connection_to_second_class: str):
    data_file_path = "uml/uml.json"

    with open(data_file_path, "r") as datei:
        data = json.load(datei)
    
    if not(connection_from_first_class in data["classes"]):
        return "Class from which the connection starts does not exist in the diagram.uml file. Create it first."
    if not(connection_to_second_class in data["classes"]):
        return "Class to which the connection points does not exist in the diagram.uml file. Create it first."
    
    data["classes"][connection_from_first_class]["connections"][connection_to_second_class] = {"type": "normal"}

    with open(data_file_path, "w") as datei:
        json.dump(data, datei, indent=4)

    return f"Created connection between {connection_to_second_class} to {connection_from_first_class} in diagram.uml file."

class ConnectionInput(BaseModel):
    connection_from_first_class: str
    connection_to_second_class: str

create_connection_tool = StructuredTool(
    name="create_connection",
    func=create_connection,
    description=(
        "Creates a connection between two classes in the diagram.uml file. "
        "Parameter 1 (connection_from_first_class): The class from which the connection starts. "
        "Parameter 2 (connection_to_second_class): The class to which the connection points. "
        "Both parameters are required and must be class names that already exist in the UML diagram."
    ),
    args_schema=ConnectionInput,
)

# Tool: Get the current UML diagram as PlantUML code
def get_uml_diagram(_=None):
    with open("uml/diagram.uml", "r") as f:
        uml_code = f.read()
    return uml_code

get_uml_diagram_tool = Tool(
    name="get_uml_diagram",
    func=get_uml_diagram,
    description="Gets the current UML diagram from the diagram.uml file, to see the current state of the diagram. This is a read-only operation and does not modify the diagram.",
)

# Tool: Add an attribute to a class
def add_attribute_to_class(attribute_name: str, attribute_type: str, class_name: str):
    data_file_path = "uml/uml.json"

    with open(data_file_path, "r") as datei:
        data = json.load(datei)
    
    if not(class_name in data["classes"]):
        return "Class does not exist in the diagram.uml file. Create it first."
    
    if "attributes" not in data["classes"][class_name]:
        data["classes"][class_name]["attributes"] = {
            attribute_name: {
                "type": attribute_type
            }
        }
    else:
        data["classes"][class_name]["attributes"][attribute_name] ={
                    "type": attribute_type
            }
    
    with open(data_file_path, "w") as datei:
        json.dump(data, datei, indent=4)

    return f"Added attribute {attribute_name} of type {attribute_type} to class {class_name} in diagram.uml file."

class AttributesInput(BaseModel):
    attribute_name: str
    attribute_type: str
    class_name: str

add_attribute_to_class_tool = StructuredTool(
    name="add_attribute_to_class",
    func=add_attribute_to_class,
    description=(
        "Adds an attribute to a class in the diagram.uml file. "
        "Parameter 1 (attribute_name): The name of the attribute to be added. "
        "Parameter 2 (attribute_type): The type of the attribute to be added. "
        "Parameter 3 (class_name): The name of the class to which the attribute will be added. "
    ),
    args_schema=AttributesInput,
)

# Tool: Add a function to a class
def add_function_to_class(function_name: str, class_name: str):
    data_file_path = "uml/uml.json"

    with open(data_file_path, "r") as datei:
        data = json.load(datei)
    
    if not(class_name in data["classes"]):
        return "Class does not exist in the diagram.uml file. Create it first."
    
    if "functions" not in data["classes"][class_name]:
        data["classes"][class_name]["functions"] = {
            function_name: {}
        }
    else:
        data["classes"][class_name]["functions"][function_name] ={}
    
    with open(data_file_path, "w") as datei:
        json.dump(data, datei, indent=4)

    return f"Added function {function_name} to class {class_name} in diagram.uml file."

class FunctionInput(BaseModel):
    function_name: str
    class_name: str

add_function_to_class_tool = StructuredTool(
    name="add_function_to_class",
    func=add_function_to_class,
    description=(
        "Adds a function to a class in the diagram.uml file. "
        "Parameter 1 (function_name): The name of the function to be added. "
        "Parameter 2 (class_name): The name of the class to which the function will be added. "
    ),
    args_schema=FunctionInput,
)
