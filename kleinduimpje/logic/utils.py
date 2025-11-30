from dataclasses import dataclass, field
import tomllib
from typing import List
from pathlib import Path
import xml.etree.ElementTree as ET

from fsspec.implementations.github import GithubFileSystem
from loguru import logger


@dataclass
class GitHubFS:
    org: str = "dkapitan"
    repo: str = "kleinduimpje-tapyr"
    branch: str = "main"
    gfs: GithubFileSystem = field(init=False)
    gpx_folder: str = "data"
    gpx_files: List = field(init=False)

    def __post_init__(self):
        """Load GitHub repository configuration from pyproject.toml"""

        pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                repo_url = data.get("project", {}).get("urls", {}).get("Repository", "")
                if repo_url:
                    parts = repo_url.rstrip("/").split("/")
                    if len(parts) >= 2:
                        self.org = parts[-2]
                        self.repo = parts[-1]

                # Fallback to tool.kleinduimpje section if exists
                tool_config = data.get("tool", {}).get("kleinduimpje", {})
                if "github_repo" in tool_config:
                    self.org, self.repo = tool_config["github_repo"].split("/")

        self.gfs = GithubFileSystem(org=self.org, repo=self.repo, sha=self.branch)
        self.gpx_files = self.gfs.glob(self.gpx_folder + "/*.gpx")


@logger.catch(reraise=True)
def fetch_and_parse_gpx(github_path, fs: GitHubFS):
    """Fetch and parse GPX file from GitHubFS"""
    try:
        # Read file content
        with fs.gfs.open(github_path, "r") as f:
            content = f.read()

        return parse_gpx_content(content, Path(github_path).name)
    except Exception as e:
        print(f"Error fetching GPX from {github_path}: {e}")
        return None, (52.0, 5.0), []


@logger.catch(reraise=True)
def parse_gpx_content(content, filename):
    """Parse GPX XML content"""
    points = []
    name = filename.replace(".gpx", "")

    try:
        root = ET.fromstring(content)

        # Define namespace
        ns = {"gpx": "http://www.topografix.com/GPX/1/1"}

        # Try to get track name
        trk_name = root.find(".//gpx:trk/gpx:name", ns)
        if trk_name is not None and trk_name.text:
            name = trk_name.text

        # Extract track points
        for trkpt in root.findall(".//gpx:trkpt", ns):
            lat = float(trkpt.get("lat"))
            lon = float(trkpt.get("lon"))
            points.append((lat, lon))

        # If no track points, try route points
        if not points:
            for rtept in root.findall(".//gpx:rtept", ns):
                lat = float(rtept.get("lat"))
                lon = float(rtept.get("lon"))
                points.append((lat, lon))

    except Exception as e:
        print(f"Error parsing GPX content: {e}")

    # Calculate center
    if points:
        avg_lat = sum(p[0] for p in points) / len(points)
        avg_lon = sum(p[1] for p in points) / len(points)
        center = (avg_lat, avg_lon)
    else:
        center = (52.0, 5.0)

    return name, center, points
