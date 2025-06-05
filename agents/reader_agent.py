import re

def extract_sections(text):
    """
    Extract key sections from an academic paper using heading-based regex search.
    Returns a dictionary with section names and their content.
    """
    section_patterns = {
        "abstract": r"(abstract|summary)[\\s\\n]*[:\\-]?[\\s\\n]*(.*?)(?=\\n\\s*(introduction|1\\.|i\\.|background))",
        "introduction": r"(introduction|background)[\\s\\n]*[:\\-]?[\\s\\n]*(.*?)(?=\\n\\s*(methods|methodology|2\\.|ii\\.|materials))",
        "methods": r"(methods|methodology|materials and methods)[\\s\\n]*[:\\-]?[\\s\\n]*(.*?)(?=\\n\\s*(results|3\\.|iii\\.|findings))",
        "results": r"(results|findings|analysis)[\\s\\n]*[:\\-]?[\\s\\n]*(.*?)(?=\\n\\s*(discussion|conclusion|4\\.|iv\\.))",
        "conclusion": r"(conclusion|discussion|summary)[\\s\\n]*[:\\-]?[\\s\\n]*(.*?)(?=\\n\\s*(references|bibliography|acknowledg|5\\.|v\\.))"
    }

    sections = {}
    for section, pattern in section_patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            sections[section] = match.group(2).strip()
        else:
            sections[section] = "Not detected"

    # Add title as first non-empty line
    lines = text.splitlines()
    title = next((line.strip() for line in lines if line.strip()), "Not detected")
    sections["title"] = title

    return sections
