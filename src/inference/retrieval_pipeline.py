"""Build prompt with memory and examples for retrieval-augmented generation.
"""

def build_prompt(context: str, examples: list = None, memory: list = None) -> str:
    parts = []
    if memory:
        parts.append("\n".join(memory))
    if examples:
        parts.append("\n\nEXAMPLES:\n" + "\n".join(examples))
    parts.append("\nCONTEXT:\n" + context)
    return "\n\n".join(parts)


if __name__ == "__main__":
    print(build_prompt("Example context", examples=["ex1 -> ans1"], memory=["user said hi"]))
