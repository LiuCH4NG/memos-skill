#!/usr/bin/env python3
"""
Create a memo in Memos via API.

Usage:
    python3 create_memo.py "Note content" [--tags "tag1,tag2"]
"""

import argparse
import os
import sys
import urllib.request
import urllib.error
import json


def load_env_file():
    """Load environment variables from .env file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '..', '.env')
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Only set if not already in environment
                    if key not in os.environ:
                        os.environ[key] = value


def create_memo(content: str, tags: list = None, visibility: str = "PRIVATE"):
    """Create a memo in Memos."""
    
    api_url = os.environ.get("MEMOS_API_URL")
    api_token = os.environ.get("MEMOS_API_TOKEN")
    
    if not api_url:
        print("Error: MEMOS_API_URL environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    if not api_token:
        print("Error: MEMOS_API_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    # Ensure URL doesn't end with trailing slash
    api_url = api_url.rstrip("/")
    
    # Build request payload
    payload = {
        "content": content,
        "visibility": visibility
    }
    
    if tags:
        payload["tags"] = tags
    
    # Make API request
    endpoint = f"{api_url}/api/v1/memos"
    
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"Note created successfully!")
            print(f"Memo ID: {result.get('id', 'N/A')}")
            if result.get('name'):
                print(f"Name: {result.get('name')}")
            return 0
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        print(f"Response: {error_body}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main():
    # Load .env file first
    load_env_file()
    
    parser = argparse.ArgumentParser(description="Create a memo in Memos")
    parser.add_argument("content", help="The memo content")
    parser.add_argument("--tags", help="Comma-separated list of tags")
    parser.add_argument("--visibility", default="PRIVATE", 
                        choices=["PRIVATE", "PROTECTED", "PUBLIC"],
                        help="Memo visibility (default: PRIVATE)")
    
    args = parser.parse_args()
    
    tags = None
    if args.tags:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    
    return create_memo(args.content, tags, args.visibility)


if __name__ == "__main__":
    sys.exit(main())
