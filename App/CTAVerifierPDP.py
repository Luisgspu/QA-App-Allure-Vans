import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CTAVerifier:
    def __init__(self, driver):
        """Initialize the CTAVerifier with a Selenium WebDriver instance."""
        self.driver = driver

    def handle_cookies(self):
        """Handles the cookie banner if present."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "cmm-cookie-banner"))
            )
            logging.info("✅ Cookie banner detected.")
            self.driver.execute_script("""
                document.querySelector("cmm-cookie-banner").shadowRoot.querySelector("wb7-button.button--accept-all").click();
            """)
            logging.info("✅ Clicked on the cookie acceptance button.")
        except Exception as ex:
            logging.warning(f"⚠️ Could not click cookie banner: {ex}")

    def verify_ctas(self, parent_selector, primary_cta_selector, expected_href_value):
        """
        Verifies the primary and secondary CTAs on the page.

        Returns:
            bool: True if both CTAs contain the expected hrefs, False otherwise.
        """
        try:
            # Locate the parent element
            parent_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.root.responsivegrid.owc-content-container > div > div.responsivegrid.ng-content-root.aem-GridColumn.aem-GridColumn--default--12 > div > div:nth-child(8) > div > div > div > div > div:nth-child(1) > article > div > div.hp-campaigns__content'))
            )
            logging.info("✅ Parent element located.")

            primary_verified = False

            # Verify the primary CTA
            try:
                primary_cta_selector = parent_element.find_element(By.CSS_SELECTOR, 'body > div.root.responsivegrid.owc-content-container > div > div.responsivegrid.ng-content-root.aem-GridColumn.aem-GridColumn--default--12 > div > div:nth-child(8) > div > div > div > div > div:nth-child(1) > article > div > div.hp-campaigns__content > div > a')
                logging.info("✅ Primary CTA located.")
                if primary_cta_selector.is_displayed():
                    logging.info("✅ Primary CTA is visible.")
                    primary_href = primary_cta_selector.get_attribute("href")
                    logging.info(f"Primary CTA href: {primary_href}")

                    # Verify if the href includes "/buy/new-car/search-results.html/"
                    href_value = primary_cta_selector.get_attribute("href")
                    if "/buy/new-car/product.html/" in expected_href_value:
                        logging.info(f"✅ The href attribute includes '/buy/new-car/product.html/': {expected_href_value}")
                    else:
                        logging.warning(f"⚠️ The href attribute does not include '/buy/new-car/product.html/': {expected_href_value}")
                else:
                    logging.warning("⚠️ Primary CTA is not visible.")
            except Exception as e:
                logging.error(f"❌ Primary CTA not found. Error: {e}")

           
            # Return True if both CTAs are verified
            return primary_verified

        except Exception as e:
            logging.error(f"❌ Parent element not found: {parent_selector}. Error: {e}")
        return False