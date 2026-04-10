# Save to CSV / insert into PostgreSQL

import os
import csv
import psycopg2

password = os.getenv("DB_PASSWORD")


def save_raw_titles_to_csv(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['title'])

        for row in data:
            writer.writerow([row])


def save_to_csv(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'title_length'])

        for row in data:
            writer.writerow([row["title"], row["title_length"]])


def upload_data(path):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="recipes_db",
            user="postgres",
            password=password
        )

        cursor = conn.cursor()

        with open(path, "r") as file:
            reader = csv.DictReader(file)
            data = [(row["title"], row["title_length"]) for row in reader]

        cursor.executemany(
            "INSERT INTO recipes (title, title_length) VALUES (%s, %s)",
            data
        )

        conn.commit()

    except Exception as e:
        print(f"Error uploading data: {e}")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # Load processed data from Databricks to Postgresql
    data_path = os.path.join("data", "processed", "recipes_export.csv")
    upload_data(data_path)
    print(f"Data from {data_path} loaded to recipes table in recipes_db")