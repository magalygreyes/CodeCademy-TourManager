from dotenv import load_dotenv
from anthropic import Anthropic

from tools import get_weather   # reuse the tool you already tested

load_dotenv()
client = Anthropic()

# 1. TELL Claude what tools exist. This is a description, not the code.
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city. Use this whenever the user asks about weather, temperature, or conditions in a place.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name, e.g. 'Osaka' or 'Berlin'.",
                }
            },
            "required": ["city"],
        },
    }
]

# 2. MAP each tool name to the real Python function.
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
}


def run_agent(user_message: str):
    """Run the agent loop until Claude reaches a final answer."""

    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            tools=tools,
            messages=messages,
        )

        # If Claude did NOT ask for a tool, it's done. Return the answer.
        if response.stop_reason != "tool_use":
            return "".join(
                block.text for block in response.content if block.type == "text"
            )

        # Claude wants a tool. Save its request into the conversation.
        messages.append({"role": "assistant", "content": response.content})

        # Run every tool Claude asked for, collect the results.
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"   [Claude decided to call {block.name} with {block.input}]")

                function = TOOL_FUNCTIONS[block.name]
                result = function(**block.input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })

        # Hand the results back to Claude, then loop again.
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    question = "What's the weather in Osaka right now? Should the crew pack a jacket for load-in?"
    print(f"You: {question}\n")
    answer = run_agent(question)
    print(f"\nTour Manager: {answer}")