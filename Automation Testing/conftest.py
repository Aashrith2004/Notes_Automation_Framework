"""
conftest.py
"""

from pathlib import Path
import os
import allure
import pytest
from config.environment import config as framework_config

from fixtures.browser_fixture import (
    create_driver,
    quit_driver,
)



def pytest_configure(config):
    """
    Initializes Allure reporting directories.
    """

    allure_results = Path(
        framework_config.reporting.allure_results_dir
    )

    allure_results.mkdir(
        parents=True,
        exist_ok=True,
    )


@pytest.fixture(scope="function")
def driver():

    drv = create_driver()

    yield drv

    quit_driver(drv)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item,
    call,
):

    outcome = yield

    report = outcome.get_result()

    # Only capture on test failure
    if (
        report.when == "call"
        and report.failed
    ):

        driver = item.funcargs.get("driver")

        if driver:

            screenshots_dir = (
                "reports/screenshots"
            )

            os.makedirs(
                screenshots_dir,
                exist_ok=True
            )

            screenshot_path = (
                f"{screenshots_dir}/"
                f"{item.name}.png"
            )

            # Save screenshot
            driver.save_screenshot(
                screenshot_path
            )

            # Attach to Allure
            allure.attach.file(
                screenshot_path,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )