import requests
from bs4 import BeautifulSoup
from readability import Document

def extract_website_content(url):
    """
    Fetches a website URL and extracts only the main readable content.
    Header, footer, navigation, and scripts are removed to reduce noise.
    """

    # Handle invalid or unreachable URLs gracefully
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception:
        return None, None

    # Readability helps isolate the main article/content from HTML
    doc = Document(response.text)
    html = doc.summary()

    soup = BeautifulSoup(html, "html.parser")

    # Remove common non-informational sections
    for tag in soup(["nav", "footer", "header", "script", "style", "aside"]):
        tag.decompose()

    # Normalize text by removing extra spaces and line breaks
    text = " ".join(soup.get_text().split())

    # Extract page title if available (used as metadata)
    title = soup.title.string if soup.title else "No Title"

    return text, title
