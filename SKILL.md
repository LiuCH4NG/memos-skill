---
name: memos-note
description: Create and manage notes in Memos via API. Use when user asks to "记录笔记", "创建笔记", "记笔记", "save note", "create memo", "delete memo", "list memos", or any request to manage Memos notes.
---

# Memos Note Skill

Create, delete, and manage notes in a Memos instance via its REST API.

## Prerequisites

Environment variables are loaded from `.env` file automatically, or can be set manually:

- `MEMOS_API_URL` - The base URL of your Memos instance (e.g., `https://memos.example.com`)
- `MEMOS_API_TOKEN` - Your Memos API access token

## Usage

### Create a Note

When user asks to record a note:

1. Extract the note content from user's request
2. Call the `scripts/create_memo.py` script with the content
3. Report success or failure

```bash
# Create a simple note
python3 ~/.openclaw/skills/memos-note/scripts/create_memo.py "This is my note content"

# Create a note with tags
python3 ~/.openclaw/skills/memos-note/scripts/create_memo.py "Meeting notes" --tags "work,meeting"
```

### Delete a Note (Requires Confirmation!)

When user asks to delete a note:

1. **MUST** show the note details and ask for confirmation
2. Call the `scripts/delete_memo.py` script
3. User must type "DELETE" to confirm

```bash
# Delete a note (will prompt for confirmation)
python3 ~/.openclaw/skills/memos-note/scripts/delete_memo.py "memos/xxx"

# Delete by ID only
python3 ~/.openclaw/skills/memos-note/scripts/delete_memo.py "xxx"

# Force delete without confirmation (DANGEROUS - use only when explicitly requested)
python3 ~/.openclaw/skills/memos-note/scripts/delete_memo.py "memos/xxx" --force
```

**IMPORTANT:** Never use `--force` unless user explicitly asks to skip confirmation!

### List Notes

When user asks to view recent notes or list memos:

```bash
# List recent 10 notes
python3 ~/.openclaw/skills/memos-note/scripts/list_memos.py

# List more notes
python3 ~/.openclaw/skills/memos-note/scripts/list_memos.py --limit 20

# Search notes by content
python3 ~/.openclaw/skills/memos-note/scripts/list_memos.py --search "关键字"

# Filter by tag
python3 ~/.openclaw/skills/memos-note/scripts/list_memos.py --tag "work"
```

### Get Note Detail

When user asks to view a specific note:

```bash
# Get full detail of a note
python3 ~/.openclaw/skills/memos-note/scripts/get_memo.py "memos/xxx"

# Or just by ID
python3 ~/.openclaw/skills/memos-note/scripts/get_memo.py "xxx"
```

See [references/api.md](references/api.md) for detailed Memos API documentation.

## Error Handling

- If `MEMOS_API_URL` or `MEMOS_API_TOKEN` is not set, inform user to configure them in `.env` file
- If the API call fails, report the error details to user
