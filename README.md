# Python Assignment – Dynamic Website Scraper

## 1. Project Overview

This project implements the Python assignment requirement to accept a website URL, scrape useful data, store the scraped result in PostgreSQL, and expose CRUD and database-schema APIs.

The application has two main layers:

- **FastAPI backend** – scraping, database operations, CRUD APIs and schema APIs.
- **Streamlit frontend** – dashboard and user interface for scraping, viewing, updating, deleting and exporting data.

The scraper supports normal HTML, JSON/API responses, JSON-LD, supported embedded JavaScript data, and JavaScript-rendered pages through Playwright.

> The assignment asks for a generic scraper that accepts a website URL and returns data in a structured form suitable for CRUD operations.

---

## 2. Assignment Requirements and Implementation

| Assignment requirement | Implementation |
|---|---|
| Scrape website data | `app/scraper.py` using Requests, BeautifulSoup and Playwright |
| Accept any URL | `POST /scrape` accepts a URL |
| Structured scraped data | Data is returned as nested Python/JSON data |
| PostgreSQL storage | `app/database.py` using psycopg2 |
| Create API | `POST /scrape` scrapes and stores data |
| Read API | `GET /data` |
| Update API | `PUT /data/{record_id}` |
| Delete API | `DELETE /data/{record_id}` |
| Schema APIs | `/schema/tables` and `/schema/{table_name}` |
| CSV script | `generate_csv.py` / CSV export page using Python `csv` |
| README | This file |
| Documentation | Project approach and flow are documented in the accompanying DOCX |

---

## 3. Project Architecture

```text
                         USER
                           |
                           v
                    STREAMLIT FRONTEND
                           |
                           v
                    ui/components/api.py
                           |
                           v
                       FASTAPI
                           |
              +------------+------------+
              |                         |
              v                         v
          SCRAPER                    DATABASE
              |                         |
              v                         v
   Requests / BeautifulSoup        PostgreSQL
              |                    JSONB storage
              v
          Playwright
       when rendering is
          required
```

### Application flow

```text
User enters URL
      |
      v
POST /scrape
      |
      v
scraper.py
      |
      +--> Normal HTML --> BeautifulSoup
      |
      +--> JSON/API response
      |
      +--> JSON-LD
      |
      +--> Embedded JS data
      |
      +--> JavaScript-rendered page --> Playwright
      |
      v
Structured data
      |
      v
database.py
      |
      v
PostgreSQL
```

---

## 4. Dynamic Website Identification

The assignment suggests disabling JavaScript and checking whether the data still loads.

If the useful page data disappears when JavaScript is disabled, the page is likely rendering data at runtime.

In this project, the scraper handles JavaScript-rendered pages by using Playwright as a browser-rendering fallback.

The current Playwright implementation:

1. Opens the page in a headless Chromium browser.
2. Waits for the DOM to load.
3. Allows time for JavaScript-rendered content.
4. Gets the rendered HTML.
5. Passes the resulting HTML to BeautifulSoup.
6. Extracts structured data.

> The current implementation does not claim automatic discovery of every Fetch/XHR/GraphQL endpoint. It renders the page and parses the resulting DOM.

---

## 5. Scraping

### Libraries

- `requests`
- `beautifulsoup4`
- `playwright`

### Extracted HTML information

For normal HTML, the scraper extracts:

- Page title
- H1/H2/H3 headings
- Paragraphs
- Links
- Images

### Other supported data

The scraper also checks for:

- JSON/API responses
- JSON-LD
- Supported embedded JavaScript data
- Dynamic rendered HTML

Example structured result:

```json
{
  "html": {
    "title": "Example Website",
    "headings": ["Heading 1", "Heading 2"],
    "paragraphs": ["Example paragraph"],
    "links": [],
    "images": []
  },
  "json": null,
  "json_ld": [],
  "embedded_data": [],
  "dynamic": null
}
```

This structure is stored inside PostgreSQL JSONB.

---

## 6. PostgreSQL Database

Database name:

```text
scraper_db
```

Table:

```sql
CREATE TABLE scraped_data (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    title TEXT,
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Why JSONB?

The assignment requires the scraper to work with different websites. Different websites can expose different fields.

Keeping variable scraped content in `data JSONB` allows the same database table to store different website structures without continuously adding website-specific columns.

The fixed columns are:

```text
id
url
title
data
created_at
updated_at
```

---

## 7. CRUD APIs

### Create

```http
POST /scrape
```

Request:

```json
{
  "url": "https://example.com"
}
```

The API:

1. Receives the URL.
2. Scrapes the website.
3. Extracts structured data.
4. Gets the page title where available.
5. Inserts the result into PostgreSQL.
6. Returns the created record information.

### Read

```http
GET /data
```

Returns all stored scraped records.

### Update

```http
PUT /data/{record_id}
```

The current UI/API update flow edits:

- Title
- Headings
- Paragraphs

The record ID is supplied through the URL and is not itself modified.

Example request:

```json
{
  "title": "Updated Title",
  "headings": [
    "Updated Heading 1",
    "Updated Heading 2"
  ],
  "paragraphs": [
    "Updated paragraph."
  ]
}
```

### Delete

```http
DELETE /data/{record_id}
```

Deletes the selected scraped record.

---

## 8. Schema APIs

### List tables

```http
GET /schema/tables
```

Returns the tables available in the public PostgreSQL schema.

### View table schema

```http
GET /schema/{table_name}
```

Returns:

- Column name
- Data type

Example response structure:

```json
{
  "table": "scraped_data",
  "columns": [
    {
      "name": "id",
      "type": "integer"
    },
    {
      "name": "url",
      "type": "text"
    },
    {
      "name": "title",
      "type": "text"
    }
  ]
}
```

---

## 9. CSV Generation

The project includes a separate CSV generation script:

```text
generate_csv.py
```

The project uses Python's built-in `csv` module.

The CSV output contains appropriate headers and organizes the scraped records into a readable tabular format.

The Streamlit project also provides a CSV Export page for users.

---

## 10. Streamlit Interface

The Streamlit UI provides:

### Dashboard

Shows application statistics, recent records and scraping-related information.

### Scraped Website

- Enter URL
- Start scraping
- View extracted data
- Inspect HTML, JSON/API, JSON-LD, embedded data and dynamic data when available

### Scraped Data

- View stored records
- Search records
- Filter records
- Inspect scraped content

### Update Record

Select a record and update:

- Title
- Headings
- Paragraphs

### Delete Record

Delete a selected record.

### Database Schema

View database tables, columns and data types.

### CSV Export

Generate/export scraped data as CSV.

---

## 11. Project Structure

```text
Python Assignment/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── scraper.py
│   └── schema.py
│
├── ui/
│   ├── dashboard.py
│   ├── components/
│   │   ├── api.py
│   │   ├── styles.py
│   │   └── __init__.py
│   ├── pages/
│   │   ├── 1_Scraped_website.py
│   │   ├── 2_Scraped_data.py
│   │   ├── 3_Update_Record.py
│   │   ├── 4_delete_record.py
│   │   ├── 5_database_schema.py
│   │   └── 6_CSV_Export.py
│   └── assets/
│       └── logo.png
│
├── generate_csv.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 12. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main language |
| FastAPI | REST API |
| Streamlit | Frontend/UI |
| PostgreSQL | Database |
| psycopg2 | PostgreSQL connection |
| Requests | HTTP requests |
| BeautifulSoup | HTML parsing |
| Playwright | Browser rendering |
| Pydantic | Request validation |
| python-dotenv | Environment variables |
| csv | CSV generation |

---

## 13. Setup

### Create virtual environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

If PowerShell activation is blocked:

```bash
venv\Scripts\activate.bat
```

### Install dependencies

```bash
pip install -r requirements.txt
```

Install Chromium for Playwright:

```bash
playwright install chromium
```

---

## 14. PostgreSQL Configuration

Create:

```text
Database: scraper_db
```

Create the table:

```sql
CREATE TABLE scraped_data (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    title TEXT,
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Create `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=scraper_db
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD
```

Do not commit `.env` to GitHub.

Recommended `.gitignore`:

```gitignore
.env
venv/
__pycache__/
```

---

## 15. Running the Project

### Terminal 1 – FastAPI

From the project root:

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Terminal 2 – Streamlit

```bash
cd ui
streamlit run dashboard.py
```

Streamlit:

```text
http://localhost:8501
```

Both services need to run at the same time because Streamlit communicates with FastAPI.

---

## 16. Complete CRUD Flow

```text
CREATE
User
  |
  v
Enter URL
  |
  v
POST /scrape
  |
  v
Scraper
  |
  v
PostgreSQL


READ
Streamlit
  |
  v
GET /data
  |
  v
PostgreSQL
  |
  v
Display records


UPDATE
Select Record ID
  |
  v
Edit Title / Headings / Paragraphs
  |
  v
PUT /data/{id}
  |
  v
PostgreSQL


DELETE
Select Record
  |
  v
DELETE /data/{id}
  |
  v
PostgreSQL
```

---

## 17. Error Handling

The API uses HTTP exceptions for cases such as:

- Record not found
- Table not found
- Scraping/database errors

The Streamlit UI also displays user-friendly error and warning messages.

---

## 18. Limitations

- Some websites may block automated requests.
- Authentication-required websites need additional authentication handling.
- Some JavaScript-heavy pages require browser rendering.
- Generic scraping cannot guarantee extraction of every website-specific field.
- The current implementation does not automatically expose every internal Fetch/XHR/GraphQL endpoint.
- Current update functionality is limited to title, headings and paragraphs.

---

## 19. Future Improvements

- Automatic Fetch/XHR/GraphQL endpoint discovery
- Authentication support
- Better website-specific extraction
- Background scraping jobs
- Pagination for large datasets
- API authentication and authorization
- Automated tests
- Logging and monitoring
- Docker deployment
- Cloud deployment

---

## 20. Assignment Submission

The assignment requires:

- GitHub repository
- README with setup and additional features
- Loom video demonstrating the working project
- Documentation of the approach and flow

The project documentation is provided separately with this repository.

---

## Author

**Gaurav**

BCA Student — Chandigarh University

**Project:** Dynamic Website Scraper & CRUD API
