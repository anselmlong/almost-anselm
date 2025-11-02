"""Simple anonymization utilities.

Replace names and redact PII. This is a stub for the real implementation.
"""

import re


def anonymize_text(text: str) -> str:
    """Return a very small anonymized version of text.

    NOTE: This is a placeholder. Real PII handling must be more robust.
    """
    # Redact email-like tokens
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[REDACTED_EMAIL]", text)
    # Redact phone numbers (very loose)
    text = re.sub(r"\b\d{7,}\b", "[REDACTED_NUMBER]", text)
    return text


if __name__ == "__main__":
    s = "Contact me at alice@example.com or 5551234567"
    print(anonymize_text(s))
