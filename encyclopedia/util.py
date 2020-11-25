import re
import markdown2

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from markdown2 import Markdown

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    html_filename = f"encyclopedia/templates/entries/{title}.html"
    default_storage.delete(filename)
    default_storage.delete(html_filename)
    default_storage.save(filename, ContentFile(content))
    markdowner = Markdown()
    html_content = markdowner.convert(content)
    html = "{% extends 'encyclopedia/entry.html' %}\n\n{% block entry_title %}\n" + title + "\n{% endblock %}\n\n{% block entry_body %}" + html_content + "\n{% endblock %}"
    default_storage.save(html_filename, ContentFile(html))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
