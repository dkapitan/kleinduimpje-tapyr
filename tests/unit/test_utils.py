import tempfile
from pathlib import Path

import pytest

from kleinduimpje.logic.utils import divide, load_config
from tests.helpers.logging_helpers import log_contain_message


def test_load_config_with_repository_url(tmp_path, monkeypatch):
    # Given: a pyproject.toml with repository URL in project.urls section
    pyproject_content = """
[project]
name = "test-project"

[project.urls]
Repository = "https://github.com/testuser/testrepo"
"""
    # Create directory structure to mimic kleinduimpje/logic/utils.py location
    logic_dir = tmp_path / "kleinduimpje" / "logic"
    logic_dir.mkdir(parents=True)
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)

    # Mock __file__ to point to the temp directory structure
    import kleinduimpje.logic.utils as utils_module

    original_file = utils_module.__file__
    monkeypatch.setattr(utils_module, "__file__", str(logic_dir / "utils.py"))

    # When
    result = load_config()

    # Then
    assert result == "testuser/testrepo"


def test_load_config_with_repository_url_trailing_slash(tmp_path, monkeypatch):
    # Given: a pyproject.toml with repository URL with trailing slash
    pyproject_content = """
[project]
name = "test-project"

[project.urls]
Repository = "https://github.com/testuser/testrepo/"
"""
    # Create directory structure to mimic kleinduimpje/logic/utils.py location
    logic_dir = tmp_path / "kleinduimpje" / "logic"
    logic_dir.mkdir(parents=True)
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)

    # Mock __file__ to point to the temp directory structure
    import kleinduimpje.logic.utils as utils_module

    monkeypatch.setattr(utils_module, "__file__", str(logic_dir / "utils.py"))

    # When
    result = load_config()

    # Then
    assert result == "testuser/testrepo"


def test_load_config_with_tool_kleinduimpje_fallback(tmp_path, monkeypatch):
    # Given: a pyproject.toml with tool.kleinduimpje.github_repo
    pyproject_content = """
[project]
name = "test-project"

[tool.kleinduimpje]
github_repo = "fallbackuser/fallbackrepo"
"""
    # Create directory structure to mimic kleinduimpje/logic/utils.py location
    logic_dir = tmp_path / "kleinduimpje" / "logic"
    logic_dir.mkdir(parents=True)
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)

    # Mock __file__ to point to the temp directory structure
    import kleinduimpje.logic.utils as utils_module

    monkeypatch.setattr(utils_module, "__file__", str(logic_dir / "utils.py"))

    # When
    result = load_config()

    # Then
    assert result == "fallbackuser/fallbackrepo"


def test_load_config_prefers_repository_url_over_tool_config(tmp_path, monkeypatch):
    # Given: a pyproject.toml with both repository URL and tool.kleinduimpje config
    pyproject_content = """
[project]
name = "test-project"

[project.urls]
Repository = "https://github.com/testuser/testrepo"

[tool.kleinduimpje]
github_repo = "fallbackuser/fallbackrepo"
"""
    # Create directory structure to mimic kleinduimpje/logic/utils.py location
    logic_dir = tmp_path / "kleinduimpje" / "logic"
    logic_dir.mkdir(parents=True)
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)

    # Mock __file__ to point to the temp directory structure
    import kleinduimpje.logic.utils as utils_module

    monkeypatch.setattr(utils_module, "__file__", str(logic_dir / "utils.py"))

    # When
    result = load_config()

    # Then: repository URL should be preferred
    assert result == "testuser/testrepo"


def test_load_config_with_no_pyproject_toml(tmp_path, monkeypatch):
    # Given: no pyproject.toml file exists
    # Create directory structure to mimic kleinduimpje/logic/utils.py location
    logic_dir = tmp_path / "kleinduimpje" / "logic"
    logic_dir.mkdir(parents=True)

    # Mock __file__ to point to the temp directory structure
    import kleinduimpje.logic.utils as utils_module

    monkeypatch.setattr(utils_module, "__file__", str(logic_dir / "utils.py"))

    # When
    result = load_config()

    # Then: should return default fallback
    assert result == "dkapitan/kleinduimpje-tapyr"


def test_load_config_with_empty_pyproject_toml(tmp_path, monkeypatch):
    # Given: an empty pyproject.toml
    # Create directory structure to mimic kleinduimpje/logic/utils.py location
    logic_dir = tmp_path / "kleinduimpje" / "logic"
    logic_dir.mkdir(parents=True)
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("")

    # Mock __file__ to point to the temp directory structure
    import kleinduimpje.logic.utils as utils_module

    monkeypatch.setattr(utils_module, "__file__", str(logic_dir / "utils.py"))

    # When
    result = load_config()

    # Then: should return default fallback
    assert result == "dkapitan/kleinduimpje-tapyr"


def test_load_config_with_incomplete_repository_url(tmp_path, monkeypatch):
    # Given: a pyproject.toml with a malformed repository URL (not enough parts)
    pyproject_content = """
[project]
name = "test-project"

[project.urls]
Repository = "https://github.com/testrepo"
"""
    # Create directory structure to mimic kleinduimpje/logic/utils.py location
    logic_dir = tmp_path / "kleinduimpje" / "logic"
    logic_dir.mkdir(parents=True)
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)

    # Mock __file__ to point to the temp directory structure
    import kleinduimpje.logic.utils as utils_module

    monkeypatch.setattr(utils_module, "__file__", str(logic_dir / "utils.py"))

    # When
    result = load_config()

    # Then: should return default fallback
    assert result == "dkapitan/kleinduimpje-tapyr"
