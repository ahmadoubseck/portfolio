def extract_title(markdown, fallback="Untitled"):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()

    return fallback
