from fastapi import FastAPI, HTTPException


from app.scraper import scrape_website


from app.database import (
    insert_scraped_data,
    get_all_scraped_data,
    update_record,
    delete_scraped_data,
    get_all_tables,
    get_table_schema
)


from app.schema import (
    ScrapeRequest,
    UpdateRecordRequest
)


app = FastAPI(
    title="Dynamic Website Scraper API"
)


# HOME
@app.get("/")
def home():

    return {
        "message": "Dynamic Website Scraper API is running"
    }


# SCRAPE WEBSITE
@app.post("/scrape")
def scrape(request: ScrapeRequest):

    try:

        result = scrape_website(
            request.url
        )

        data = result["data"]

        title = None

        if data.get("html"):

            title = data["html"].get("title")

        record_id = insert_scraped_data(
            request.url,
            title,
            data
        )

        return {
            "message": "Website scraped successfully",
            "record_id": record_id,
            "url": request.url,
            "data": data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# GET ALL DATA
@app.get("/data")
def get_data():

    rows = get_all_scraped_data()

    result = []

    for row in rows:

        result.append({
            "id": row[0],
            "url": row[1],
            "title": row[2],
            "data": row[3],
            "created_at": row[4],
            "updated_at": row[5]
        })

    return {
        "count": len(result),
        "data": result
    }


# UPDATE RECORD
@app.put("/data/{record_id}")
def update_data(
    record_id: int,
    request: UpdateRecordRequest
):

    row = update_record(
        record_id,
        request.title,
        request.headings,
        request.paragraphs
    )

    if row is None:

        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    return {
        "message": "Record updated successfully",

        "id": row[0],

        "url": row[1],

        "title": row[2],

        "data": row[3],

        "created_at": row[4],

        "updated_at": row[5]
    }


# DELETE DATA
@app.delete("/data/{record_id}")
def delete_data(record_id: int):

    row = delete_scraped_data(
        record_id
    )

    if row is None:

        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    return {
        "message": "Record deleted successfully",
        "deleted_id": row[0]
    }


# GET DATABASE TABLES
@app.get("/schema/tables")
def get_tables():

    rows = get_all_tables()

    tables = []

    for row in rows:

        tables.append(
            row[0]
        )

    return {
        "count": len(tables),
        "tables": tables
    }


# GET TABLE SCHEMA
@app.get("/schema/{table_name}")
def table_schema(table_name: str):

    rows = get_table_schema(
        table_name
    )

    if not rows:

        raise HTTPException(
            status_code=404,
            detail="Table not found"
        )

    columns = []

    for row in rows:

        columns.append({
            "name": row[0],
            "type": row[1]
        })

    return {
        "table": table_name,
        "columns": columns
    }