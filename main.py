
import requests
import sqlite3

API_URL = "https://openlibrary.org/search.json"
DB_NAME = "books.db"


def fetch_books():
    """Fetch books from the external API."""
    response = requests.get(
        API_URL,
        params={"q": "python programming", "limit": 10},
        timeout=15
    )
    response.raise_for_status()

    data = response.json()
    books = []

    for item in data.get("docs", []):
        book_id = item.get("key")
        title = item.get("title")

        if not book_id or not title:
            continue

        books.append((
            book_id,
            title,
            ", ".join(item.get("author_name", [])) or "Unknown",
            item.get("first_publish_year")
        ))

    return books


def save_books(books):
    """Create the table and save the fetched records."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT,
                publication_year INTEGER
            )
        """)

        conn.executemany("""
            INSERT INTO books
                (book_id, title, author, publication_year)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(book_id) DO UPDATE SET
                title = excluded.title,
                author = excluded.author,
                publication_year = excluded.publication_year
        """, books)


def display_books():
    """Read the saved records and display them."""
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("""
            SELECT title, author, publication_year
            FROM books
            ORDER BY title
        """).fetchall()

    print("\nBOOKS STORED IN SQLITE")
    print("=" * 50)

    for title, author, year in rows:
        print(f"Title: {title}")
        print(f"Author: {author}")
        print(f"Publication Year: {year or 'Unknown'}")
        print("-" * 50)

    print(f"Total books displayed: {len(rows)}")


def main():
    try:
        books = fetch_books()
        save_books(books)
        display_books()
        print("\nProgram completed successfully.")

    except requests.RequestException as error:
        print(f"API error: {error}")

    except (sqlite3.Error, ValueError) as error:
        print(f"Processing error: {error}")


if __name__ == "__main__":
    main()
