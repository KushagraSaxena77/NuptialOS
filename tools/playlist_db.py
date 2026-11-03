from pathlib import Path
from langchain.tools import tool
from langchain_community.utilities import SQLDatabase
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR/"resources"/"Chinook.db"

DATABASE_URL= f"sqlite:///{DATABASE_PATH}"

db = SQLDatabase.from_uri(DATABASE_URL)

@tool
def playlist_db(genre: str) -> str:
    '''Execute a SQL query against the Chinook music database.

        Available tables include:
        - Track: song information
        - Genre: music genres
        - Album: album information
        - Artist: artist information

    Use Track, not Songs, to retrieve song records.
    
    '''

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:

            cursor = connection.cursor()

            query = """
                SELECT
                    t.Name AS song,
                    ar.Name AS artist,
                    al.Title AS album,
                    g.Name AS genre
                FROM Track t
                JOIN Genre g ON t.GenreId = g.GenreId
                LEFT JOIN Album al ON t.AlbumId = al.AlbumId
                LEFT JOIN Artist ar ON al.ArtistId = ar.ArtistId
                WHERE LOWER(g.Name) = LOWER(?)
                LIMIT 20;
            """

            cursor.execute(query, (genre,))
            results = cursor.fetchall()

            if not results:
                return f"No tracks found for genre: {genre}"

            output = []

            for song, artist, album, music_genre in results:
                output.append(
                    f"Song: {song}\n"
                    f"Artist: {artist}\n"
                    f"Album: {album}\n"
                    f"Genre: {music_genre}"
                )

            return "\n\n".join(output)
    except Exception as exc:
        return f"Database query failed: {exc}"
    