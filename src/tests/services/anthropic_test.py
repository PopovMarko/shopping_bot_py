from datetime import date

from shopping_bot.services.anthropic import (
    messages_builder,
    prompt_builder,
    tool_choice,
    tools,
)


def test_prompt_builder_contains_today_and_products():
    prompt = prompt_builder(["milk", "bread"])

    assert f"Today is {date.today().isoformat()}" in prompt
    assert "- milk\n" in prompt
    assert "- bread" in prompt


def test_messages_builder():
    messages = list(messages_builder("aW1n", ["milk"]))

    assert len(messages) == 1
    content = list(messages[0]["content"])
    assert content[0]["type"] == "image"
    assert content[0]["source"]["data"] == "aW1n"  # type: ignore[typeddict-item]
    assert content[1]["type"] == "text"
    assert "- milk" in content[1]["text"]  # type: ignore[typeddict-item]


def test_tool_schema_requires_receipt_date():
    tool = list(tools)[0]
    schema = tool["input_schema"]  # type: ignore[typeddict-item]

    assert tool_choice == {"type": "tool", "name": tool["name"]}
    assert "receipt_date" in schema["required"]
    assert "YYYY-MM-DDTHH:MM:SS" in schema["properties"]["receipt_date"]["description"]
