from markdown import markdown_to_html_node
import os
import shutil
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

public_path = os.path.join(BASE_DIR, "..", "public")
static_path = os.path.join(BASE_DIR, "..", "static")


def copy_static_to_public():
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    shutil.copytree(static_path, public_path)


def extract_title(markdown):
    headings = re.findall(r"^# ([^\n]+)", markdown, re.MULTILINE)
    if not len(headings):
        raise Exception("No title in the page")

    return headings[0].strip()


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    with open(template_path, "r", encoding="utf-8") as file:
        template_html = file.read()
    html_node = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    page_html = template_html.replace("{{ Title }}", title)
    page_html = page_html.replace("{{ Content }}", html_node)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page_html)


def main():
    copy_static_to_public()
    from_path = os.path.join(BASE_DIR, "..", "content/index.md")
    template_path = os.path.join(BASE_DIR, "..", "template.html")
    dest_path = os.path.join(BASE_DIR, "..", "public/index.html")
    generate_page(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
