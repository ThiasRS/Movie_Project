from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_image_url TEXT
        )
    """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_image_url FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster_image_url": row[3]} for row in movies}

def add_movie(title, year, rating, poster_image_url):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster_image_url) VALUES (:title, :year, :rating, :poster_image_url)"),
                               {"title": title, "year": year, "rating": rating, "poster_image_url": poster_image_url})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as error:
            print(f"Error: {error}")

def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(text("DELETE FROM movies WHERE LOWER(title) = LOWER(:title)"),
                                {"title": title})
            connection.commit()

            if result.rowcount > 0:
                print(f"Movie '{title}' deleted successfully.")
            else:
                print(f"Movie '{title}' not found.")

        except Exception as error:
            print(f"Error: {error}")


def update_movie(title, rating, year):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(text("UPDATE movies SET year = :year, rating = :rating WHERE LOWER(title) = LOWER(:title)"),
                               {"year": year, "rating": rating, "title": title})
            connection.commit()

            if result.rowcount > 0:
                print(f"Movie '{title}' updated successfully.")
            else:
                print(f"Movie '{title}' not found.")

        except Exception as error:
            print(f"Error: {error}")