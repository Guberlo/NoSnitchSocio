"""Read data from files"""
import os

def get_abs_path(*root_file_path: str) -> str:
    """Get the abs path from the root directory of the project to the requested path
    Args:
        root_file_path: path from the root project directory
    Returns:
        corresponding abs path
    """
    root_path = os.path.join(os.path.dirname(__file__), "..", "..")
    return os.path.join(root_path, *root_file_path)


def read_file(*root_file_path: str) -> str:
    """Read the contents of the file
    Args:
        root_file_path: path of the file to read from the root project directory
    Returns:
        contents of the file
    """
    with open(get_abs_path(*root_file_path), "r", encoding="utf-8") as in_file:
        text = in_file.read().strip()
    return text


def read_md(file_name: str) -> str:
    """Read the contents of a markdown file.
    The path is data/markdown.
    It also will replace the following parts of the text:
    - {channel_tag} -> Config.settings['meme']['channel_tag']
    - {bot_tag}     -> Config.settings['bot_tag']
    Args:
        file_name: name of the file
    Returns:
        contents of the file
    """
    text = read_file("markdown", file_name + ".md")
    return text