import csv

from app.database import get_connection


def generate_csv():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT id, url, title, data, created_at, updated_at
        FROM scraped_data
        ORDER BY id;
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    with open("scraped_data.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        # CSV header
        writer.writerow([
            "id",
            "url",
            "title",
            "data",
            "created_at",
            "updated_at"
        ])

        # Database records
        for row in rows:
            writer.writerow(row)

    print("CSV generated successfully!")


if __name__ == "__main__":
    generate_csv()