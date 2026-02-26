from shiny import App, render, ui, reactive
from shiny.types import ImgData
import plotly.express as px
from ridgeplot import ridgeplot
import seaborn as sns
from shinywidgets import render_plotly, render_widget, output_widget
import pandas as pd


# use shiny run --reload --launch-browser src/app.py to local test

sales_df = pd.read_csv("data/raw/sales_and_customer_insights.csv", parse_dates=True)
sales_df["risk_value"] = sales_df["Lifetime_Value"]*sales_df["Churn_Probability"]

# Macro functions for components

kpi_component = ui.layout_columns(
    ui.layout_columns(
        ui.value_box("Average Lifetime Value", ui.output_text("kpi_lifetime")),
        ui.value_box("Average Churn Rate", ui.output_text("kpi_churn")),
        ui.value_box("Average Value-At-Risk", ui.output_text("kpi_risk")),
        ui.value_box("Average Days Per Purchase", ui.output_text("kpi_days")),
        col_widths = (6,6,6,6)
    ),
    ui.value_box("Count of Datapoints", ui.output_ui("kpi_count")),
    col_widths = (8,4), # 12 part ratio
    # row_heights= (1,2), # direct ratio
    fill=False
)



# UI
app_ui = ui.page_fluid(
    ui.tags.style("body { font-size: 0.6em; }"),
    ui.panel_title("Salescope"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider(
                id="slider_churn",
                label="Churn Rate",
                min=0.0,
                max=1.0,
                value=[0.0, 1.0],
            ),
            ui.input_slider(
                id="slider_customer",
                label="Customer Lifetime Value",
                min=100,
                max=10000,
                value=[100, 10000],
            ),
            ui.input_slider(
                id="slider_order",
                label="Average Order Value",
                min=20,
                max=200,
                value=[20, 200],
            ),
            ui.input_slider(
                id="slider_freq",
                label="Purchase Frequency",
                min=1,
                max=19,
                value=[1, 19],
            ),             
            ui.input_date_range("inDateRange", "Input date"),
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
                id="checkbox_group_region",
                label="Region",
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
        
            ui.input_action_button("action_button", "Apply filter"),
            open="desktop",
        ),
        kpi_component,
        ui.navset_bar(
            ui.nav_panel("User Story 1", 
                ui.layout_columns(
                    ui.input_select(id = "row_dropdown",
                                    label = "Table partition options:",
                                    choices = ["Region","Retention Strategy","Most Frequent Value"]),
                    ui.navset_card_tab( # replace each of these with instances of ui.output_data_frame
                        ui.nav_panel("Customer Lifetime Value", ui.output_data_frame("customer_df")),
                        ui.nav_panel("Value-at-risk", ui.output_data_frame("risk_df")),
                        ui.nav_panel("Order Value", ui.output_data_frame("order_df")),
                        ui.nav_panel("Purchase Frequency", ui.output_data_frame("frequency_df")),
                        id = "multitabtable"
                    ),
                    col_widths = [3,9]
                ),
            ),       
            ui.nav_panel("User Story 2", 
                ui.layout_columns(
                    ui.card(
                        ui.card_header("High Churn Risk Scatterplot"),
                        ui.output_image("high_churn_risk"), # placeholder, swap with below for M2
                        #output_widget("high_churn_risk"),
                        full_screen=True,
                    ),
                    col_widths=[12],
                ),
            ),
            ui.nav_panel("User Story 3", 
                ui.layout_columns(
                        ui.card(
                            ui.card_header("Seasonal and Product Type Heatmap"),
                            ui.output_image("heatmap"), # placeholder, swap with below for M2
                            #output_widget("heatmap"),
                            full_screen=True,
                        ),
                        col_widths=[12],
                    ),
            ),
            title = "SaleScope"
        )
        
    )
    
)


def create_summary_table(df,grouping,feature):
    summary = df.groupby(grouping).agg(
        Count=(feature, "size"),
        Mean=(feature, "mean"),
        Median=(feature, "median"),
        Maximum=(feature, "max"),
        Total=(feature, "sum")
    ).round(2).reset_index()
    return summary

# Server
def server(input, output, session):
    
    @reactive.calc
    def filtered_df():
        df = sales_df.copy()

        churn_min, churn_max = input.slider_churn()
        clv_min, clv_max = input.slider_customer()
        order_min, order_max = input.slider_order()
        freq_min, freq_max = input.slider_freq()

        df = df[df["Churn_Probability"].between(churn_min, churn_max)]
        df = df[df["Lifetime_Value"].between(clv_min, clv_max)]
        df = df[df["Average_Order_Value"].between(order_min, order_max)]
        df = df[df["Purchase_Frequency"].between(freq_min, freq_max)]

        return df
        
    @render.text
    def kpi_lifetime():
        return "5432.86"

    @render.text
    def kpi_churn():
        return "0.727"

    @render.text
    def kpi_risk():
        return "1234.64"

    @render.text
    def kpi_days():
        return "5.315"

    

    @render.data_frame
    def customer_df():
        return create_summary_table(filtered_df(),"Region","Lifetime_Value")

    @render.data_frame
    def risk_df():
        return create_summary_table(filtered_df(),"Region","risk_value") # still need to compute risk column here

    @render.data_frame
    def order_df():
        return create_summary_table(filtered_df(),"Region","Average_Order_Value")

    @render.data_frame
    def frequency_df():
        return create_summary_table(filtered_df(),"Region","Purchase_Frequency")

    @render.image # Change to widget/plotly for M2
    def high_churn_risk():
        img: ImgData = {"src": "img/markup-user2.png"}
        return img
    
    @render.image # Change to widget/plotly for M2
    def heatmap():
        img: ImgData = {"src": "img/markup-user3.png"}
        return img
    
    @render.text
    def kpi_count():
        return f"{len(filtered_df()):,}"

    
    

    


# Create app
app = App(app_ui, server)