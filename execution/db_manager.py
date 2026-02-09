import os
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

class DatabaseManager:
    def __init__(self):
        self.connection_string = os.environ.get("DATABASE_URL")
        if not self.connection_string:
            print("WARNING: DATABASE_URL not found in environment variables.")
            self.client = None
            return
        
        try:
            # Set a timeout so it doesn't hang forever if the connection fails
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            self.db = self.client['reddit_insights']
            self.collection = self.db['posts']
            # Test connection
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB Atlas.")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            if "SSL handshake failed" in str(e):
                print("HINT: This is likely an IP Whitelist issue. Ensure 0.0.0.0/0 is allowed in MongoDB Atlas.")
            self.client = None

    def save_posts(self, subreddit, posts):
        if not self.client:
            return False
        
        timestamp = datetime.datetime.now().isoformat()
        
        for post in posts:
            # We use 'url' or 'permalink' as a unique identifier to avoid duplicates
            # but we want to update the engagement history
            post_id = post.get('permalink')
            
            self.collection.update_one(
                {'permalink': post_id},
                {
                    '$set': {
                        'subreddit': subreddit,
                        'title': post.get('title'),
                        'url': post.get('url'),
                        'ups': post.get('ups'),
                        'num_comments': post.get('num_comments'),
                        'engagement': post.get('engagement'),
                        'last_updated': timestamp
                    },
                    '$setOnInsert': {
                        'created_at': timestamp
                    }
                },
                upsert=True
            )
        return True

    def get_latest_posts(self, subreddits, limit=5):
        if not self.client:
            return {}
        
        results = {}
        for subreddit in subreddits:
            cursor = self.collection.find({'subreddit': subreddit}).sort('engagement', -1).limit(limit)
            results[subreddit] = list(cursor)
            # Remove MongoDB's _id for JSON serialization
            for post in results[subreddit]:
                post.pop('_id', None)
                
        return results

# Singleton instance
db_manager = DatabaseManager()
