from shiny import App, render, ui, reactive
from shiny.types import ImgData
import plotly.express as px
from ridgeplot import ridgeplot
import seaborn as sns
from shinywidgets import render_plotly, render_widget, output_widget
import pandas as pd
import os
from dotenv import load_dotenv
import querychat
from chatlas import ChatAnthropic
import duckdb

# used LLM to know how to show actual count/mean inside the box for heatmap
# used querychat-explore.ipynb notes for querychat integration

# use shiny run --reload --launch-browser src/app.py to local test
load_dotenv()
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

sales_df = pd.read_csv("data/raw/sales_and_customer_insights.csv", parse_dates=True)
sales_df["risk_value"] = sales_df["Lifetime_Value"]*sales_df["Churn_Probability"]
sales_df["Launch_Date"] = pd.to_datetime(sales_df["Launch_Date"], format = "%Y-%m-%d")
min_date, max_date = sales_df["Launch_Date"].min().date(), sales_df["Launch_Date"].max().date()

qc = querychat.QueryChat(
    sales_df.copy(),
    "Salescope",
    greeting=" Hi! I'm your Salescope Assistant. Feel free to ask me to filter by region, category, churn risk or other relevant questions!",
    data_description="""
    This is Sales insights dataset
    Columns:
    - Region: Asia, Europe, North America, South America
    - Most_Frequent_Category: Clothing, Electronics, Home, Sports
    - Lifetime_Value: Numerical float
    - Churn_Probability: Float (0 to 1)
    - Retention_Strategy: Discount, Email Campaign, Loyalty Program
    """,
    client=ChatAnthropic(model="claude-sonnet-4-0", api_key=API_KEY),
)

kpi_component = ui.layout_columns(
    ui.layout_columns(
        ui.value_box("Average Lifetime Value", ui.output_text("kpi_lifetime")),
        ui.value_box("Average Churn Rate", ui.output_text("kpi_churn")),
        ui.value_box("Average Value-At-Risk", ui.output_text("kpi_risk")),
        ui.value_box("Average Days Per Purchase", ui.output_text("kpi_days")),
        col_widths = (6,6,6,6)
    ),
    ui.value_box("Count of Datapoints", ui.output_text("kpi_count")),
    col_widths = (8,4), # 12 part ratio
    # row_heights= (1,2), # direct ratio
    fill=False
)

main_sidebar = ui.sidebar(
    ui.input_numeric(
        id="num_churn_min",
        label="Churn rate min",
        value=0.0,
        min=0.0,
        max=1.0,
        step=0.01,
    ),
    ui.input_numeric(
        id="num_churn_max",
        label="Churn rate max",
        value=1.0,
        min=0.0,
        max=1.0,
        step=0.01,
    ),
    ui.input_slider(
        id="slider_churn_decrease",
        label="Churn rate decrease (%)",
        min=0,
        max=100,
        value=0,
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
    ui.input_date_range(
        id="date_range", 
        label="Filter by launch date",
        start=min_date,
        end=max_date,
        min=min_date,
        max=max_date
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

        ],
    ),

    ui.input_action_button("reset", "Reset filters"),
    open="desktop",
)


# Specialized table for User Story 1
panel_1 = ui.nav_panel("KPI Tables", 
    ui.layout_columns(
        ui.input_select(id = "row_dropdown",
                        label = "Table partition options:",
                        choices = ["Region","Retention Strategy","Most Frequent Value"]),
        ui.navset_card_tab(
            ui.nav_panel("Customer Lifetime Value", ui.output_data_frame("customer_df")),
            ui.nav_panel("Value-at-risk", ui.output_data_frame("risk_df")),
            ui.nav_panel("Order Value", ui.output_data_frame("order_df")),
            ui.nav_panel("Purchase Frequency", ui.output_data_frame("frequency_df")),
            id = "multitabtable"
        ),
        col_widths = [3,9]
    ),
)

# Specialized plot for User Story 2
panel_2 = ui.nav_panel("Churn Risk Plot", 
    ui.layout_columns(
        ui.card(
            output_widget("high_churn_risk"),
            full_screen=True,
        ),
        ui.card(
            output_widget("quartile_churn_risk"),
            full_screen=True,
        ),
        col_widths=[8, 4],
    ),
)

# Specialized plot for User Story 3
panel_3 = ui.nav_panel("Seasonal Product Heatmap", 
    ui.layout_columns(
        ui.card(
            ui.card_header("Heatmap settings"),
            ui.input_radio_buttons(
                "heatmap_metric", 
                "Select metric:", 
                {
                "mean": "Avg customer value", 
                "count": "Frequency (Count of entries)" },
                selected="mean"
               ),
            ui.help_text("Choose 'Frequency' to see total number of transactions per season.")
              ),
        ui.card(
            ui.card_header("Seasonal & Product Type Heatmap"),
            output_widget("heatmap"),
            full_screen=True,
        ),
        col_widths=[3, 9], ),
)

#panel for AI insights
panel_ai = ui.nav_panel("AI Insights", 
    ui.layout_sidebar(
        #AI chat interface
        qc.sidebar(),
        ui.download_button("download_ai_filtered", "⬇️ Download Filtered Dataframe"),
        ui.layout_columns(
            ui.card(
                ui.card_header("AI Filtered Data"),
                ui.output_data_frame("ai_data_table")
            )
        )
    )
)

# UI
app_ui = ui.page_navbar(
    ui.nav_panel(
        "Advanced Figures",
        ui.navset_card_tab(
            panel_1,
            panel_2,
            panel_3, 
            id="advanced_nav"
        )
    ),
    panel_ai, 
    title="Salescope", 
    sidebar=main_sidebar,
    header=ui.TagList(
        ui.tags.style("body { font-size: 0.8em; }"), 
        kpi_component,
    ),
    id="top_navbar",
    theme=ui.Theme("lumen")
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
    
    qc_vals = qc.server()
    
    @reactive.calc
    def ai_filtered_df():
        return qc_vals.df()

    @render.data_frame
    def ai_data_table():
        return ai_filtered_df()
    
    @render.download(filename="sales_and_customer_insights_ai_filtered.csv")
    def download_ai_filtered():
        yield ai_filtered_df().to_csv(index=False)

    @reactive.calc
    def filtered_df():
        df = sales_df.copy()
        churn_min_raw = input.num_churn_min()
        churn_max_raw = input.num_churn_max()
        churn_min = min(churn_min_raw, churn_max_raw)
        churn_max = max(churn_min_raw, churn_max_raw)
        pct_decrease = input.slider_churn_decrease()

        clv_min, clv_max = input.slider_customer()
        order_min, order_max = input.slider_order()
        freq_min, freq_max = input.slider_freq()
        date_start, date_end = input.date_range()

        # Math: reduced_max = churn_max * (1 - pct_decrease / 100).
        reduced_max = churn_max * (1 - pct_decrease / 100)

        df = df[df["Churn_Probability"].between(churn_min, churn_max)]
        if pct_decrease > 0:
            df = df[df["Churn_Probability"] <= reduced_max]
            
        df["in_reduced_churn_range"] = (df["Churn_Probability"] >= churn_min) & (df["Churn_Probability"] <= reduced_max)
        df = df[df["Lifetime_Value"].between(clv_min, clv_max)]
        df = df[df["Average_Order_Value"].between(order_min, order_max)]
        df = df[df["Purchase_Frequency"].between(freq_min, freq_max)]
        df = df[df["Launch_Date"].between(pd.Timestamp(date_start),pd.Timestamp(date_end))]

        types = input.checkbox_group_type() 
        regions = input.checkbox_group_region() 
        strategies = input.checkbox_group_strategy() 

        if types:
            df = df[df["Most_Frequent_Category"].isin(types)]

        if regions:
            df = df[df["Region"].isin(regions)]

        if strategies:
            df = df[df["Retention_Strategy"].isin(strategies)]

        return df
    
    @reactive.effect
    @reactive.event(input.reset)
    def reset_filters():
        # Update the inputs to defaults
        ui.update_numeric(
            id="num_churn_min",
            value=0.0,
            session=session
        )
        ui.update_numeric(
            id="num_churn_max",
            value=1.0,
            session=session
        )
        ui.update_slider(
            id="slider_churn_decrease",
            value=0,
            session=session
        )
        ui.update_slider(
            id="slider_customer",
            value=[100, 10000],
            session=session
        )
        ui.update_slider(
            id="slider_order",
            value=[20, 200],
            session=session
        )
        ui.update_slider(
            id="slider_freq",
            value=[1, 19],
            session=session
        )
        ui.update_date_range(
            "date_range",
            start=min_date,
            end=max_date,
            min=min_date,
            max=max_date,
            session=session
        )
        ui.update_checkbox_group(
            id="checkbox_group_type",
            selected=[

            ],
            session=session
        )
        ui.update_checkbox_group(
            id="checkbox_group_region",
            selected=[
                
            ],
            session=session
        )
        ui.update_checkbox_group(
            id="checkbox_group_strategy",
            selected=[

            ],
            session=session
        )

    @render.text
    def kpi_lifetime():
        df = filtered_df()
        if df.empty:
            return "—"
        return f"${df['Lifetime_Value'].mean():,.2f}"

    @render.text
    def kpi_churn():
        df = filtered_df()
        if df.empty:
            return "—"
        return f"{df['Churn_Probability'].mean():.1%}"

    @render.text
    def kpi_risk():
        df = filtered_df()
        if df.empty:
            return "—"
        return f"${df['risk_value'].mean():,.2f}"

    @render.text
    def kpi_days():
        df = filtered_df()
        if df.empty:
            return "—"
        return f"{df['Time_Between_Purchases'].mean():,.2f} days"

    @render.data_frame
    def customer_df():
        mapping = {"Region": "Region",
            "Retention Strategy": "Retention_Strategy",
            "Most Frequent Value": "Most_Frequent_Category"
                    }
        group = mapping[input.row_dropdown()]
        return create_summary_table(filtered_df(), group, "Lifetime_Value")

    @render.data_frame
    def risk_df():
        mapping = {"Region": "Region", "Retention Strategy": "Retention_Strategy", "Most Frequent Value": "Most_Frequent_Category"}
        group = mapping[input.row_dropdown()]
        return create_summary_table(filtered_df(), group, "risk_value")

    @render.data_frame
    def order_df():
        mapping = {"Region": "Region", "Retention Strategy": "Retention_Strategy", "Most Frequent Value": "Most_Frequent_Category"}
        group = mapping[input.row_dropdown()]
        return create_summary_table(filtered_df(), group, "Average_Order_Value")

    @render.data_frame
    def frequency_df():
        mapping = {"Region": "Region", "Retention Strategy": "Retention_Strategy", "Most Frequent Value": "Most_Frequent_Category"}
        group = mapping[input.row_dropdown()]
        return create_summary_table(filtered_df(), group, "Purchase_Frequency")

    @render_widget
    def high_churn_risk():
        df = filtered_df()
        churn_min_raw = input.num_churn_min()
        churn_max_raw = input.num_churn_max()
        churn_min = min(churn_min_raw, churn_max_raw)
        churn_max = max(churn_min_raw, churn_max_raw)
        pct_decrease = input.slider_churn_decrease()
        reduced_max = churn_max * (1 - pct_decrease / 100)

        if df.empty:
            fig = px.scatter(title="No data available for current filters")
            return fig

        fig = px.scatter(
            df,
            x="Lifetime_Value",
            y="Time_Between_Purchases",
            color="Retention_Strategy",
            size="Churn_Probability",
            size_max=18,
            hover_data=["Customer_ID", "Region", "Churn_Probability", "Purchase_Frequency"],
        )
        fig.update_layout(
            title=f"Customers by Lifetime Value and Days Between Purchases, Churn Risk From {churn_min:0.2f} to {reduced_max:0.2f}",
            xaxis_title="Customer Lifetime Value",
            yaxis_title="Days Between Purchases",
            legend_title="Retention Strategy",
        )
        return fig
    
    @render_widget
    def quartile_churn_risk():
        df = filtered_df()
        
        if df.empty:
            return px.scatter(title="No data available for current filters")

        fig = px.box(
            df,
            x="Retention_Strategy",
            y="Churn_Probability",
            color="Retention_Strategy",
        )
        fig.update_layout(
            title="Churn Probability quartiles by Retention Strategy",
            xaxis_title="Retention Strategy",
            yaxis_title="Churn Probability",
            showlegend=False
        )
        return fig
    
    @render_widget
    def heatmap():
        df = filtered_df()
        
        if df.empty:
            return None
        # fetching value from  radio buttons
        metric = input.heatmap_metric()

        if metric == "count":
            plot_data = (
                df.groupby(["Season", "Most_Frequent_Category"])
                .size().reset_index(name="Frequency") )
            z_col = "Frequency"
            title_text = "Frequency of Sales: Season vs. Category"
            label_text = "Total Count"
        else:
            plot_data = (
                df.groupby(["Season", "Most_Frequent_Category"])["Lifetime_Value"]
                .mean()
                .reset_index()  )
            z_col = "Lifetime_Value"
            title_text = "Avg Customer Value: Season vs. Category"
            label_text = "Avg LTV"

        fig = px.density_heatmap(
            plot_data, 
            x="Season", 
            y="Most_Frequent_Category", 
            z=z_col,
            title=title_text,
            labels={z_col: label_text, 'Most_Frequent_Category': 'Product Type'},
            color_continuous_scale="Viridis",
            text_auto=True ) 
        
        return fig

    
    @render.text
    def kpi_count():
        return f"{len(filtered_df()):,}"


# Create app
app = App(app_ui, server)