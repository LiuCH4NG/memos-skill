#!/usr/bin/env python3
"""
Get a single memo detail from Memos via API.

Usage:
    python3 get_memo.py <memo_name_or_id>

Examples:
    python3 get_memo.py memos/NWmePf6May2iH85ALaoHhT
    python3 get_memo.py NWmePf6May2iH85ALaoHhT
"""

import argparse
import os
import sys
import urllib.request
import urllib.error
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
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return iso_time


def get_memo(api_url: str, api_token: str, memo_name: str):
    """Get a single memo detail from Memos."""
    
    # Ensure memo_name has memos/ prefix
    if not memo_name.startswith('memos/'):
        memo_name = f'memos/{memo_name}'
    
    endpoint = f"{api_url}/api/v1/{memo_name}"
    
    req = urllib.request.Request(
        endpoint,
        headers={
            "Authorization": f"Bearer {api_token}"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            memo = json.loads(response.read().decode("utf-8"))
            
            # Display memo details
            print("\n" + "=" * 60)
            print("📝 笔记详情")
            print("=" * 60)
            
            print(f"\n📄 名称: {memo.get('name', 'N/A')}")
            print(f"🔒 可见性: {memo.get('visibility', 'N/A')}")
            print(f"📌 置顶: {'是' if memo.get('pinned') else '否'}")
            
            tags = memo.get('tags', [])
            print(f"🏷️  标签: {', '.join(tags) if tags else '无'}")
            
            print(f"\n🕐 创建时间: {format_time(memo.get('createTime', ''))}")
            print(f"🔄 更新时间: {format_time(memo.get('updateTime', ''))}")
            
            print(f"\n" + "-" * 60)
            print("📝 内容:")
            print("-" * 60)
            print(memo.get('content', 'N/A'))
            print("=" * 60)
            
            return 0
            
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"❌ 笔记不存在: {memo_name}", file=sys.stderr)
        else:
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
        description="Get a memo detail from Memos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s memos/NWmePf6May2iH85ALaoHhT
  %(prog)s NWmePf6May2iH85ALaoHhT
        """
    )
    parser.add_argument("memo", help="Memo name or ID (e.g., 'memos/xxx' or just 'xxx')")
    
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
    
    return get_memo(api_url, api_token, args.memo)


if __name__ == "__main__":
    sys.exit(main())
