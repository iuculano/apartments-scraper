import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def _strip_numerical_formatting(number: str) -> int:
    """
    Helper to strip a formatted currency string.
    """
    return re.sub('[\$, ]', '', number.strip())

def _create_selenium_webdriver(additional_args: list[str] = []) -> webdriver.Chrome:
    """
    Creates a Selenium web driver.

    Currently hardcoded to Chrome. This is provided by the dev container and
    there should (probably) be little reason to need to change this.

    Returns a Selenium web driver if successful.
    """

    options = Options()

    # You must set a user agent, otherwise you're likely to be blocked
    # Use something like a typical browser would produce and you'll be fine
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')

    # Headless Chrome seems relatively crash happy without these arguments
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    for arg in additional_args:
        options.add_argument(arg)

    return webdriver.Chrome(options=options)

def _get_parseable_page_source(url: str, driver: webdriver.Chrome) -> str:
    """
    Get the source of the page using Selenium.

    Selenium is required here, the content is dynamic and you cannot simply
    make a GET request.

    Returns the Selenium rendered page source.
    """

    driver.get(url)

    # Try to handle simple failures where the page doesn't load by retrying
    # a few times - these seem to be some kind of rate limiting/protection?
    i = 1
    while driver.title == '' and i < 5:            
        print('Failed to get page (possibly rate limited) - retrying - {i} of 5...')
        driver.refresh()
        i += 1

    return driver.page_source
