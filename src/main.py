from textnode import TextType, TextNode
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

public_path = os.path.join(BASE_DIR, "..", "public")
static_path = os.path.join(BASE_DIR, "..", "static")


def copy_static_to_public():
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    shutil.copytree(static_path, public_path)


def main():
    copy_static_to_public()


if __name__ == "__main__":
    main()
