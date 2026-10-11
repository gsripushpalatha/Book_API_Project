import sqlite3

with sqlite3.connect("books.db") as conn:
    cursor = conn.execute("SELECT COUNT(*) FROM books")
    print("Total stored books:", cursor.fetchone()[0])

    cursor = conn.execute("""
        SELECT title, author, publication_year
        FROM books
        LIMIT 5
    """)

    for row in cursor.fetchall():
        print(row)