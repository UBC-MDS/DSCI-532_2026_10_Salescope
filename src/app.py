from shiny import App, render, ui, reactive
from shiny.types import ImgData
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from shinywidgets import render_plotly, render_widget, output_widget
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import querychat
from chatlas import ChatAnthropic, ToolRejectError
import duckdb
from pathlib import Path

# src imports
from dflogic import create_summary_table, filter_sales_data
from db import get_base_dataframe, execute_filtered_query


# used LLM to know how to show actual count/mean inside the box for heatmap
# used LLM to plot trends over time
# used querychat-explore.ipynb notes for querychat integration

# use shiny run --reload --launch-browser src/app.py to local test

load_dotenv()
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

sales_df = execute_filtered_query()
sales_df["Churn_Probability"] = sales_df["Churn_Probability"].fillna(0)
sales_df["Value_At_Risk"] = sales_df["Lifetime_Value"] * sales_df["Churn_Probability"]
sales_df["Launch_Date"] = pd.to_datetime(sales_df["Launch_Date"])
min_date, max_date = sales_df["Launch_Date"].min().date(), sales_df["Launch_Date"].max().date()

# Determine the most recent quarter in the data
latest_quarter = pd.Period(max_date, freq='Q')
default_start = latest_quarter.start_time.date()
default_end = latest_quarter.end_time.date()

# domain context for the LLM - see notebooks/querychat_customization.ipynb for why we settled on this
SALESCOPE_EXTRA_INSTRUCTIONS = """
You are working inside the Salescope retention dashboard. Users are sales managers, not data scientists.

Value_At_Risk = Lifetime_Value * Churn_Probability. This is the dollar amount at risk if a customer churns.
Treat it as the most useful column when prioritizing interventions.

Rough churn thresholds: above 0.7 = high risk, 0.4-0.7 = medium, below 0.4 = low.

When you answer, say what it means for the business (e.g. "this region has $X at risk").
Keep responses short. Suggest which retention strategy fits when it's relevant.

If the user's question is outside the current analysis scope (churn-only or revenue-only), do not reinterpret it; instead, tell them which scope is active and suggest switching modes.

In Churn Focus mode, only query churn-related columns (e.g. Churn_Probability, Value_At_Risk, Region, Retention_Strategy). In Revenue Focus mode, only query revenue and value columns (e.g. Lifetime_Value, Average_Order_Value, Value_At_Risk).

If Churn_Probability is missing for a row, assume it is 0 when computing Value_At_Risk so that new customers without a modeled churn score do not inflate revenue-at-risk totals.
"""

qc = querychat.QueryChat(
    sales_df.copy(),
    "Salescope",
    greeting=(
        "Hi! I'm your Salescope AI Assistant. I can help you filter customers, "
        "analyze churn risk, and surface retention insights.\n\n"
        "Try asking:\n"
        "- *Show me high-risk customers in Asia*\n"
        "- *Which retention strategy has the highest average Lifetime Value (LTV)?*\n"
        "- *Find customers with Churn_Probability above 0.8 and Lifetime_Value above 5000*"
    ),
    data_description="""
    Salescope customer dataset — 10,000 e-commerce customer records across four global regions.

    Columns:
    - Customer_ID: Unique customer identifier
    - Product_ID: Product identifier
    - Transaction_ID: Transaction identifier
    - Purchase_Frequency: Integer (1–19), number of purchases in the review period
    - Average_Order_Value: Float (20–200 USD), typical basket size
    - Most_Frequent_Category: Clothing, Electronics, Home, Sports
    - Time_Between_Purchases: Integer (days), gap between purchases — a proxy for engagement
    - Region: Asia, Europe, North America, South America
    - Churn_Probability: Float (0–1), modeled churn risk score
    - Lifetime_Value: Float (100–10000 USD), predicted total customer revenue
    - Launch_Date: Date (YYYY-MM-DD), customer acquisition date
    - Peak_Sales_Date: Date (YYYY-MM-DD), date of highest purchase activity
    - Season: Spring, Summer, Fall, Winter
    - Preferred_Purchase_Times: Morning, Afternoon, Evening
    - Retention_Strategy: Discount, Email Campaign, Loyalty Program
    - Value_At_Risk: Derived column — Lifetime_Value × Churn_Probability (revenue at risk)
    """,
    extra_instructions=SALESCOPE_EXTRA_INSTRUCTIONS,
    client=ChatAnthropic(model="claude-sonnet-4-0", api_key=API_KEY),
)

kpi_component = ui.TagList(
    ui.layout_columns(
        ui.value_box(
            ui.tags.span(
                "Average Lifetime Value (Filtered Base)",
                style="font-size:1.0em; font-weight:600;"
            ),
            ui.output_ui("kpi_lifetime")
        ),
        ui.value_box(
            ui.tags.span(
                "Average Value-At-Risk (Filtered Base)",
                style="font-size:1.0em; font-weight:600;"
            ),
            ui.output_ui("kpi_risk")
        ),
        ui.value_box(
            ui.tags.span(
                "Average Churn (Filtered Base)",
                style="font-size:1.0em; font-weight:600;"
            ),
            ui.output_ui("kpi_churn")
        ),
        ui.value_box(
            ui.tags.span(
                "Average Days Between Purchase (Filtered Base)",
                style="font-size:1.0em; font-weight:600;"
            ),
            ui.output_ui("kpi_days")
        ),
        col_widths=(3, 3, 3, 3),
        fill=False,
    ),
    ui.HTML(
        "<div style='font-size: 0.9em;'>⚠️ <strong>Note:</strong> All KPIs (Key Performance Indicators) and charts on this page reflect <strong>current</strong> filter settings, defaulting to the most recent quarter.</div>"
    ),
    ui.output_ui("kpi_note"),
)

    
main_sidebar = ui.sidebar(
    # CSS Styling, 
    ui.tags.style("""
        /* Outer container styling */
        .numeric-range-styled {
            border: 1px solid #ccc;
            border-radius: 4px;
            overflow: hidden;
            display: grid !important;
            align-items: center;
            width: fit-content;
        }
        
        /* Remove internal borders */
        .numeric-range-styled .form-control {
            border: none !important;
            box-shadow: none !important;
            text-align: center;
        }

        /* Adjust last input for the 'to' box */
        .numeric-range-styled > div:last-child {
            position: relative;
        }

        /* Create the 'to' box, position linked to last object */
        .numeric-range-styled > div:last-child::before {
            content: "to";
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #eeeeee;
            border-left: 1px solid #ccc;
            border-right: 1px solid #ccc;
            padding: 0 12px;
            height: 100%;
            color: #555;
            position: absolute;
            left: -35px;
            z-index: 1;
        }

    """),
    
    # Launch date filter
    
    ui.input_date_range(
        id="date_range", 
        label="Filter by launch date",
        start=max(default_start,min_date),
        end=min(default_end,max_date),
        min=min_date,
        max=max_date
    ),
    
    # Checkbox filters

    ui.input_checkbox(
        id="use_ai_filter",
        label=ui.tags.span("Use the ",ui.tags.code("AI Insights")," dataframe"),
        value=False,
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
    

    # Numeric Filters

    ui.markdown("Churn Rate"),
    ui.layout_column_wrap(
        ui.input_numeric(
            id="num_churn_min",
            label=None,
            value=0.0,
            min=0.0,
            max=1.0,
            step=0.01,
            width="100%"
        ),
        ui.input_numeric(
            id="num_churn_max",
            label=None,
            value=1.0,
            min=0.0,
            max=1.0,
            step=0.01,
            width="100%"
        ),
        width=1/2,
        gap="30px",
    class_="numeric-range-styled"
    ),

    ui.input_slider(
        id="slider_churn_decrease",
        label=ui.tags.span(
            "Churn rate decrease (%) ",
            ui.tags.span(
                "ⓘ",
                title="Scenario slider: simulate reducing the upper churn bound by this percentage. KPIs and plots compare this scenario against the original churn range.",
                style="cursor: help;"
            )
        ),
        min=0,
        max=100,
        value=0,
    ),
   
    ui.markdown("Customer Lifetime Value"),
    ui.layout_column_wrap(  
        ui.input_numeric(
            id="num_clv_min",
            label=None,
            value=100, 
            min=100, 
            max=10000, 
            step=50
        ),
        ui.input_numeric(
            id="num_clv_max",
            label=None,
            value=10000, 
            min=100, 
            max=10000, 
            step=50
        ),  
        width=1/2,
        gap="30px",
    class_="numeric-range-styled"
    ),

    ui.markdown("Average Order Value"),
    ui.layout_column_wrap(
        ui.input_numeric(
            id="num_order_min",
            label=None,
            value=20, 
            min=20, 
            max=200, 
            step=5
        ),
        ui.input_numeric(
            id="num_order_max",
            label=None,
            value=200, 
            min=20, 
            max=200, 
            step=5
        ),
        width=1/2,
        gap="30px",
    class_="numeric-range-styled"
    ),    

    ui.markdown("Purchase Frequency"),
    ui.layout_column_wrap(
        ui.input_numeric(
            id="num_freq_min",
            label=None,
            value=1, 
            min=1, 
            max=19, 
            step=1
        ),
        ui.input_numeric(
            id="num_freq_max",
            label=None,
            value=19, 
            min=1, 
            max=19, 
            step=1
        ),
        width=1/2,
        gap="30px",
    class_="numeric-range-styled"
    ),
    
    
    
    ui.input_action_button("reset", "Reset filters", class_="salescope-primary-btn"),
    open="desktop",
)


# Specialized table for User Story 1
panel_1 = ui.nav_panel("Key Metric Tables", 
    ui.layout_columns(
        ui.input_select(
            id="row_dropdown",
            label="Table partition options:",
            choices=["Total", "Region", "Retention Strategy", "Most Frequent Value"]
        ),
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
    ui.layout_columns(
        ui.card(
            output_widget("quarter_bubbles"),
            full_screen=True,
        )
    )
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
                "mean": "Average customer value", 
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

# Specialized plot for trends over time

panel_4 = ui.nav_panel(
    
    "Trends Over Time",
    ui.layout_columns(
        ui.card(
            ui.card_header("Trend settings"),
            ui.input_radio_buttons(
                "time_metric",
                "Select metric:",
                {
                    "Lifetime_Value": "Customer Lifetime Value",
                    "Churn_Probability": "Churn Risk",
                    "Value_At_Risk": "Value at Risk",                    
                    "Average_Order_Value": "Average Order Value",
                    "Purchase_Frequency": "Purchase Frequency",
                    "Time_Between_Purchases": "Days Between Purchases",
                },
                selected="Lifetime_Value",
            ),
            ui.help_text("This plot uses dashboard filters or AI filtered data when AI checkbox is enabled."),
        ),
        ui.card(
            ui.card_header("Metric Trend Over Time"),

            output_widget("trend_over_time"),

            full_screen=True,
        ),

        col_widths=[3, 9],
    ),
)

#panel for AI insights
panel_ai = ui.nav_panel(
    "AI Insights",
    ui.div(
        ui.tags.style("""
            .ai-chat-scroll-fix .bslib-sidebar-layout > .sidebar {
                max-height: 80vh;
                overflow-y: auto;
                overflow-x: hidden;
            }
            .ai-chat-scroll-fix .bslib-sidebar-layout {
                align-items: flex-start !important;
            }
        """),
        ui.layout_sidebar(
            # AI chat interface
            qc.sidebar(open = "always"),
            # AI scope control — affects LLM behavior via on_tool_request
            ui.card(
                ui.card_header("AI Analysis Settings"),
                ui.input_select(
                    id="ai_scope_mode",
                    label="Analysis Scope",
                    choices={
                        "full": "Full Analysis (no restrictions)",
                        "churn_only": "Churn Focus Only",
                        "revenue_only": "Revenue & Lifetime Value Focus Only",
                    },
                    selected="full",
                ),
                ui.output_ui("scope_mode_info"),
                style="margin-bottom: 8px;",
            ),
            ui.download_button("download_ai_filtered", "⬇️ Download Filtered Dataframe", class_="salescope-primary-btn"),
            ui.layout_columns(
                ui.card(
                    ui.card_header("AI Filtered Data"),
                    ui.output_data_frame("ai_data_table"),
                    ui.help_text("This table updates when you ask the AI to filter customers (e.g., 'show customers where...'). Pure summary questions may leave the table at the full dataset.")
                ),
                ui.card(
                    output_widget("ai_tab_scatter"),
                    full_screen=True
                ),
                ui.card(
                    output_widget("ai_tab_heatmap"),
                    full_screen=True
                ),
                col_widths=(12, 12, 12)
            )
        ),
        class_="ai-chat-scroll-fix"
    )
)

# UI
app_ui = ui.page_navbar(
    ui.nav_panel(
        "Advanced Figures",
        ui.layout_sidebar(
            main_sidebar, 
            ui.TagList(
                ui.output_ui("conditional_kpis"),
                ui.navset_card_tab(
                    panel_2,
                    panel_1,
                    panel_3, 
                    panel_4,
                    id="advanced_nav"
                )
            ) 
        )
    ),
    panel_ai, 
    title=ui.TagList(
        ui.img(
            src="salescope_logo_icon.png",
            height="28px",
            style="margin-right: 8px; border-radius: 4px;",
        ),
        "Salescope — Customer Retention & Churn Insights",
    ),
    header=ui.TagList(
        ui.tags.style(
            """
            .salescope-primary-btn {
                background-color: #007bc2;
                border-color: #007bc2;
            }
            .salescope-primary-btn:hover {
                background-color: #005c8e;
                border-color: #005c8e;
            }
            .salescope-accent-card > .card-header {
                border-left: 4px solid #FF9F1C;
            }
            """
        ),
        ui.markdown("#### Data-driven customer retention and churn analysis."),
        ui.markdown(
            "**Suggested analysis flow:** Start on the *Churn Risk Plot* tab to spot high-risk segments, "
            "then use *KPI Tables* and the *Seasonal Product Heatmap* to drill into details."
        )
    ),
    id="top_navbar",
    theme=ui.Theme("lumen")
)    

def create_summary_table(df, grouping, feature):
    total_row = pd.DataFrame({
        "Group": ["Total"],
        "Count": [df[feature].size],
        "Mean": [df[feature].mean()],
        "Median": [df[feature].median()],
        "Maximum": [df[feature].max()],
        "Total": [df[feature].sum()]
    }).round(2)

    if grouping == "Total":
        return total_row

    summary = (
        df.groupby(grouping)
        .agg(
            Count=(feature, "size"),
            Mean=(feature, "mean"),
            Median=(feature, "median"),
            Maximum=(feature, "max"),
            Total=(feature, "sum"),
        )
        .round(2)
        .reset_index()
    )

    summary = summary.rename(columns={grouping: "Group"})
    summary = pd.concat([summary, total_row], ignore_index=True)

    return summary

# Server
def server(input, output, session):

    qc_vals = qc.server()

    # Mutable holder for scope — updated by reactive effect below so the
    # on_tool_request callback (which runs outside reactive context) can read it.
    _scope = {"value": "full"}

    @reactive.effect
    def _sync_scope():
        _scope["value"] = input.ai_scope_mode()

    def _handle_tool_request(request):
        # log the call so we can see what sql the model is generating
        args = request.arguments if isinstance(request.arguments, dict) else {}
        sql = args.get("query", "")
        print(f"[querychat] tool={request.name} scope={_scope['value']} sql={sql[:80]!r}")

        # block queries outside the selected scope
        scope = _scope["value"]
        if scope == "churn_only" and sql:
            if not any(t in sql.lower() for t in ("churn", "churn_probability", "retention_strategy")):
                raise ToolRejectError(
                    "Churn Focus Only mode is on. Please ask about churn, "
                    "retention strategies, or at-risk customers."
                )
        elif scope == "revenue_only" and sql:
            if not any(t in sql.lower() for t in ("lifetime_value", "average_order_value", "value_at_risk")):
                raise ToolRejectError(
                    "Revenue Focus Only mode is on. Please ask about "
                    "Lifetime_Value, Average_Order_Value, or Value_At_Risk."
                )

    qc_vals.client.on_tool_request(_handle_tool_request)

    @render.ui
    def scope_mode_info():
        scope = input.ai_scope_mode()
        msgs = {
            "full": ("All questions allowed", "green"),
            "churn_only": ("Churn & retention questions only", "darkorange"),
            "revenue_only": ("Revenue & Lifetime Value questions only", "steelblue"),
        }
        msg, color = msgs[scope]
        return ui.HTML(f'<small style="color:{color};">{msg}</small>')

    @reactive.calc
    def ai_filtered_df():
        return qc_vals.df()

    @reactive.calc
    def dashboard_df():
        if input.use_ai_filter():
            return ai_filtered_df()
        return filtered_df()

    @render.data_frame
    def ai_data_table():
        return ai_filtered_df()
    
    @render.download(filename="sales_and_customer_insights_ai_filtered.csv")
    def download_ai_filtered():
        yield ai_filtered_df().to_csv(index=False)

    @render_widget
    def ai_tab_scatter():
        df = ai_filtered_df()
        
        if df is None or df.empty:
            return px.scatter(title="No data available for current filters")

        req_cols = ["Lifetime_Value", "Time_Between_Purchases"]
        missing_cols = [col for col in req_cols if col not in df.columns]
        if missing_cols:
            return px.scatter(title=f"Missing expected columns from AI filter: {', '.join(missing_cols)}")

        hover_cols = ["Customer_ID", "Region", "Churn_Probability", "Purchase_Frequency"]
        actual_hover = [c for c in hover_cols if c in df.columns]

        fig = px.scatter(
            df,
            x="Lifetime_Value",
            y="Time_Between_Purchases",
            color="Retention_Strategy" if "Retention_Strategy" in df.columns else None,
            size="Churn_Probability" if "Churn_Probability" in df.columns else None,
            hover_data=actual_hover,
            size_max=18
        )
        fig.update_layout(
            title="AI-filtered: Customers by Lifetime Value (LTV) and Days Between Purchases",
            xaxis_title="Customer Lifetime Value ($)",
            yaxis_title="Days Between Purchases"
        )
        return fig

    @render_widget
    def ai_tab_heatmap():
        df = ai_filtered_df()
        if df is None or df.empty:
            return px.scatter(title="No data available for current filters")
        req_cols = ["Season", "Most_Frequent_Category", "Lifetime_Value"]
        missing_cols = [c for c in req_cols if c not in df.columns]
        if missing_cols:
            return px.scatter(
                title=f"Missing expected columns from AI filter: {', '.join(missing_cols)}"
            )
        plot_data = (
            df.groupby(["Season", "Most_Frequent_Category"])["Lifetime_Value"]
            .mean()
            .reset_index()
        )
        fig = px.density_heatmap(
            plot_data,
            x="Season",
            y="Most_Frequent_Category",
            z="Lifetime_Value",
            title="AI-filtered: Average Lifetime Value (LTV) by Season vs. Category",
            labels={"Lifetime_Value": "Average Lifetime Value ($)", "Most_Frequent_Category": "Product Type"},
            color_continuous_scale="Viridis",
            text_auto=True,
        )
        return fig

    @reactive.calc
    def churn_plot_df():
        churn_min_raw = input.num_churn_min() or 0.0
        churn_max_raw = input.num_churn_max() or 1.0
        churn_min = min(churn_min_raw, churn_max_raw)
        churn_max = max(churn_min_raw, churn_max_raw)
        pct_decrease = input.slider_churn_decrease()

        clv_min_raw = input.num_clv_min() or 100
        clv_max_raw = input.num_clv_max() or 10000
        clv_min = min(clv_min_raw, clv_max_raw)
        clv_max = max(clv_min_raw, clv_max_raw)

        order_min_raw = input.num_order_min() or 20
        order_max_raw = input.num_order_max() or 200
        order_min = min(order_min_raw, order_max_raw)
        order_max = max(order_min_raw, order_max_raw)

        freq_min_raw = input.num_freq_min() or 1
        freq_max_raw = input.num_freq_max() or 19
        freq_min = min(freq_min_raw, freq_max_raw)
        freq_max = max(freq_min_raw, freq_max_raw)

        date_start, date_end = input.date_range()
        reduced_max = churn_max * (1 - pct_decrease / 100)

        df = execute_filtered_query(
            churn_min=churn_min,
            churn_max=churn_max,
            clv_min=clv_min,
            clv_max=clv_max,
            order_min=order_min,
            order_max=order_max,
            freq_min=freq_min,
            freq_max=freq_max,
            date_start=pd.Timestamp(date_start),
            date_end=pd.Timestamp(date_end),
            types=input.checkbox_group_type(),
            regions=input.checkbox_group_region(),
            strategies=input.checkbox_group_strategy(),
        )

        df["in_reduced_churn_range"] = (
            (df["Churn_Probability"] >= churn_min) &
            (df["Churn_Probability"] <= reduced_max)
        )

        return df

    @reactive.calc
    def filtered_df():
        churn_min_raw = input.num_churn_min() or 0.0
        churn_max_raw = input.num_churn_max() or 1.0
        churn_min = min(churn_min_raw, churn_max_raw)
        churn_max = max(churn_min_raw, churn_max_raw)
        pct_decrease = input.slider_churn_decrease()

        clv_min_raw = input.num_clv_min() or 100
        clv_max_raw = input.num_clv_max() or 10000
        clv_min = min(clv_min_raw, clv_max_raw)
        clv_max = max(clv_min_raw, clv_max_raw)

        order_min_raw = input.num_order_min() or 20
        order_max_raw = input.num_order_max() or 200
        order_min = min(order_min_raw, order_max_raw)
        order_max = max(order_min_raw, order_max_raw)

        freq_min_raw = input.num_freq_min() or 1
        freq_max_raw = input.num_freq_max() or 19
        freq_min = min(freq_min_raw, freq_max_raw)
        freq_max = max(freq_min_raw, freq_max_raw)

        date_start, date_end = input.date_range()

        reduced_max = churn_max * (1 - pct_decrease / 100)
        effective_churn_max = reduced_max if pct_decrease > 0 else churn_max

        df = execute_filtered_query(
            churn_min=churn_min,
            churn_max=effective_churn_max,
            clv_min=clv_min,
            clv_max=clv_max,
            order_min=order_min,
            order_max=order_max,
            freq_min=freq_min,
            freq_max=freq_max,
            date_start=pd.Timestamp(date_start),
            date_end=pd.Timestamp(date_end),
            types=input.checkbox_group_type(),
            regions=input.checkbox_group_region(),
            strategies=input.checkbox_group_strategy(),
        )

        df["in_reduced_churn_range"] = (
            (df["Churn_Probability"] >= churn_min) &
            (df["Churn_Probability"] <= reduced_max)
        )

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
        ui.update_numeric(
            id="num_clv_min",
            value=100,
            session=session
        )
        ui.update_numeric(
            id="num_clv_max",
            value=10000,
            session=session
        )
        ui.update_numeric(
            id="num_order_min",
            value=20,
            session=session
        )
        ui.update_numeric(
            id="num_order_max",
            value=200,
            session=session
        )
        ui.update_numeric(
            id="num_freq_min",
            value=1,
            session=session
        )
        ui.update_numeric(
            id="num_freq_max",
            value=19,
            session=session
        )
        ui.update_date_range(
            "date_range",
            start=max(default_start,min_date),
            end=min(default_end,max_date),
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

        ui.update_checkbox(
            id="use_ai_filter",
            value=False,
            session=session
        )

    @render.ui
    def kpi_lifetime():
        df = filtered_df()
        pct_decrease = input.slider_churn_decrease()

        if df.empty:
            return "—"

        val = df["Lifetime_Value"].mean()
        val_str = f"${val:,.2f}"

        if pct_decrease > 0:
            df_base = churn_plot_df()
            if not df_base.empty:
                base_val = df_base["Lifetime_Value"].mean()
                delta = val - base_val
                pct_change = 0 if base_val == 0 else delta / base_val
                direction = "increase" if delta > 0 else "decrease" if delta < 0 else "change"
                color = "green" if delta > 0 else "red" if delta < 0 else "inherit"
                subtext = f"{abs(pct_change):.1%} {direction} vs no churn reduction"

                return ui.HTML(
                    f"<div>{val_str}</div>"
                    f"<div style='font-size: 0.6em; opacity: 0.8; color: {color};'>{subtext}</div>"
                )

        return val_str
    
    @render.ui
    def kpi_churn():
        df = filtered_df()
        pct_decrease = input.slider_churn_decrease()

        if df.empty:
            return "—"

        val = df["Churn_Probability"].mean()
        val_str = f"{val:.1%}"

        if pct_decrease > 0:
            df_base = churn_plot_df()
            if not df_base.empty:
                base_val = df_base["Churn_Probability"].mean()
                delta = val - base_val
                direction = "increase" if delta > 0 else "decrease" if delta < 0 else "change"
                color = "red" if delta > 0 else "green" if delta < 0 else "inherit"
                subtext = f"{abs(delta):.1%} {direction} vs no churn reduction"

                return ui.HTML(
                    f"<div>{val_str}</div>"
                    f"<div style='font-size: 0.6em; opacity: 0.8; color: {color};'>{subtext}</div>"
                )

        return val_str

    @render.ui
    def kpi_risk():
        df = filtered_df()
        pct_decrease = input.slider_churn_decrease()

        if df.empty:
            return "—"

        val = df["Value_At_Risk"].mean()
        val_str = f"${val:,.2f}"

        if pct_decrease > 0:
            df_base = churn_plot_df()
            if not df_base.empty:
                base_val = df_base["Value_At_Risk"].mean()
                delta = val - base_val
                pct_change = 0 if base_val == 0 else delta / base_val
                direction = "increase" if delta > 0 else "decrease" if delta < 0 else "change"
                color = "red" if delta > 0 else "green" if delta < 0 else "inherit"
                subtext = f"{abs(pct_change):.1%} {direction} vs no churn reduction"

                return ui.HTML(
                    f"<div>{val_str}</div>"
                    f"<div style='font-size: 0.6em; opacity: 0.8; color: {color};'>{subtext}</div>"
                )

        return val_str

    @render.ui
    def kpi_days():
        df = filtered_df()
        pct_decrease = input.slider_churn_decrease()

        if df.empty:
            return "—"

        val = df["Time_Between_Purchases"].mean()
        val_str = f"{val:,.2f} days"

        if pct_decrease > 0:
            df_base = churn_plot_df()
            if not df_base.empty:
                base_val = df_base["Time_Between_Purchases"].mean()
                delta = val - base_val
                pct_change = 0 if base_val == 0 else delta / base_val
                direction = "increase" if delta > 0 else "decrease" if delta < 0 else "change"
                color = "red" if delta > 0 else "green" if delta < 0 else "inherit"
                subtext = f"{abs(pct_change):.1%} {direction} vs no churn reduction"

                return ui.HTML(
                    f"<div>{val_str}</div>"
                    f"<div style='font-size: 0.6em; opacity: 0.8; color: {color};'>{subtext}</div>"
                )

        return val_str
    
    @render.ui
    def kpi_note():
        df = dashboard_df()
        count = len(df)

        if count < 50:
            return ui.HTML(
                f"<small style='color:#b45309;'>⚠️ Low sample size: current filters leave only {count} datapoints.</small>"
            )

        return None

    @render.ui
    def decision_cues():
        df = filtered_df()
        if df.empty:
            return ui.markdown("No data available to generate insights.")
        
        cues = []
        
        # Cue 1: Region with highest churn
        if "Region" in df.columns and "Churn_Probability" in df.columns:
            region_churn = df.groupby("Region")["Churn_Probability"].mean()
            if not region_churn.empty:
                high_risk = region_churn.idxmax()
                val = region_churn.max()
                if val > 0.4:
                    cues.append(f"**Focus on {high_risk}**: This region has the highest average churn risk ({val:.1%}). Consider localized retention campaigns.")
                else:
                    cues.append(f"**Stable Regions**: Across all regions, churn remains manageable (highest: {high_risk} at {val:.1%}).")

        # Cue 2: Retention strategy with highest Lifetime Value
        if "Retention_Strategy" in df.columns and "Lifetime_Value" in df.columns:
            strat_ltv = df.groupby("Retention_Strategy")["Lifetime_Value"].mean()
            if not strat_ltv.empty:
                best_strat = strat_ltv.idxmax()
                cues.append(f"**Scale {best_strat}**: This retention strategy is currently driving the highest Average Lifetime Value (${strat_ltv.max():,.0f}).")
            
        if not cues:
            return ui.markdown("Data distribution appears stable. No immediate critical interventions flagged.")
            
        markup = "".join([f"- {cue}\n" for cue in cues])
        return ui.markdown(markup)
    
    @render.ui
    def conditional_kpis():
        if input.top_navbar() == "AI Insights":
            return None

        return ui.TagList(
            kpi_component,
            ui.card(
                ui.card_header(
                    "💡 Actionable Insights & Next Steps",
                    style="font-weight: bold; font-size: 1.1em; background-color: #f8f9fa; padding: 0.5rem 1rem;"
                ),
                ui.output_ui("decision_cues"),
                class_="salescope-accent-card",
                style="margin-bottom: 20px; border-left: 4px solid #FF9F1C;"
            )
        )

    @render.data_frame
    def customer_df():
        mapping = {
            "Total": "Total",
            "Region": "Region",
            "Retention Strategy": "Retention_Strategy",
            "Most Frequent Value": "Most_Frequent_Category"
        }
        group = mapping[input.row_dropdown()]
        return create_summary_table(dashboard_df(), group, "Lifetime_Value")

    @render.data_frame
    def risk_df():
        mapping = {
            "Total": "Total",
            "Region": "Region",
            "Retention Strategy": "Retention_Strategy",
            "Most Frequent Value": "Most_Frequent_Category"
        }
        group = mapping[input.row_dropdown()]
        return create_summary_table(dashboard_df(), group, "Value_At_Risk")

    @render.data_frame
    def order_df():
        mapping = {
            "Total": "Total",
            "Region": "Region",
            "Retention Strategy": "Retention_Strategy",
            "Most Frequent Value": "Most_Frequent_Category"
        }
        group = mapping[input.row_dropdown()]
        return create_summary_table(dashboard_df(), group, "Average_Order_Value")

    @render.data_frame
    def frequency_df():
        mapping = {
            "Total": "Total",
            "Region": "Region",
            "Retention Strategy": "Retention_Strategy",
            "Most Frequent Value": "Most_Frequent_Category"
        }
        group = mapping[input.row_dropdown()]
        return create_summary_table(dashboard_df(), group, "Purchase_Frequency")
    
    @render_widget
    def high_churn_risk():
        pct_decrease = input.slider_churn_decrease()
        df = filtered_df()
        if input.use_ai_filter(): 
            df = ai_filtered_df()
        elif pct_decrease > 0: 
            df = churn_plot_df()
        
        churn_min_raw = input.num_churn_min()
        churn_max_raw = input.num_churn_max()
        churn_min = min(churn_min_raw, churn_max_raw)
        churn_max = max(churn_min_raw, churn_max_raw)
        reduced_max = churn_max * (1 - pct_decrease / 100)

        if df.empty:
            fig = px.scatter(title="No data available for current filters")
            return fig

        if pct_decrease > 0 and not input.use_ai_filter():
            df["status"] = df["in_reduced_churn_range"].map({True: "In Range", False: "Excluded"})
            color_col = "status"
            legend_title = "Within Reduced Range"
        else:
            color_col = "Retention_Strategy"
            legend_title = "Retention Strategy"


        fig = px.scatter(
            df,
            x="Lifetime_Value",
            y="Time_Between_Purchases",
            color=color_col,
            size="Churn_Probability",
            size_max=18,
            hover_data=["Customer_ID", "Region", "Churn_Probability", "Purchase_Frequency"],
        )
        fig.update_layout(
            title=f"Customers by Lifetime Value and Days Between Purchases, Churn Risk From {churn_min:0.2f} to {reduced_max:0.2f}",
            xaxis_title="Customer Lifetime Value ($)",
            yaxis_title="Days Between Purchases",
            legend_title=legend_title,
        )
        return fig
    
    @render_widget
    def quartile_churn_risk():
        df = filtered_df()
        if input.use_ai_filter(): 
            df = ai_filtered_df()
        
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
    def quarter_bubbles():
        df = filtered_df()
        if input.use_ai_filter(): 
            df = ai_filtered_df()
            
        if df.empty:
            return px.scatter(title="No data available for current filters")

        df_plot = df.copy()
        df_plot['Quarter'] = 'Q' + df_plot['Launch_Date'].dt.quarter.astype(str)
        
        agg_df = df_plot.groupby(['Quarter', 'Retention_Strategy']).agg(
            Avg_LTV=('Lifetime_Value', 'mean'),
            Count=('Customer_ID', 'size'),
            Avg_Churn=('Churn_Probability', 'mean')
        ).reset_index()
        
        # Sort quarters Q1 to Q4
        agg_df = agg_df.sort_values(by="Quarter")

        fig = px.scatter(
            agg_df,
            x="Quarter",
            y="Retention_Strategy",
            size="Avg_LTV",
            color="Avg_Churn",
            hover_data=["Count"],
            size_max=35,
            color_continuous_scale="RdYlGn_r"
        )
        fig.update_layout(
            title="Q1–Q4 Trend: Retention Strategy by Average Lifetime Value (Size) & Churn Risk (Color)",
            xaxis_title="Quarter",
            yaxis_title="Retention Strategy",
            coloraxis_colorbar=dict(title="Average Churn Probability")
        )
        return fig
    
    @render_widget
    def heatmap():
        df = dashboard_df()
        
        if df.empty:
            fig = px.density_heatmap(title="No data available for current filters")
            return fig
            
        # fetching value from  radio buttons
        metric = input.heatmap_metric()

        if metric == "count":
            plot_data = (
                df.groupby(["Season", "Most_Frequent_Category"])
                .size().reset_index(name="Frequency") )
            z_col = "Frequency"
            title_text = "Sales Frequency: Season vs. Category"
            label_text = "Total Sales Count"
        else:
            plot_data = (
                df.groupby(["Season", "Most_Frequent_Category"])["Lifetime_Value"]
                .mean()
                .reset_index()  )
            z_col = "Lifetime_Value"
            title_text = "Average Value: Season vs. Category"
            label_text = "Average Lifetime Value ($)"

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

    @render_widget
    def trend_over_time():
        df = dashboard_df()

        if df.empty:
            return px.scatter(title="No data available for current filters")

        metric = input.time_metric()

        metric_labels = {
            "Lifetime_Value": "Customer Lifetime Value ($)",
            "Churn_Probability": "Churn Risk",
            "Value_At_Risk": "Value at Risk ($)",
            "Average_Order_Value": "Average Order Value ($)",
            "Purchase_Frequency": "Purchase Frequency",
            "Time_Between_Purchases": "Days Between Purchases",
        }

        if metric not in df.columns:
            return px.scatter(
                title=f"Selected metric '{metric}' is not available in the current dataframe"
            )

        df_plot = df.copy()
        #df_plot["Launch_Date"] = pd.to_datetime(df_plot["Launch_Date"])

        trend_df = (
            df_plot.groupby("Launch_Date", as_index=False)[metric]
            .mean()
            .sort_values("Launch_Date")
        )

        trend_df["smooth"] = trend_df[metric].rolling(window=7, min_periods=1).mean()

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=np.array(trend_df["Launch_Date"].dt.to_pydatetime()),
                y=trend_df[metric],
                mode="markers",
                name="Daily average",
                marker=dict(size=6),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=np.array(trend_df["Launch_Date"].dt.to_pydatetime()),
                y=trend_df["smooth"],
                mode="lines",
                name="7-day rolling mean",
            )
        )

        fig.update_layout(
            title=f"{metric_labels.get(metric, metric)} Over Time",
            xaxis_title="Date",
            yaxis_title=metric_labels.get(metric, metric),
            hovermode="x unified",
        )

        fig.update_xaxes(type="date")

        return fig
    
    @render.text
    def kpi_count():
        df = dashboard_df()
        count = len(df)
        if count < 50:
            return f"{count:,} ⚠️ Low sample"
        return f"{count:,}"


# Create app
www_dir = Path(__file__).parent.parent / "www"
app = App(app_ui, server, static_assets=www_dir)