"""Push event handler."""

from astrbot.api import logger

from ..formatters.push_formatter import format_push_message


async def handle_push_event(data: dict, context):
    """Handle push event from GitHub webhook."""
    try:
        pusher = data.get("pusher", {})
        author_name = pusher.get("name", "Unknown")

        repository = data.get("repository", {})
        repo_name = repository.get("full_name", "Unknown")

        ref = data.get("ref", "")
        branch = ref.replace("refs/heads/", "") if ref else "Unknown"

        commits = data.get("commits", [])
        if not commits:
            logger.warning("GitHub Webhook: Push event has no commits")
            return None

        # 方案 B：不再只取 commits[0]，而是把全部 commit 交给格式化层渲染，
        # 由格式化层按上限折叠为摘要，避免多条提交被静默丢弃。
        message = format_push_message(
            author_name=author_name,
            repo_name=repo_name,
            branch=branch,
            commits=commits,
        )

        return message

    except Exception as e:
        logger.error(f"GitHub Webhook: Error handling push event: {e}")
        return None
