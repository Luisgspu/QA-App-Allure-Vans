import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ConfiguratorCompleted:
    def __init__(self, driver):
        """Initializes the Configurator with a WebDriver instance."""
        self.driver = driver

    def expand_shadow_element(self, shadow_host):
        """Expands and returns the shadow root of a shadow DOM element."""
        return self.driver.execute_script("return arguments[0].shadowRoot", shadow_host)

    def perform_configurator_actions(self):
        """Performs navigation and clicks inside the car configurator menu."""
        try:
            # Step 1: Find the first shadow host
            first_shadow_host = self.driver.find_element(By.CSS_SELECTOR, "#first-component")
            logging.info("✅ First shadow host found.")

            # Step 2: Expand the first shadow root
            first_shadow_root = self.expand_shadow_element(first_shadow_host)
            logging.info("✅ First shadow root expanded.")

            # Step 3: Locate the second shadow host inside the first shadow root
            second_shadow_host = first_shadow_root.find_element(By.CSS_SELECTOR, "#first-component")
            logging.info("✅ Second shadow host found.")

            # Step 4: Expand the second shadow root
            second_shadow_root = self.expand_shadow_element(second_shadow_host)
            logging.info("✅ Second shadow root expanded.")
            
     
            # Step 5: Click the element inside the second shadow root
            target_element = WebDriverWait(self.driver, 20).until(
            lambda driver: second_shadow_root.find_element(By.CSS_SELECTOR, "#voc-wrapper voc-vehicle-tile img")
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", target_element)
            time.sleep(1)  # Allow the page to adjust
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(target_element)
            )
            target_element.click()
            logging.info("✅ Element clicked successfully.")
            time.sleep(5)
        except Exception as e:
            logging.error(f"❌ Error interacting with Shadow DOM elements: {e}")    
        try:
            # Step 1: Find the first shadow host
            first_shadow_host = self.driver.find_element(By.CSS_SELECTOR, "#first-component")
            logging.info("✅ First shadow host found.")

            # Step 2: Expand the first shadow root
            first_shadow_root = self.expand_shadow_element(first_shadow_host)
            logging.info("✅ First shadow root expanded.")

            # Step 3: Locate the second shadow host inside the first shadow root
            second_shadow_host = first_shadow_root.find_element(By.CSS_SELECTOR, "#first-component")
            logging.info("✅ Second shadow host found.")

            # Step 4: Expand the second shadow root
            second_shadow_root = self.expand_shadow_element(second_shadow_host)
            logging.info("✅ Second shadow root expanded.")
             
                
            # Step 5: Click the element inside the second shadow root
            target_element = second_shadow_root.find_element(By.CSS_SELECTOR, "#voc-wrapper > div.voc-content.ng-tns-c1281076090-0 > div > main > voc-stage > div.main-section.content-side > voc-navigator-menu > wb7-card > ul > li:last-child > button")
            target_element.click()
            logging.info("✅ Element clicked successfully.")
            time.sleep(4)    
        
        except Exception as e:
            logging.error(f"❌ Error while performing configurator actions: {e}")