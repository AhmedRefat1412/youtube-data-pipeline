import os
import psycopg2
from dotenv import load_dotenv

# Load database credentials from .env file
load_dotenv()

class DataLoader:
    def __init__(self):
        # Connect to PostgreSQL
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        # Create a cursor to execute SQL queries
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Create videos table if it doesn't already exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                video_id VARCHAR PRIMARY KEY,
                title TEXT,
                channel_id VARCHAR,
                channel_name VARCHAR,
                published_at TIMESTAMP,
                description TEXT,
                view_count INTEGER,
                like_count INTEGER,
                comment_count INTEGER
            )
        """)

        # Create comments table with a foreign key reference to videos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id SERIAL PRIMARY KEY,
                video_id VARCHAR REFERENCES videos(video_id),
                author VARCHAR,
                text TEXT,
                published_at TIMESTAMP,
                like_count INTEGER
            )
        """)
        # Commit both table creations in one transaction
        self.conn.commit()
        print("Tables created successfully")

    def load_videos(self, videos):
        for video in videos:
            # Insert each video, skip if video_id already exists
            self.cursor.execute("""
                INSERT INTO videos 
                    (video_id, title, channel_id, channel_name, 
                     published_at, description, view_count, 
                     like_count, comment_count)
                VALUES 
                    (%(video_id)s, %(title)s, %(channel_id)s, %(channel_name)s,
                     %(published_at)s, %(description)s, %(view_count)s,
                     %(like_count)s, %(comment_count)s)
                ON CONFLICT (video_id) DO NOTHING
            """, video)
        # Commit all inserts at once
        self.conn.commit()
        print(f"Loaded {len(videos)} videos")

    def load_comments(self, comments):
        for comment in comments:
            # Insert each comment linked to its video
            self.cursor.execute("""
                INSERT INTO comments 
                    (video_id, author, text, published_at, like_count)
                VALUES 
                    (%(video_id)s, %(author)s, %(text)s, 
                     %(published_at)s, %(like_count)s)
            """, comment)
        # Commit all comment inserts at once
        self.conn.commit()
        print(f"Loaded {len(comments)} comments")

    def close(self):
        # Close cursor and connection to free up resources
        self.cursor.close()
        self.conn.close()