import tomllib
from pathlib import Path

from loguru import logger


@logger.catch(reraise=True)
def divide(x: int, y: int) -> float:
    """
    The purpose of this function is to illustrate where to put functions in the template.
    Additionally it shows how to use loguru to catch exceptions and log them.
    """

    return x / y


@logger.catch(reraise=True)
def load_config():
    """Load GitHub repository configuration from pyproject.toml"""
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"

    if pyproject_path.exists():
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

            # Extract repository URL from project metadata
            repo_url = data.get("project", {}).get("urls", {}).get("Repository", "")

            if repo_url:
                # Parse GitHub repo from URL (e.g., https://github.com/user/repo)
                parts = repo_url.rstrip("/").split("/")
                if len(parts) >= 2:
                    return f"{parts[-2]}/{parts[-1]}"

            # Fallback to tool.kleinduimpje section if exists
            tool_config = data.get("tool", {}).get("kleinduimpje", {})
            if "github_repo" in tool_config:
                return tool_config["github_repo"]

    # Default fallback
    return "dkapitan/kleinduimpje-tapyr"
