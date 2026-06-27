"""
Flask web server for the Tour Manager AI Agent.
Holds the API key safely on the server, relays chat to the real agent.
Run with:  python app.py    then open the forwarded port (set it to Public).
"""
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from anthropic import Anthropic

from tools import get_weather, convert_currency

load_dotenv()
client = Anthropic()
app = Flask(__name__)

# Keep conversation history on the server, keyed simply for this single-user demo.
conversation = []

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


def run_agent():
    """Run the agent loop using the server-side conversation. Returns (answer_text, traces)."""
    traces = []
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            tools=tools,
            messages=conversation,
        )
        if response.stop_reason != "tool_use":
            conversation.append({"role": "assistant", "content": response.content})
            answer = "".join(b.text for b in response.content if b.type == "text")
            return answer, traces
        conversation.append({"role": "assistant", "content": response.content})
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
        conversation.append({"role": "user", "content": tool_results})


@app.route("/")
def home():
    return send_from_directory(".", "web.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    if data.get("reset"):
        conversation.clear()
    conversation.append({"role": "user", "content": user_msg})
    answer, traces = run_agent()
    # Only send back plain strings, never raw Anthropic objects.
    return jsonify({"answer": answer, "traces": traces})


if __name__ == "__main__":
    print("Tour Manager web app running. Open the forwarded port (set it Public) to use it.")
    app.run(host="0.0.0.0", port=5000, debug=False)
