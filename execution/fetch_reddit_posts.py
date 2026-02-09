import argparse
import requests
import time
import json
import sys
import os
import datetime

# Add the current directory to sys.path to import db_manager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db_manager import db_manager

LOG_FILE = 'logs/activities.jsonl'

def log_activity(level, message, data=None):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    entry = {
        'timestamp': datetime.datetime.now().isoformat(),
        'script': 'fetch_reddit_posts.py',
        'level': level,
        'message': message,
        'data': data
    }
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')

def fetch_subreddit_posts(subreddit, limit=100):
    """
    Fetches posts from a subreddit using the public JSON API.
    """
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:
            print(f"Rate limited on r/{subreddit}. Waiting 5 seconds...")
            time.sleep(5)
            response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error fetching r/{subreddit}: {response.status_code}")
            return []

        data = response.json()
        posts = []
        
        if 'data' in data and 'children' in data['data']:
            for child in data['data']['children']:
                post_data = child['data']
                posts.append({
                    'title': post_data.get('title'),
                    'url': post_data.get('url'),
                    'permalink': f"https://www.reddit.com{post_data.get('permalink')}",
                    'ups': post_data.get('ups', 0),
                    'num_comments': post_data.get('num_comments', 0),
                    'created_utc': post_data.get('created_utc')
                })
        
        return posts

    except Exception as e:
        print(f"Exception fetching r/{subreddit}: {e}")
        return []

def analyze_posts(posts, top_n=5):
    """
    Calculates engagement score and returns the top N posts.
    Engagement = ups + num_comments
    """
    for post in posts:
        post['engagement'] = post['ups'] + post['num_comments']
    
    sorted_posts = sorted(posts, key=lambda x: x['engagement'], reverse=True)
    return sorted_posts[:top_n]

def main():
    parser = argparse.ArgumentParser(description='Fetch and analyze Reddit posts.')
    parser.add_argument('--subreddits', nargs='+', required=True, help='List of subreddits to fetch')
    parser.add_argument('--limit', type=int, default=100, help='Number of posts to fetch per subreddit')
    parser.add_argument('--top', type=int, default=5, help='Number of top posts to return')
    parser.add_argument('--output', type=str, help='Path to save results as JSON')
    
    args = parser.parse_args()
    
    results = {}
    
    log_activity('INFO', f"Starting Reddit fetch for: {args.subreddits}")

    for subreddit in args.subreddits:
        print(f"Fetching r/{subreddit}...")
        log_activity('INFO', f"Fetching posts from r/{subreddit}")
        posts = fetch_subreddit_posts(subreddit, args.limit)
        
        if not posts:
            log_activity('WARNING', f"No posts found for r/{subreddit}")

        top_posts = analyze_posts(posts, args.top)
        results[subreddit] = top_posts
        
        log_activity('INFO', f"Analyzed r/{subreddit}", {'posts_fetched': len(posts), 'top_posts': len(top_posts)})
        
        # Be nice to Reddit's API
        time.sleep(2)

    # Output Report
    print("\n# Reddit Analysis Report\n")
    for subreddit, posts in results.items():
        print(f"## Top {len(posts)} Posts in r/{subreddit}")
        for i, post in enumerate(posts, 1):
            print(f"{i}. **{post['title']}**")
            print(f"   - Engagement: {post['engagement']} (Ups: {post['ups']}, Comments: {post['num_comments']})")
            print(f"   - Link: {post['permalink']}")
            print()

    # Save to JSON if requested
    if args.output:
        if 'reddit-viewer' in args.output:
             final_path = args.output
             output_dir = os.path.dirname(final_path)
             if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
        else:
            # Enforce .tmp directory
            filename = os.path.basename(args.output)
            final_path = os.path.join('.tmp', filename)
            
            if not os.path.exists('.tmp'):
                os.makedirs('.tmp')
        try:
            with open(final_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
            print(f"Results saved to {final_path}")
            log_activity('INFO', "Results saved to JSON", {'path': final_path})
        except Exception as e:
            print(f"Error saving to JSON: {e}")
            log_activity('ERROR', "Failed to save to JSON", {'error': str(e)})

    # Save to MongoDB
    try:
        if db_manager.client:
            print("Saving results to MongoDB...")
            for subreddit, posts in results.items():
                db_manager.save_posts(subreddit, posts)
            log_activity('INFO', "Results saved to MongoDB")
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")
        log_activity('ERROR', "Failed to save to MongoDB", {'error': str(e)})

    log_activity('INFO', "Execution completed")

if __name__ == "__main__":
    main()
