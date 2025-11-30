import sys
from pathlib import Path

from loguru import logger
from shiny import App, ui


from kleinduimpje.view.root import get_dashboard_ui, server

LOG_LEVEL = "INFO"

# Setup settings and logger
logger.remove()
logger.add(sys.stderr, level=LOG_LEVEL)

# Combine clean shiny UI with CSS and external resources
ui_with_css = ui.TagList(ui.tags.link(href="style.css", rel="stylesheet"), get_dashboard_ui())

app_dir = Path(__file__).parent
app = App(ui_with_css, server, static_assets=app_dir / "www")
