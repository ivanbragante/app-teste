import json
import os
import argparse
from datetime import datetime

LOG_FILE = 'logs/activities.jsonl'

def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    
    logs = []
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                logs.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return logs

def display_logs(logs, limit=20, level=None, script=None):
    print(f"\n# Automation Logs (Last {limit})\n")
    
    filtered_logs = logs
    if level:
        filtered_logs = [l for l in filtered_logs if l.get('level') == level]
    if script:
        filtered_logs = [l for l in filtered_logs if l.get('script') == script]
        
    for log in filtered_logs[-limit:]:
        timestamp = log.get('timestamp', 'N/A')
        lvl = log.get('level', 'INFO')
        scr = log.get('script', 'Unknown')
        msg = log.get('message', '')
        
        print(f"[{timestamp}] [{lvl}] [{scr}] {msg}")
        if 'data' in log and log['data']:
             print(f"   Data: {json.dumps(log['data'], ensure_ascii=False)}")

def main():
    parser = argparse.ArgumentParser(description='View automation logs.')
    parser.add_argument('--limit', type=int, default=20, help='Number of logs to show')
    parser.add_argument('--level', type=str, help='Filter by log level')
    parser.add_argument('--script', type=str, help='Filter by script name')
    
    args = parser.parse_args()
    
    logs = load_logs()
    if not logs:
        print("No logs found.")
        return

    display_logs(logs, args.limit, args.level, args.script)

if __name__ == "__main__":
    main()
