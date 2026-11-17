import os
from openai import OpenAI

SYSTEM_PROMPT = (
    "You are a courteous customer service assistant for a general business. "
    "Give concise, helpful answers. If you do not know a company-specific policy, "
    "say so and recommend contacting a human representative. Never invent order "
    "status, refunds, account details, or company policies."
)

def generate_reply(message: str) -> tuple[str, str]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return (
            "Demo mode: Thanks for contacting customer support. I can help with "
            "general questions, but this demo is not connected to company account "
            "or order systems. Please provide a little more detail or contact a "
            "human representative for account-specific help.",
            "demo",
        )
    try:
        client = OpenAI(api_key=api_key)
        result = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            max_tokens=300,
            temperature=0.3,
        )
        reply = result.choices[0].message.content or "I couldn't generate a response."
        return reply, "openai"
    except Exception:
        # Avoid exposing provider errors, credentials, or internal details to end users.
        return (
            "I'm sorry, but the automated assistant is temporarily unavailable. "
            "Please try again or contact a human representative.",
            "unavailable",
        )
