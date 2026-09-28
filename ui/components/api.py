import requests


API_URL = "http://127.0.0.1:8000"


# GET ALL SCRAPED DATA
def get_data():

    response = requests.get(
        f"{API_URL}/data",
        timeout=20
    )

    response.raise_for_status()

    return response.json()


# SCRAPE WEBSITE
def scrape_website(url):

    response = requests.post(
        f"{API_URL}/scrape",
        json={
            "url": url
        },
        timeout=60
    )

    response.raise_for_status()

    return response.json()


# UPDATE TITLE, HEADINGS AND PARAGRAPHS
def update_record(
    record_id,
    title,
    headings,
    paragraphs
):

    response = requests.put(
        f"{API_URL}/data/{record_id}",
        json={
            "title": title,
            "headings": headings,
            "paragraphs": paragraphs
        },
        timeout=20
    )

    response.raise_for_status()

    return response.json()


# DELETE RECORD
def delete_record(record_id):

    response = requests.delete(
        f"{API_URL}/data/{record_id}",
        timeout=20
    )

    response.raise_for_status()

    return response.json()


# GET DATABASE TABLES
def get_tables():

    response = requests.get(
        f"{API_URL}/schema/tables",
        timeout=20
    )

    response.raise_for_status()

    return response.json()


# GET TABLE SCHEMA
def get_schema(table_name):

    response = requests.get(
        f"{API_URL}/schema/{table_name}",
        timeout=20
    )

    response.raise_for_status()

    return response.json()