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