from shiny import App, render, ui, reactive
import plotly.express as px
from ridgeplot import ridgeplot
import seaborn as sns
from shinywidgets import render_plotly, render_widget, output_widget

# use shiny run --reload --launch-browser src/app.py to local test


# UI
app_ui = ui.page_fluid(
    ui.tags.style("body { font-size: 0.6em; }"),
    ui.panel_title("Salescope"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider(
                id="slider_freq",
                label="Purchase Frequency",
                min=1,
                max=19,
                value=[1, 19],
            ),
            ui.input_slider(
                id="slider_value",
                label="Average Order Value",
                min=20,
                max=200,
                value=[20, 200],
            ),
            ui.input_slider(
                id="slider_time",
                label="Time Between Purchase",
                min=5,
                max=89,
                value=[5, 89],
            ),
            
            ui.input_checkbox_group(
                id="checkbox_group_type",
                label="Most Common Purchase Type",
                choices={
                    "Clothing": "Clothing",
                    "Electronics": "Electronics",
                    "Home": "Home",
                    "Sports": "Sports",
                    
                },
                selected=[
                    "Clothing",
                ],
            ),

            ui.input_checkbox_group(
                id="checkbox_group_continent",
                label="Continent",
                choices={
                    "Asia": "Asia",
                    "Europe": "Europe",
                    "North America": "North America",
                    "South America": "South America",
                },
                selected=[
                    "North America",
                ],
            ),

            ui.input_checkbox_group(
                id="checkbox_group_strategy",
                label="Retention Strategy",
                choices={
                    "Discount": "Discount",
                    "Email Campaign": "Email Campaign",
                    "Loyalty Program": "Loyalty Program"
                },
                selected=[
                    "Discount",
                    "Email Campaign",
                    "Loyalty Program",
                ],
            ),
            
            ui.input_action_button("action_button", "Reset filter"),
            open="desktop",
        ),
        ui.layout_columns(
            ui.value_box("Average Churn Probability", "0.727"),
            ui.value_box("Average Lifetime Value", "5432.86"),
            ui.value_box("Count of Datapoints", "1234"),
            fill=False,
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Retention Strategy vs Lifetime Value"),
                ui.output_data_frame("tips_data"), # not definied placeholder
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Launch Date vs Lifetime Value"),
                output_widget("scatterplot"), # not definied placeholder
                full_screen=True,
            ),
            col_widths=[6, 6],
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Distribution of Lifetime Value"),
                output_widget("ridge"), # not definied placeholder
                full_screen=True,
            )
        ),
    ),
)


# Server
def server(input, output, session):
    pass


# Create app
app = App(app_ui, server)