from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import unittest
import logging
import time
import os


class VerifyElements(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument("--disable-gpu")
        options.add_argument("--enable-webgl")
        options.add_argument("--maximize")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        options.add_argument("profile-directory=Default")
        options.add_argument("--start-fullscreen")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
        self.vars = {}
        logging.info("✅ Browser opened in headless mode and in full-screen.")

        self.screenshot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Element Verification")
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def tearDown(self):
        self.driver.quit()
        logging.info("✅ Browser closed.")

    def handle_cookies(self):
        """Handles the cookie banner if present."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "cmm-cookie-banner"))
            )
            time.sleep(2)
            logging.info("✅ Cookie banner detected.")

            self.driver.execute_script("""
                document.querySelector("cmm-cookie-banner").shadowRoot.querySelector("wb7-button.button--accept-all").click();
            """)
            logging.info("✅ Clicked on the cookie acceptance button.")
        except Exception as ex:
            logging.warning(f"⚠️ Could not click cookie banner: {ex}")

    def expand_shadow_element(self, element):
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root
    
    
    def find_and_click_shadow_element(self):
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
    
    def perform_configurator_actions(self):
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
            logging.error(f"❌ Error interacting with the configurator: {e}")
                 

    def test_interact_with_shadow_dom(self):
        self.driver.get("https://www.mercedes-benz.de/vans/buy/van-online-configurator.html#/de_de?models=SPRINTER_NEW&bodyTypes=PANELVAN?internal_test=true")
        self.handle_cookies()
        self.find_and_click_shadow_element()
        self.perform_configurator_actions()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()