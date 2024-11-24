def open_textract_json(textract_response):
    blocks = textract_response.get("Blocks", [])
    lines = []

    for block in blocks:
        if block["BlockType"] == "LINE":
            line_id = block["Id"]
            line_text = block["Text"]
            lines.append(line_text)
    return lines