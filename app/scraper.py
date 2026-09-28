import json
import re

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# =========================================================
# MAIN SCRAPER
# =========================================================

def scrape_website(url):

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

    except requests.RequestException:
        print("Requests failed. Trying Playwright...")

        return scrape_with_playwright(url)

    content_type = response.headers.get(
        "Content-Type",
        ""
    ).lower()

    # =====================================================
    # DIRECT JSON / API RESPONSE
    # =====================================================

    if "application/json" in content_type:

        json_data = response.json()

        return {
            "url": url,
            "data": {
                "html": None,
                "json": json_data,
                "json_ld": [],
                "embedded_data": [],
                "dynamic": None
            }
        }

    # =====================================================
    # HTML RESPONSE
    # =====================================================

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    html_data = extract_html_data(soup)

    json_ld = extract_json_ld(soup)

    embedded_data = extract_embedded_data(soup)

    data = {
        "html": html_data,
        "json": None,
        "json_ld": json_ld,
        "embedded_data": embedded_data,
        "dynamic": None
    }

    # =====================================================
    # IF HTML HAS BASIC DATA
    # =====================================================

    if has_useful_data(data):

        return {
            "url": url,
            "data": data
        }

    # =====================================================
    # OTHERWISE USE PLAYWRIGHT
    # =====================================================

    print(
        "Normal HTML did not contain enough data. "
        "Trying Playwright..."
    )

    return scrape_with_playwright(url)


# =========================================================
# HTML EXTRACTION
# =========================================================

def extract_html_data(soup):

    return {

        "title": (
            soup.title.get_text(strip=True)
            if soup.title
            else None
        ),

        "headings": [
            heading.get_text(
                " ",
                strip=True
            )
            for heading in soup.find_all(
                ["h1", "h2", "h3"]
            )
        ],

        "paragraphs": [
            paragraph.get_text(
                " ",
                strip=True
            )
            for paragraph in soup.find_all("p")
        ],

      "links": [
    {
        "text": link.get_text(" ", strip=True) or "Untitled Link",
        "url": link.get("href")
    }
    for link in soup.find_all("a", href=True)
],

        "images": [
            image.get("src")
            for image in soup.find_all(
                "img",
                src=True
            )
        ]
    }


# =========================================================
# JSON-LD
# =========================================================

def extract_json_ld(soup):

    data = []

    for script in soup.find_all(
        "script",
        type="application/ld+json"
    ):

        try:

            if script.string:

                data.append(
                    json.loads(
                        script.string
                    )
                )

        except (
            json.JSONDecodeError,
            TypeError
        ):

            continue

    return data


# =========================================================
# EMBEDDED JAVASCRIPT DATA
# =========================================================

def extract_embedded_data(soup):

    data = []

    for script in soup.find_all("script"):

        script_text = script.get_text()

        if "var data =" not in script_text:
            continue

        match = re.search(
            r"var\s+data\s*=\s*(\[.*?\]);",
            script_text,
            re.DOTALL
        )

        if not match:
            continue

        try:

            json_text = match.group(1)

            data.append(
                json.loads(
                    json_text
                )
            )

        except json.JSONDecodeError:

            continue

    return data


# =========================================================
# CHECK USEFUL DATA
# =========================================================

def has_useful_data(data):

    html_data = data.get("html")

    if not html_data:
        return False

    # Title alone is NOT useful because
    # React/Vue/JS websites often have a static title.

    # Links/images are also not enough because
    # navigation and static assets can exist in the HTML shell.

    # Actual text content is a stronger signal.
    paragraphs = html_data.get("paragraphs", [])

    meaningful_paragraphs = [
        paragraph
        for paragraph in paragraphs
        if paragraph and len(paragraph.strip()) > 30
    ]

    if meaningful_paragraphs:
        return True

    # Structured data is useful even without normal HTML content.
    if data.get("json_ld"):
        return True

    if data.get("embedded_data"):
        return True

    return False
# =========================================================
# PLAYWRIGHT
# =========================================================

def scrape_with_playwright(url):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            user_agent=HEADERS["User-Agent"]
        )

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000
        )

        page.wait_for_timeout(3000)

        html = page.content()

        browser.close()

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    html_data = extract_html_data(soup)

    json_ld = extract_json_ld(soup)

    embedded_data = extract_embedded_data(soup)

    return {
        "url": url,
        "data": {
            "html": html_data,
            "json": None,
            "json_ld": json_ld,
            "embedded_data": embedded_data,
            "dynamic": {
                "rendered": True
            }
        }
    }