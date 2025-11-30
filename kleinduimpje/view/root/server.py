from shiny import Inputs, Outputs, Session, reactive, module, render, ui

from kleinduimpje.view.root.ui import gpx_map_ui
from kleinduimpje.logic.utils import GitHubFS

fs = GitHubFS()


@module.server
def gpx_map_server(input, output, session, github_path):
    gpx_data = reactive.Value(None)

    @reactive.effect
    def _():
        data = fetch_and_parse_gpx(github_path)
        gpx_data.set(data)

    @render_widget
    def map_widget():
        data = gpx_data.get()

        if data is None:
            # Return empty map while loading
            return Map(basemap=basemaps.OpenStreetMap.Mapnik, center=(52.0, 5.0), zoom=7)

        name, center, points = data

        m = Map(basemap=basemaps.OpenStreetMap.Mapnik, center=center, zoom=13, scroll_wheel_zoom=True)

        if points:
            line = Polyline(locations=points, color="#2563eb", fill=False, weight=4, opacity=0.8)
            m.add_layer(line)

        return m

    @render.text
    def card_title():
        data = gpx_data.get()
        if data is None:
            return f"Loading {github_path}..."
        return data[0]


def server(input: Inputs, output: Outputs, session: Session):
    # @render.ui
    # def link_button():
    #     """
    #     UI link that looks like a button. This element could be placed directly in the UI definition
    #     but is here to showcase testing.
    #     """
    #     return ui.a(
    #         "Start with the docs!",
    #         href="https://appsilon.github.io/tapyr-docs/",
    #         target="_blank",
    #         class_="docs-link",
    #     )

    @render.ui
    def loading_message():
        files = fs.gpx_files
        if not files:
            return ui.div(ui.p("Loading GPX files from GitHub...", class_="text-muted"))
        return ui.p(f"Visualizing {len(files)} GPX routes", class_="lead")

    @render.ui
    def maps_container():
        files = fs.gpx_files

        if not files:
            return ui.div()

        # Create horizontally stacked cards
        return ui.div(
            *[gpx_map_ui(f.replace(".gpx", "")) for f in files],
            style="display: flex; gap: 20px; flex-wrap: wrap; overflow-x: auto;",
        )

    # Initialize map servers for each file
    @reactive.effect
    def _():
        files = gpx_files.get()
        for f in files:
            module_id = f.replace(".gpx", "")
            gpx_map_server(module_id, f)
