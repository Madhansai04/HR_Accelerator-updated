import re

def split_sections(text):
    parts = re.split(r"(Section \d+:.*?)", text)

    sections = {}

    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        content = parts[i+1].strip()
        sections[title] = content

    return sections