"""
Flask web server for the Tour Manager AI Agent.
Holds the API key safely on the server, relays chat to the real agent.
Run with:  python app.py    then open the forwarded port.
"""
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from anthropic import Anthropic

from tools import get_weather, convert_currency

load_dotenv()
client = Anthropic()
app = Flask(__name__)

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city. Use this whenever the user asks about weather, temperature, or conditions in a place.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "The city name."}},
            "required": ["city"],
        },
    },
    {
        "name": "convert_currency",
        "description": "Convert money from one currency to another. Use this whenever the user asks about exchange rates, converting money, per diems, or costs in another currency.",
        "input_schema": {
            "type": "object",
            "properties": {
                "amount": {"type": "number", "description": "The amount to convert."},
                "from_currency": {"type": "string", "description": "3-letter code to convert from."},
                "to_currency": {"type": "string", "description": "3-letter code to convert to."},
            },
            "required": ["amount", "from_currency", "to_currency"],
        },
    },
]

TOOL_FUNCTIONS = {"get_weather": get_weather, "convert_currency": convert_currency}


def run_agent(messages):
    """Run the agent loop. Returns (updated messages, answer text, list of tool traces)."""
    traces = []
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            tools=tools,
            messages=messages,
        )
        if response.stop_reason != "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            answer = "".join(b.text for b in response.content if b.type == "text")
            return messages, answer, traces
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                traces.append(block.name + " " + str(block.input))
                result = TOOL_FUNCTIONS[block.name](**block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })
        messages.append({"role": "user", "content": tool_results})


@app.route("/")
def home():
    return send_from_directory(".", "web.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    history = data.get("history", [])
    user_msg = data.get("message", "")
    history.append({"role": "user", "content": user_msg})
    history, answer, traces = run_agent(history)
    return jsonify({"answer": answer, "traces": traces, "history": history})


if __name__ == "__main__":
    print("Tour Manager web app running. Open the forwarded port to use it.")
    app.run(host="0.0.0.0", port=5000, debug=False)
