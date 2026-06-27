from dotenv import load_dotenv
from anthropic import Anthropic
from tools import get_weather, convert_currency

load_dotenv()
client = Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city. Use this whenever the user asks about weather, temperature, or conditions in a place.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name, e.g. Osaka or Berlin."}
            },
            "required": ["city"],
        },
    },
    {
        "name": "convert_currency",
        "description": "Convert money from one currency to another. Use this whenever the user asks about exchange rates, converting money, per diems, or costs in another currency.",
        "input_schema": {
            "type": "object",
            "properties": {
                "amount": {"type": "number", "description": "The amount to convert, e.g. 18000."},
                "from_currency": {"type": "string", "description": "3-letter code to convert from, e.g. JPY."},
                "to_currency": {"type": "string", "description": "3-letter code to convert to, e.g. USD."},
            },
            "required": ["amount", "from_currency", "to_currency"],
        },
    },
]

TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "convert_currency": convert_currency,
}


def run_agent(user_message):
    messages = [{"role": "user", "content": user_message}]
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            tools=tools,
            messages=messages,
        )
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print("   [Claude decided to call " + block.name + " with " + str(block.input) + "]")
                result = TOOL_FUNCTIONS[block.name](**block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    question = "We're in Osaka for load-in. What's the weather, and how much is the 18000 JPY catering buyout in USD?"
    print("You: " + question + "\n")
    answer = run_agent(question)
    print("\nTour Manager: " + answer)
