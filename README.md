# Memos Note Skill

OpenClaw skill for managing notes in [Memos](https://usememos.com/) via REST API.

## Features

- ✅ **Create** - Create notes with optional tags
- 📋 **List** - View recent notes
- 🔍 **Search** - Search notes by content
- 🏷️ **Filter** - Filter notes by tags
- 📄 **View** - Get detailed view of a single note
- 🗑️ **Delete** - Delete notes (with confirmation)

## Installation

### For Humans (推荐)

复制这段提示词发给你的 LLM Agent：

```
Install and configure the memos-note skill for OpenClaw by following the instructions here:
https://raw.githubusercontent.com/LiuCH4NG/memos-skill/refs/heads/master/README.md
```

或者简单说：

> "帮我安装 memos-note skill，用于管理 Memos 笔记"

然后提供你的 Memos 地址和 API Token 即可。

---

### For LLM Agents

如果你是帮助用户安装此 skill 的 LLM Agent，请按以下步骤操作：

#### Step 1: 检查 OpenClaw 是否已安装

```bash
if command -v openclaw &> /dev/null || [ -d "$HOME/.openclaw" ]; then
    echo "OpenClaw is installed"
else
    echo "OpenClaw not detected. Please install OpenClaw first."
    echo "Ref: https://docs.openclaw.ai"
fi
```

#### Step 2: 复制 skill 到 skills 目录

```bash
# 创建 skills 目录（如果不存在）
mkdir -p ~/.openclaw/skills

# 复制 skill 文件
cp -r memos-note ~/.openclaw/skills/

# 验证安装
ls -la ~/.openclaw/skills/memos-note/
```

#### Step 3: 配置环境变量

询问用户：
1. **Memos 实例地址**（如：`http://182.92.163.3:5230`）
2. **API Token**（从 Memos Settings → API 获取）

然后创建 `.env` 文件：

```bash
cat > ~/.openclaw/skills/memos-note/.env << 'EOF'
MEMOS_API_URL=用户提供的地址
MEMOS_API_TOKEN=用户提供的token
EOF

# 设置安全权限
chmod 600 ~/.openclaw/skills/memos-note/.env
```

#### Step 4: 验证安装

```bash
# 测试列出笔记
python3 ~/.openclaw/skills/memos-note/scripts/list_memos.py --limit 3
```

如果成功显示笔记列表，则安装完成。

#### Step 5: 向用户确认

告知用户：
- ✅ Skill 已安装到 `~/.openclaw/skills/memos-note/`
- ✅ API 配置已保存（安全权限：600）
- ✅ 现在可以使用指令如：
  - "记录笔记：xxx"
  - "列出我的笔记"
  - "搜索关于 xxx 的笔记"
  - "删除笔记 memos/xxx"

---

### Manual Installation (手动安装)

如果你想手动安装：

#### Prerequisites

- Python 3.6+ (仅使用标准库，无需额外依赖)
- 一个运行中的 Memos 实例
- Memos API access token

#### Quick Install

```bash
# 1. 复制此 skill 到 OpenClaw skills 目录
cp -r memos-note ~/.openclaw/skills/

# 2. 进入 skill 目录
cd ~/.openclaw/skills/memos-note

# 3. 复制环境配置文件示例
cp .env.example .env

# 4. 编辑 .env 填入你的 Memos 凭证
nano .env
```

#### Configuration

编辑 `.env` 文件：

```bash
MEMOS_API_URL=http://your-memos-server:5230
MEMOS_API_TOKEN=your_api_token_here
```

**获取 API Token：**

1. 浏览器打开你的 Memos 实例
2. 点击头像 → **Settings**
3. 进入 **API** 标签页
4. 点击 **Create Access Token**
5. 复制生成的 token 到 `.env` 文件

#### Verify Installation

测试安装是否成功：

```bash
python3 scripts/list_memos.py --limit 5
```

如果配置正确，会显示最近的笔记列表。

#### Permission Setup (可选但推荐)

保护你的 `.env` 文件：

```bash
chmod 600 .env
```

## Configuration

Create a `.env` file in the skill directory:

```bash
MEMOS_API_URL=https://your-memos-instance.com
MEMOS_API_TOKEN=your_api_token_here
```

### Getting API Token

1. Open your Memos instance
2. Go to **Settings** → **API**
3. Click **Create Access Token**
4. Copy the token to your `.env` file

## Usage

### Create a Note

```bash
python3 scripts/create_memo.py "Your note content"
python3 scripts/create_memo.py "Meeting notes" --tags "work,meeting"
```

### List Notes

```bash
python3 scripts/list_memos.py                    # Recent 10 notes
python3 scripts/list_memos.py --limit 20         # Recent 20 notes
python3 scripts/list_memos.py --tag "work"       # Filter by tag
python3 scripts/list_memos.py --search "keyword" # Search content
```

### View Note Detail

```bash
python3 scripts/get_memo.py memos/xxx
python3 scripts/get_memo.py xxx  # ID only also works
```

### Delete Note

⚠️ **Requires confirmation!**

```bash
python3 scripts/delete_memo.py memos/xxx
# Then type "DELETE" to confirm
```

Force delete (use with caution):
```bash
python3 scripts/delete_memo.py memos/xxx --force
```

## File Structure

```
memos-note/
├── SKILL.md              # Skill definition for OpenClaw
├── README.md             # This file
├── .env                  # Your API credentials (not in git)
├── .env.example          # Template for .env
├── .gitignore            # Git ignore rules
├── scripts/
│   ├── create_memo.py    # Create notes
│   ├── list_memos.py     # List/search notes
│   ├── get_memo.py       # Get note detail
│   └── delete_memo.py    # Delete notes
└── references/
    └── api.md            # API documentation
```

## Safety Features

- **Delete confirmation** - Must type "DELETE" to confirm deletion
- **Environment isolation** - Credentials stored in `.env` file (chmod 600)
- **URL encoding** - Proper encoding for search/filter queries
- **Error handling** - Clear error messages for common issues

## License

MIT - Feel free to use and modify!
