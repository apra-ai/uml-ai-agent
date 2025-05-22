# AI UML Agent

This repository provides an AI-powered assistant for **creating, editing, and visualizing UML class diagrams** using natural language.  
It combines OpenAI or Anthropic LLMs, LangChain tools, and PlantUML for a seamless UML modeling experience.

---

## Features

- **Natural Language Interface:**  
  Describe your UML classes, attributes, functions, and relationships in plain English or German.
- **Interactive Multi-turn Dialog:**  
  The agent can ask follow-up questions if information is missing or unclear.
- **Automatic Diagram Generation:**  
  All changes are stored in a JSON model and converted to PlantUML for visualization.
- **Extensible Tooling:**  
  Easily add new tools for more UML features.

---

## How it works

1. **User Input:**  
   You describe your UML diagram (e.g., "Create a class Animal with attribute age of type int. Connect Animal to Dog.").
2. **AI Agent:**  
   The agent parses your request, asks for missing details if needed, and updates the UML model.
3. **Diagram Rendering:**  
   The model is converted to PlantUML and rendered as a diagram.

---

## Technologies Used

- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenAI](https://platform.openai.com/) or [Anthropic](https://www.anthropic.com/)
- [PlantUML](https://plantuml.com/)

---

## Setup & Usage

### 1. Clone the repository

```bash
git clone https://github.com/apra-ai/uml-ai-agent.git
cd ai-uml-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your API keys

Create a `.env` file in the project root with the following content:

```env
OPENAI_API_KEY="your-openai-key"
ANTHROPIC_API_KEY="your-anthropic-key"
```

You can use either OpenAI or Anthropic (Claude) as your LLM provider.

### 4. Run the agent

```bash
python main.py
```

Follow the prompts and describe your UML diagram in natural language.  
The agent will interactively ask for more information if needed and update the UML model.

---

## Example

**Input:**
```
Create a class Animal with attribute age of type int.
Create a class Dog.
Connect Dog to Animal.
```

**Result:**  
- The agent creates the classes and relationship in `uml/uml.json`.
- The PlantUML code is generated in `uml/diagram.uml`.
- The diagram is rendered via PlantUML.

---

## File Structure

```
.
├── main.py                # Main entry point for the AI agent
├── tools.py               # Tool definitions for manipulating the UML model
├── uml/
│   ├── uml.json           # JSON representation of the UML model, this folder gets generated
│   └── diagram.uml        # Generated PlantUML code, this folder gets generated
├── .env                   # API keys (not tracked in git)
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## Notes

- Make sure you have a working internet connection for API access and PlantUML rendering.
- The agent supports both English and German input.
- You can extend the tools in `tools.py` to support more UML features.

---

## License

MIT License

---

**This project is ideal for students, developers, and anyone who wants to quickly create UML diagrams using AI!**
