import re

def make_title(text):
    words = re.findall(r"\b[\w'-]+\b", text)
    if not words:
        return "You Need to Hear This"
    clean = " ".join(words[:14])
    if len(clean) > 72:
        clean = clean[:69].rsplit(" ",1)[0] + "…"
    return clean[0].upper() + clean[1:]