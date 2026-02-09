# Directive: Fetch Reddit Posts

## Goal
Fetch recent posts from specified subreddits and identify the top posts based on engagement.

## Inputs
- `subreddits`: List of subreddit names (e.g., "n8n", "automation").
- `limit`: Number of recent posts to fetch per subreddit (default: 100).
- `top`: Number of top posts to return per subreddit (default: 5).
- `output`: (Optional) Path to save results as a JSON file.

## Tools / Scripts
- `execution/fetch_reddit_posts.py`

## Output
- A Markdown report or JSON object containing the top posts for each subreddit, sorted by engagement score.

## Edge Cases
- **Rate Limiting**: The public JSON API has strict rate limits. If 429 errors occur, wait and retry or reduce the request frequency.
- **Private Subreddits**: Ensure subreddits are public.
- **No Posts**: Handle cases where a subreddit has fewer posts than the limit.
