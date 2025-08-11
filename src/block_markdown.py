def markdown_to_blocks(markdown):
    sections = markdown.split('\n\n')
    for section in sections:
        section = section.strip()
        if section == "":
            sections.remove(section)
    return sections