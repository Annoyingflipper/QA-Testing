"""
DANAConnect Framework Tests — Selenium Configuration (conftest.py)
==================================================================
This file is automatically loaded by pytest before running any tests.
It provides shared fixtures for Selenium-based tests.

Key differences from Playwright:
- Selenium uses WebDriver to control browsers (older, more established)
- Selenium 4.6+ ships with built-in Selenium Manager, which automatically
  downloads the correct ChromeDriver — no third-party tool required.
- Selenium requires explicit waits (WebDriverWait) — it doesn't auto-wait
- Selenium uses find_element() instead of Playwright's locator system
"""

import os                          # For reading environment variables
import allure                      # Allure adapter — emits the per-test result JSON
import pytest                      # The test framework
from dotenv import load_dotenv     # Reads .env file into environment variables
from selenium import webdriver     # Selenium browser automation
from selenium.webdriver.chrome.service import Service  # Explicit chromedriver path

# ── Load environment variables from .env file ──────────────────────────
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))


@pytest.fixture(autouse=True)
def _allure_parent_suite():
    """
    Tag every test in this folder as belonging to the "Selenium"
    parent suite in the Allure report.

    See the matching fixture in the Playwright conftest for the
    full rationale. Short version: Allure merges suites by name
    across result dirs, so without a parent_suite label both
    framework folders collapse into one "tests" group and you
    can't tell who wrote each test in the Suites tab.

    Setting `parent_suite="Selenium"` puts every test in this
    folder under a top-level "Selenium" group, giving the
    side-by-side framework comparison the project is built for.
    """
    allure.dynamic.parent_suite("Selenium")


@pytest.fixture(scope="session")
def base_url():
    """
    Returns the base URL for the application under test.

    scope="session" = created once, shared across all tests.
    """
    return os.getenv('BASE_URL', 'https://portal.danaconnect.com/')


@pytest.fixture(scope="session")
def credentials():
    """
    Returns a dictionary with all login credentials from .env.

    scope="session" because credentials don't change between tests.
    """
    return {
        'company': os.getenv('COMPANY', ''),
        'username': os.getenv('USERNAME', ''),
        'password': os.getenv('PASSWORD', ''),
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attach the test result to the request node so the ``driver``
    fixture can check whether the test failed during ``call``
    and save a screenshot + the page source before quitting the
    browser. Without this hook, we would have no debugging
    evidence when a test fails.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def driver(base_url, request):
    """
    Creates a fresh Chrome WebDriver instance for each test.

    scope="function" means EACH test gets its own browser.
    This ensures complete isolation — no shared cookies or state.

    How Selenium's driver setup works:
    1. Selenium Manager (built into Selenium 4.6+) detects the
       installed Chrome version and downloads the matching ChromeDriver
       automatically on first use. No service= argument needed.
    2. webdriver.Chrome() launches Chrome with that driver.
    3. implicitly_wait(10) tells Selenium to wait up to 10 seconds
       when looking for elements before throwing an error.
    4. maximize_window() makes the browser full-screen.
    5. get() navigates to the application URL.

    After the test:
    6. driver.quit() closes the browser and cleans up.
    """
    # ── Read HEADLESS env var ──
    # Default is True so CI / Docker containers work without extra
    # setup. Run locally with HEADLESS=false to see the browser
    # window while interactively debugging a test.
    headless = os.getenv('HEADLESS', 'true').lower() != 'false'

    # ── Set up Chrome options ──
    options = webdriver.ChromeOptions()
    if headless:
        # --headless=new is Chrome's modern headless mode (v109+).
        # Old --headless still works but lacks newer features and
        # has known rendering differences from real Chrome.
        options.add_argument('--headless=new')
        # In Docker the default Chrome sandbox conflicts with the
        # container's user namespace and Chrome fails to start.
        # Disabling it is safe in a CI container; never do this
        # in a user-facing browser.
        options.add_argument('--no-sandbox')
        # /dev/shm inside Docker defaults to 64 MB. Chrome's tabs
        # exceed that quickly and crash with "session deleted". Force
        # shared memory into /tmp instead, which has more room.
        options.add_argument('--disable-dev-shm-usage')
        # Headless mode has no window manager, so explicitly pick
        # a viewport. DANAConnect's Vaadin UI is responsive and
        # behaves differently below ~1024px wide.
        options.add_argument('--window-size=1920,1080')

    # Some Linux distros (including Debian, which our Jenkins image
    # is built on) install Chromium as `chromium` rather than the
    # `google-chrome` binary that Selenium looks for by default.
    # CHROME_BINARY overrides this; otherwise we auto-detect the
    # standard apt-installed path.
    chrome_binary = os.getenv('CHROME_BINARY') or (
        '/usr/bin/chromium' if os.path.exists('/usr/bin/chromium') else None
    )
    if chrome_binary:
        options.binary_location = chrome_binary

    # ── Create the WebDriver ──
    # Why we sometimes bypass Selenium Manager:
    #
    # Selenium 4.6+ ships with Selenium Manager, which auto-downloads
    # a chromedriver binary matching the installed Chrome. Convenient,
    # but there are no `linux/aarch64` binaries published — so on
    # Apple-Silicon-based Docker images it fails with
    # "Unsupported platform/architecture combination: linux/aarch64".
    #
    # Our Jenkins image ships chromedriver via apt at
    # /usr/bin/chromedriver (the aarch64 build provided by Debian).
    # If CHROMEDRIVER_PATH is set OR that path exists, use it via
    # an explicit Service object. Otherwise (e.g. running locally
    # on a Mac), fall back to Selenium Manager.
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH') or (
        '/usr/bin/chromedriver' if os.path.exists('/usr/bin/chromedriver') else None
    )
    if chromedriver_path:
        driver = webdriver.Chrome(
            service=Service(chromedriver_path),
            options=options,
        )
    else:
        # Local dev path: Selenium Manager downloads + caches the
        # correct chromedriver for the host architecture.
        driver = webdriver.Chrome(options=options)

    # ── Configure the driver ──
    # implicit wait: if an element isn't found immediately, Selenium
    # will keep trying for up to 10 seconds before failing
    driver.implicitly_wait(10)

    # In headless mode there's no real window to maximise — we've
    # already pinned a sensible viewport via --window-size. Only
    # maximise when we're actually showing a window (HEADLESS=false).
    if not headless:
        driver.maximize_window()

    # Navigate to the application's base URL
    driver.get(base_url)

    # Give this driver to the test function
    yield driver

    # ── On failure: capture screenshot and page source BEFORE quit ──
    # The ``pytest_runtest_makereport`` hook above attaches ``rep_call``
    # to the request node with the test's pass/fail status. If the
    # test failed, save artefacts into a ``screenshots/`` folder next
    # to this conftest so we can see what the browser looked like.
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call is not None and rep_call.failed:
        artefacts_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(artefacts_dir, exist_ok=True)
        safe_name = request.node.name.replace("/", "_")
        try:
            driver.save_screenshot(os.path.join(artefacts_dir, f"{safe_name}.png"))
            with open(os.path.join(artefacts_dir, f"{safe_name}.html"), "w") as f:
                f.write(driver.page_source)
            with open(os.path.join(artefacts_dir, f"{safe_name}.url.txt"), "w") as f:
                f.write(driver.current_url)
        except Exception:
            # Never let artefact capture mask the real test failure.
            pass

    # ── Cleanup (runs after the test finishes) ──
    driver.quit()  # Close the browser and end the WebDriver session
