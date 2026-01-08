def markdown_to_blocks(markdow):
    blocks = markdow.split("\n\n")

    formated_blocks = []
    for block in blocks:
        striped = block.strip()
        if len(striped) == 0:
            continue

        formated_blocks.append(striped)

    return formated_blocks
