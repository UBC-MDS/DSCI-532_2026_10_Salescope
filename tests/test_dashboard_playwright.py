# Note : Code is adapted from lecture 8 : test_app04_playwright.py file.

from shiny.playwright import controller
from shiny.run import ShinyAppProc
from shiny.pytest import create_app_fixture
from playwright.sync_api import Page

app = create_app_fixture("../src/app.py")


def test_initial_kpi_count(page: Page, app: ShinyAppProc) -> None:
    
    """Default dashboard shows datapoint count."""

    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    controller.OutputText(page, "kpi_count").expect_value("7 ⚠️ Low sample")


def test_customer_table_initial_structure(page: Page, app: ShinyAppProc) -> None:
    
    """Customer Lifetime Value summary table structure."""

    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    customer_df = controller.OutputDataFrame(page, "customer_df")
    customer_df.expect_ncol(6)
    customer_df.expect_column_labels(
        ["Region", "Count", "Mean", "Median", "Maximum", "Total"]
    )
    customer_df.expect_nrow(4)
