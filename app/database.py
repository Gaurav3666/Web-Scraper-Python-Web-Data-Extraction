import os
import psycopg2
from dotenv import load_dotenv
import json


load_dotenv()


def get_connection():

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return connection


# INSERT SCRAPED DATA
def insert_scraped_data(url, title, data):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
        INSERT INTO scraped_data
        (url, title, data)
        VALUES (%s, %s, %s)
        RETURNING id;
    """

    cursor.execute(
        query,
        (
            url,
            title,
            json.dumps(data)
        )
    )

    record_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return record_id


# GET ALL SCRAPED DATA
def get_all_scraped_data():

    connection = get_connection()

    cursor = connection.cursor()

    query = """
        SELECT id, url, title, data, created_at, updated_at
        FROM scraped_data
        ORDER BY id DESC;
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


# UPDATE TITLE, HEADINGS AND PARAGRAPHS
def update_record(
    record_id,
    title,
    headings,
    paragraphs
):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
        UPDATE scraped_data
        SET
            title = %s,

            data = jsonb_set(
                jsonb_set(
                    jsonb_set(
                        data,
                        '{html,title}',
                        %s::jsonb,
                        true
                    ),
                    '{html,headings}',
                    %s::jsonb,
                    true
                ),
                '{html,paragraphs}',
                %s::jsonb,
                true
            ),

            updated_at = CURRENT_TIMESTAMP

        WHERE id = %s

        RETURNING
            id,
            url,
            title,
            data,
            created_at,
            updated_at;
    """

    cursor.execute(
        query,
        (
            title,
            json.dumps(title),
            json.dumps(headings),
            json.dumps(paragraphs),
            record_id
        )
    )

    row = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return row


# DELETE SCRAPED DATA
def delete_scraped_data(record_id):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
        DELETE FROM scraped_data
        WHERE id = %s
        RETURNING id;
    """

    cursor.execute(
        query,
        (record_id,)
    )

    row = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return row


# GET ALL DATABASE TABLES
def get_all_tables():

    connection = get_connection()

    cursor = connection.cursor()

    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


# GET TABLE SCHEMA
def get_table_schema(table_name):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = %s
        ORDER BY ordinal_position;
    """

    cursor.execute(
        query,
        (table_name,)
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows