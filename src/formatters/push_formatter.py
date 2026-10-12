"""Push event formatter."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

# 单个事件最多逐条展示的 commit 数量，超出部分折叠为摘要，避免消息过长
MAX_DISPLAYED_COMMITS = 5


def _normalize_commit(commit: Mapping[str, Any]) -> dict[str, str]:
    """Normalize a single GitHub commit object into display fields."""
    return {
        "message": (commit.get("message") or "No message").strip().splitlines()[0],
        "url": commit.get("url", ""),
        "id": (commit.get("id") or "")[:7],
    }


def _format_commit_line(index: int, commit: Mapping[str, str]) -> str:
    """Format a single commit into a multi-line text block."""
    return (
        f"  {index}. 💬 {commit['message']}\n"
        f"     🔗 {commit['id']}\n"
        f"     📎 {commit['url']}"
    )


def format_push_message(
    author_name: str,
    repo_name: str,
    branch: str,
    commits: Iterable[Mapping[str, Any]],
) -> str:
    """Format push event message with all commits folded into a summary."""
    normalized = [_normalize_commit(c) for c in commits]
    total = len(normalized)

    lines = [
        "📦 GitHub Push Event",
        f"👤 {author_name} pushed to {repo_name}",
        f"🌿 Branch: {branch}",
        f"🧾 Commits: {total}",
    ]

    # 逐条展示，超出上限的部分折叠为摘要，避免消息过长
    displayed = normalized[:MAX_DISPLAYED_COMMITS]
    lines.append("")
    lines.extend(_format_commit_line(i, c) for i, c in enumerate(displayed, start=1))

    hidden = total - len(displayed)
    if hidden > 0:
        lines.append(f"  … 其余 {hidden} 个 commit 已折叠")

    return "\n".join(lines)
