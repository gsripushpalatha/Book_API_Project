# Book API Project

This project retrieves book records from the Open Library Search API, stores
them in a local SQLite database, and displays the saved records in the
terminal.

## Requirements

- Python 3
- The `requests` package

Install the dependency with:

```powershell
py -m pip install requests
```

## Walkthrough

Run the main program from the project directory:

```powershell
py main.py
```

The program performs these steps:

1. Sends a request to `https://openlibrary.org/search.json` for the query
   `python programming`, asking for up to 10 results.
2. Skips results that do not have both a book key and a title. It uses
   `Unknown` when an author is missing and leaves the publication year empty
   when the API does not provide one.
3. Creates `books.db` and its `books` table if they do not already exist.
4. Inserts each book, or updates its existing row when the same Open Library
   key is already stored.
5. Reads all rows from the database, sorts them by title, and prints their
   titles, authors, publication years, and the total displayed.

The database file is created in the current working directory. Run commands
from the project directory if you want it to be the `books.db` next to
`main.py`.

## Check the database

After running the main program, inspect the stored record count and up to five
sample rows with:

```powershell
py check_database.py
```

Example output:

```text
Total stored books: 10
('Example title', 'Example author', 2020)
```

The actual records depend on the API response. The check script expects the
`books` table to exist, so run `main.py` first.

## Database schema

The `books` table contains:

| Column | Type | Description |
| --- | --- | --- |
| `book_id` | `TEXT PRIMARY KEY` | Open Library key used to identify and update a book |
| `title` | `TEXT NOT NULL` | Book title |
| `author` | `TEXT` | Comma-separated author names, or `Unknown` |
| `publication_year` | `INTEGER` | First publication year, if available |

## Errors

The main program reports request errors (such as network failures and HTTP
errors) as API errors. SQLite and value-processing errors are reported as
processing errors. If the API is unavailable, check the network connection
and try again.
