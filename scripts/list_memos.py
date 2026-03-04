#!/usr/bin/env python3
"""
List memos from Memos via API.

Usage:
    python3 list_memos.py [--limit 10] [--tag xxx] [--search xxx]

Examples:
    python3 list_memos.py                    # List recent 10 memos
    python3 list_memos.py --limit 20         # List recent 20 memos
    python3 list_memos.py --tag work         # List memos with 'work' tag
    python3 list_memos.py --search 报销      # Search for '报销' in content
"""

import argparse
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
import json
from datetime import datetime


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
                    if key not in os.environ:
                        os.environ[key] = value


def format_time(iso_time: str) -> str:
    """Format ISO time to readable format."""
    try:
        dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return iso_time


def truncate_content(content: str, max_len: int = 50) -> str:
    """Truncate content for display."""
    content = content.replace('\n', ' ').strip()
    if len(content) > max_len:
        return content[:max_len] + '...'
    return content


def list_memos(api_url: str, api_token: str, limit: int = 10, tag: str = None, search: str = None):
    """List memos from Memos."""
    
    # Build query parameters
    # If filtering by tag, fetch more to ensure we get enough after filtering
    fetch_limit = limit * 3 if tag else limit
    params = [f"pageSize={fetch_limit}"]
    
    if search and not tag:
        # Search in content
        params.append(f"filter={urllib.parse.quote(f'content.contains(\"{search}\")')}")
    
    query_string = "&".join(params)
    endpoint = f"{api_url}/api/v1/memos?{query_string}"
    
    req = urllib.request.Request(
        endpoint,
        headers={
            "Authorization": f"Bearer {api_token}"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            memos = result.get('memos', [])
            
            # Client-side tag filtering
            if tag:
                memos = [m for m in memos if tag in m.get('tags', [])]
            
            # Limit results
            memos = memos[:limit]
            
            if not memos:
                print("没有找到笔记")
                return 0
            
            # Display header
            if search:
                print(f"\n🔍 搜索结果: '{search}'")
            elif tag:
                print(f"\n🏷️  标签过滤: '{tag}'")
            else:
                print(f"\n📝 最近笔记")
            print("=" * 60)
            
            # Display memos
            for i, memo in enumerate(memos, 1):
                name = memo.get('name', 'N/A')
                content = truncate_content(memo.get('content', ''), 40)
                create_time = format_time(memo.get('createTime', ''))
                tags = memo.get('tags', [])
                pinned = "📌 " if memo.get('pinned') else ""
                
                print(f"\n{i}. {pinned}{content}")
                print(f"   📄 {name}")
                print(f"   🕐 {create_time}", end="")
                if tags:
                    print(f"  🏷️  {', '.join(tags)}")
                else:
                    print()
            
            print(f"\n" + "=" * 60)
            print(f"共找到 {len(memos)} 条笔记")
            return 0
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"❌ HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        print(f"Response: {error_body}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"❌ URL Error: {e.reason}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def main():
    # Load .env file first
    load_env_file()
    
    parser = argparse.ArgumentParser(
        description="List memos from Memos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # List recent 10 memos
  %(prog)s --limit 20         # List recent 20 memos
  %(prog)s --tag work         # List memos with 'work' tag
  %(prog)s --search 报销       # Search for '报销' in content
        """
    )
    parser.add_argument("--limit", type=int, default=10,
                        help="Number of memos to show (default: 10)")
    parser.add_argument("--tag", help="Filter by tag")
    parser.add_argument("--search", help="Search in content")
    
    args = parser.parse_args()
    
    api_url = os.environ.get("MEMOS_API_URL")
    api_token = os.environ.get("MEMOS_API_TOKEN")
    
    if not api_url:
        print("Error: MEMOS_API_URL environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    if not api_token:
        print("Error: MEMOS_API_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    api_url = api_url.rstrip("/")
    
    return list_memos(api_url, api_token, args.limit, args.tag, args.search)


if __name__ == "__main__":
    sys.exit(main())
