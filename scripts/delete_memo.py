#!/usr/bin/env python3
"""
Delete a memo from Memos via API.
Requires user confirmation before deletion.

Usage:
    python3 delete_memo.py <memo_name_or_id> [--force]

Examples:
    python3 delete_memo.py memos/NWmePf6May2iH85ALaoHhT
    python3 delete_memo.py NWmePf6May2iH85ALaoHhT
    python3 delete_memo.py memos/NWmePf6May2iH85ALaoHhT --force  # Skip confirmation
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
                    if key not in os.environ:
                        os.environ[key] = value


def get_memo(api_url: str, api_token: str, memo_name: str):
    """Get memo details before deletion."""
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
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: Memo not found: {memo_name}", file=sys.stderr)
        else:
            error_body = e.read().decode("utf-8")
            print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
            print(f"Response: {error_body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error fetching memo: {e}", file=sys.stderr)
        return None


def delete_memo(api_url: str, api_token: str, memo_name: str, force: bool = False):
    """Delete a memo from Memos with confirmation."""
    
    # Ensure memo_name has memos/ prefix
    if not memo_name.startswith('memos/'):
        memo_name = f'memos/{memo_name}'
    
    # First, get memo details to show user what will be deleted
    memo = get_memo(api_url, api_token, memo_name)
    if not memo:
        return 1
    
    # Show memo details
    print("\n" + "="*50)
    print("⚠️  即将删除以下笔记：")
    print("="*50)
    print(f"名称: {memo.get('name', 'N/A')}")
    print(f"内容: {memo.get('content', 'N/A')[:100]}")
    if len(memo.get('content', '')) > 100:
        print("... (内容已截断)")
    print(f"创建时间: {memo.get('createTime', 'N/A')}")
    print(f"标签: {', '.join(memo.get('tags', [])) or '无'}")
    print("="*50)
    
    # Require confirmation unless --force is used
    if not force:
        print("\n⚠️  警告：此操作不可恢复！")
        confirmation = input(f"确认删除? 请输入 'DELETE' 确认: ")
        if confirmation != "DELETE":
            print("❌ 删除已取消")
            return 1
    else:
        print("\n⚠️  强制删除模式 (跳过确认)")
    
    # Perform deletion
    endpoint = f"{api_url}/api/v1/{memo_name}"
    
    req = urllib.request.Request(
        endpoint,
        headers={
            "Authorization": f"Bearer {api_token}"
        },
        method="DELETE"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"✅ 笔记已删除: {memo_name}")
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
        description="Delete a memo from Memos (requires confirmation)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s memos/NWmePf6May2iH85ALaoHhT
  %(prog)s NWmePf6May2iH85ALaoHhT
  %(prog)s memos/NWmePf6May2iH85ALaoHhT --force  # Skip confirmation (dangerous!)
        """
    )
    parser.add_argument("memo", help="Memo name or ID (e.g., 'memos/xxx' or just 'xxx')")
    parser.add_argument("--force", action="store_true", 
                        help="Skip confirmation prompt (DANGEROUS!)")
    
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
    
    return delete_memo(api_url, api_token, args.memo, args.force)


if __name__ == "__main__":
    sys.exit(main())
