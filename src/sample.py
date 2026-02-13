from shiny import App, render, ui, reactive
import plotly.express as px
from ridgeplot import ridgeplot
import seaborn as sns
from shinywidgets import render_plotly, render_widget, output_widget

# use shiny run --reload --launch-browser src/sample.py to local test

tips = sns.load_dataset("tips")

# UI
app_ui = ui.page_fluid(
    ui.tags.style("body { font-size: 0.6em; }"),
    ui.panel_title("Restaurant tipping"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider(
                id="slider",
                label="Bill amount",
                min=tips.total_bill.min(),
                max=tips.total_bill.max(),
                value=[tips.total_bill.min(), tips.total_bill.max()],
            ),
            ui.input_checkbox_group(
                id="checkbox_group",
                label="Food service",
                choices={
                    "Lunch": "Lunch",
                    "Dinner": "Dinner",
                },
                selected=[
                    "Lunch",
                    "Dinner",
                ],
            ),
            ui.input_action_button("action_button", "Reset filter"),
            open="desktop",
        ),
        ui.layout_columns(
            ui.value_box("Total tippers", ui.output_text("total_tippers")),
            ui.value_box("Average tip", ui.output_text("average_tip")),
            ui.value_box("Average bill", ui.output_text("average_bill")),
            fill=False,
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Tips by day"),
                ui.output_data_frame("tips_data"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Total bill vs tip"),
                output_widget("scatterplot"),
                full_screen=True,
            ),
            col_widths=[6, 6],
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Tip percentages"),
                output_widget("ridge"),
                full_screen=True,
            )
        ),
    ),
)


# Server
def server(input, output, session):

    @reactive.calc
    def filtered_data():
        idx1 = tips.total_bill.between(
            left=input.slider()[0],
            right=input.slider()[1],
            inclusive="both",
        )
        idx2 = tips.time.isin(input.checkbox_group())
        tips_filtered = tips[idx1 & idx2]
        return tips_filtered

    @render.text
    def total_tippers():
        return str(filtered_data().shape[0])

    @render.text
    def average_tip():
        perc = filtered_data().tip / filtered_data().total_bill
        return f"{perc.mean():.1%}"

    @render.text
    def average_bill():
        bill = filtered_data().total_bill.mean()
        return f"${bill:.2f}"

    @render.data_frame
    def tips_data():
        df = filtered_data().copy()
        df["tip_pct"] = df.tip / df.total_bill
        summary = df.groupby("day").agg(
            count=("tip", "size"),
            avg_bill=("total_bill", "mean"),
            avg_tip=("tip", "mean"),
            avg_tip_pct=("tip_pct", "mean"),
        ).round(2).reset_index()
        return summary

    @render_plotly
    def scatterplot():
        return px.scatter(filtered_data(), x="total_bill", y="tip", trendline="lowess")

    @render_widget
    def ridge():
        df = filtered_data().copy()
        df["percent"] = df.tip / df.total_bill

        uvals = df.day.unique()
        samples = [[df.percent[df.day == val]] for val in uvals]

        plt = ridgeplot(
            samples=samples,
            labels=uvals,
            bandwidth=0.01,
            colorscale="viridis",
            colormode="row-index",
        )

        plt.update_layout(
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5
            )
        )

        return plt


# Create app
app = App(app_ui, server)