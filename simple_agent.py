import truststore
truststore.inject_into_ssl()
import os
import openai
from dotenv import load_dotenv
import json
from pathlib import Path 
import httpx

load_dotenv()

# ---------- OpenAI Client ----------
client = openai.OpenAI(
    base_url="https://logiq-service.logitech.io/openai/v1",
    api_key=os.getenv("LOGI_API_KEY"),
)

# ---------- Tools (Plain Python) ----------

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path:str, text:str) -> str:
    """
    This function takes text as input and writes it to a file.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(text, encoding="utf-8")

    return "Success" # simple way to check things went right

def fetch_web(url:str) -> str:
    """
    This function allows to fetch content from a web page.
    """
    response = httpx.get(url) 
    response.raise_for_status()
    return response.text # will be the HTML (same as view page source)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file from disk",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text to a text file on disk",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "text": {"type": "string"}
                },
                "required": ["path", "text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_web",
            "description": "Fetch content from a web page",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"}
                },
                "required": ["url"]
            }
        }
    }
]

TOOLS_MAP = {
    "read_file": read_file,
    "write_file": write_file,
    "fetch_web": fetch_web
}

# ---------- Agent ----------
state = {
    "completed_steps": [],
    "facts": {}
}

def run_agent(goal: str): 
    # similar structure to what we have for generative AI
    # except now we add the tools aspect
    messages = [
        {"role": "system", "content": (
            "You are a helpful agent."
            "Use tools to achieve the goal."
            "When the goal is complete, reply with DONE."
            ),
        },
        {"role": "user", "content": goal},
    ]
    i=0
    while True:
        print(f"{i} ---------------------------------------------------------")
        i+=1
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=256,
        )
        # model answer
        message = response.choices[0].message

        print("\n=== MODEL RESPONSE ===")
        print(message)

        # check that we're done
        if message.content and "DONE" in message.content:
            print("\nGOAL COMPLETED!")
            return
        
        # check that a tool was called
        if not message.tool_calls:
            print("\nNo tool was called.")
            return

        # handle one tool call per step
        call = message.tool_calls[0]
        tool_name = call.function.name
        args = json.loads(call.function.arguments)

        # if a tool was called, call it
        print("\n=== TOOL CALL ===")
        print("Tool:", tool_name)
        print("Args:", args)

        tool_fct = TOOLS_MAP.get(tool_name)
        if tool_fct is None:
            raise ValueError(f"Unknown tool: {tool_name}")

        result = tool_fct(**args)
        print("\n=== TOOL RESULT ===")
        print(result)

        # update state (memory)
        state["completed_steps"].append({
            "tool": tool_name,
            "args": args
        })


        state["facts"][tool_name] = result

        messages.append({
            "role": "assistant",
            "content": (
                "Current agent state:\n"
                f"- Goal: {goal}\n"
                f"- Completed steps: {state['completed_steps']}\n"
                f"- Known facts: {state['facts']}\n\n"
                "Based on this state, decide the next best action. "
                "If the goal is complete, reply with DONE."
            )
        })


# ---------- Run ----------

if __name__ == "__main__":
    run_agent("Explain what the EMN country factsheets (https://home-affairs.ec.europa.eu/networks/european-migration-network-emn/emn-publications/country-factsheets_en) are and store a simple description in data/emn.txt")