from shiny import module, ui
import shinyswatch

# def get_dashboard_ui() -> ui.Tag:
#     return ui.page_fluid(
#         # This example shows how custom Shiny for Python apps can be!
#         ui.card(
#             ui.row(
#                 ui.column(
#                     7,
#                     ui.h1(
#                         ui.span("Tapyr", style="color: #486590; font-size: 3rem;"),
#                         " | Shiny for Python Template by ",
#                         ui.span("Appsilon", style="color: #007bff; font-size: 3rem;"),
#                     ),
#                     ui.output_ui("link_button"),
#                     style="padding: 2rem;",
#                 ),
#                 ui.column(
#                     5,
#                     ui.img(src="images/tapyr.png", style="width: 300px; display: block; margin: 0 auto;"),
#                 ),
#             ),
#         ),
#         style="display: flex; justify-content: center; align-items: center; height: 100vh;",
#     )


def get_dashboard_ui() -> ui.Tag:
    return ui.page_fillable(
        ui.panel_title("Klein Duimpje: Route Visualizer"),
        ui.div(ui.output_ui("loading_message"), ui.output_ui("maps_container"), class_="p-3"),
        theme=shinyswatch.theme.flatly,
    )


@module.ui
def gpx_map_ui():
    return ui.div(
        ui.card(
            ui.card_header(ui.output_text("card_title")),
            output_widget("map_widget"),
            height="400px",
        ),
        style="min-width: 350px; flex: 1;",
    )
