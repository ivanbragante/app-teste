import os
import sys
from dotenv import load_dotenv

# Add execution directory to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'execution'))
from db_manager import db_manager

def check_db():
    print("Checking MongoDB data...")
    if not db_manager.client:
        print("Error: Could not connect to MongoDB.")
        return

    subreddits = ['n8n', 'automation']
    for sub in subreddits:
        count = db_manager.collection.count_documents({'subreddit': sub})
        print(f"Subreddit r/{sub}: {count} posts found.")
        
        if count > 0:
            latest = db_manager.collection.find_one({'subreddit': sub})
            print(f"Sample post: {latest.get('title')}")

if __name__ == "__main__":
    check_db()
