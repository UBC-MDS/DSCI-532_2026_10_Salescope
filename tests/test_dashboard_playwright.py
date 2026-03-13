# Note : Code is adapted from lecture 8 : test_app04_playwright.py file.

from shiny.playwright import controller
from shiny.run import ShinyAppProc
from shiny.pytest import create_app_fixture
from playwright.sync_api import Page

app = create_app_fixture("../src/app.py")


def test_initial_kpi_count(page: Page, app: ShinyAppProc) -> None:
    
    """Default dashboard shows datapoint count, ensuring the baseline state of the dashboard loads correctly."""

    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    controller.OutputText(page, "kpi_count").expect_value("7 ⚠️ Low sample", timeout = 10000)


def test_customer_table_initial_structure(page: Page, app: ShinyAppProc) -> None:
    
    """Customer Lifetime Value summary table structure, ensuring the KPI table renders correct summary statistics for the selected grouping."""

    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    controller.NavPanel(page, id = "advanced_nav", panel_value = "KPI Tables").click()

    customer_df = controller.OutputDataFrame(page, "customer_df")
    customer_df.expect_ncol(6, timeout = 10000)
    customer_df.expect_column_labels(
        ["Region", "Count", "Mean", "Median", "Maximum", "Total"]
    )
    customer_df.expect_nrow(4)


def test_customer_table_initial_cell_values(page: Page, app: ShinyAppProc) -> None:
    
    """Spot-check Asia row values, ensuring region-level aggregation is calculated correctly in the KPI tables."""

    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    controller.NavPanel(page, id = "advanced_nav", panel_value = "KPI Tables").click()

    customer_df = controller.OutputDataFrame(page, "customer_df")
    customer_df.expect_cell("Asia", row=0, col=0, timeout = 10000)
    customer_df.expect_cell("3", row=0, col=1)


def test_region_filter_asia_only(page: Page, app: ShinyAppProc) -> None:

    
    """Selecting only Asia verifies that the Region filter updates the KPI count
       and grouped table output, ensuring dashboard summaries reflect the filtered subset.
    """

    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    controller.NavPanel(page, id = "advanced_nav", panel_value = "KPI Tables").click()

    region_checkbox = controller.InputCheckboxGroup(page, "checkbox_group_region")
    region_checkbox.set(["Asia"])
    region_checkbox.expect_selected(["Asia"], timeout = 10000)

    controller.OutputText(page, "kpi_count").expect_value("3 ⚠️ Low sample")
    controller.OutputDataFrame(page, "customer_df").expect_nrow(1)


def test_purchase_type_filter_two_values(page: Page, app: ShinyAppProc) -> None:
    
    """Purchase type filter reduces datapoints, ensuring dashboard summaries reflect the selected purchase category subset."""

    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    controller.NavPanel(page, id = "advanced_nav", panel_value = "KPI Tables").click()

    purchase_checkbox = controller.InputCheckboxGroup(page, "checkbox_group_type")
    purchase_checkbox.set(["Clothing", "Electronics"])
    purchase_checkbox.expect_selected(["Clothing", "Electronics"], timeout = 10000)

    controller.OutputText(page, "kpi_count").expect_value("4 ⚠️ Low sample")


def test_retention_strategy_filter_two_values(page: Page, app: ShinyAppProc) -> None:
    
    """Retention strategy filter reduces datapoints, ensuring dashboard summaries update to reflect the selected retention strategy."""

    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    controller.NavPanel(page, id = "advanced_nav", panel_value = "KPI Tables").click()

    strategy_checkbox = controller.InputCheckboxGroup(page, "checkbox_group_strategy")
    strategy_checkbox.set(["Discount", "Email Campaign"])
    strategy_checkbox.expect_selected(["Discount", "Email Campaign"], timeout = 10000)

    controller.OutputText(page, "kpi_count").expect_value("5 ⚠️ Low sample")


def test_row_dropdown_changes_grouping(page: Page, app: ShinyAppProc) -> None:
    
    """Changing dropdown updates summary table grouping, ensuring the dashboard recalculates metrics for the selected dimension."""

    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    controller.NavPanel(page, id = "advanced_nav", panel_value = "KPI Tables").click()

    row_dropdown = controller.InputSelect(page, "row_dropdown")
    customer_df = controller.OutputDataFrame(page, "customer_df")

    row_dropdown.set("Retention Strategy")

    customer_df.expect_ncol(6, timeout = 10000)
    customer_df.expect_column_labels(
        ["Retention_Strategy", "Count", "Mean", "Median", "Maximum", "Total"]
    )
    customer_df.expect_nrow(3)


def test_reset_button_restores_defaults(page: Page, app: ShinyAppProc) -> None:
    
    """Reset button restores default filters, ensuring users can quickly return to the baseline dashboard view."""

    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    controller.NavPanel(page, id = "advanced_nav", panel_value = "KPI Tables").click()

    region_checkbox = controller.InputCheckboxGroup(page, "checkbox_group_region")
    reset_btn = controller.InputActionButton(page, "reset")
    kpi_count = controller.OutputText(page, "kpi_count")

    # changing filter

    region_checkbox.set(["Asia"])
    kpi_count.expect_value("3 ⚠️ Low sample", timeout = 10000)

    # resetting filter

    reset_btn.click()

    kpi_count.expect_value("0 ⚠️ Low sample", timeout = 10000)
    region_checkbox.expect_selected([])
