from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import unittest
import logging
import time
import os
from ConfigCompleted import ConfiguratorCompleted
from CTAVerifierPDP import CTAVerifier

class VerifyElements(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument("--disable-gpu")
        options.add_argument("--enable-webgl")
        #options.add_argument("--maximize")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        options.add_argument("profile-directory=Default")
        #options.add_argument("--start-fullscreen")
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

    def test_verify_elements(self):
        
        url = "https://www.mercedes-benz.at/vans"  # Replace with the actual URL

        self.driver.get(url)
        WebDriverWait(self.driver, 15).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        # Handle cookie banner if present
        self.handle_cookies()
        time.sleep(2)  # Optional: wait for the cookies to be accepted
        
        self.driver.get("https://www.mercedes-benz.at/passengercars/buy/new-car/search-results.html/vehicleCategory-new-commercial-vans/brand-Mercedes-Benz/modelIdentifier-SPRINTER?emhsortType=price-asc&emhbodyType=PANEL_VAN")    
        element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "img.wbx-vehicle-tile__image-img"))
        )
        parent_element = element.find_element(By.XPATH, "./ancestor::a")  # Locate the parent <a> tag
        pdp_url = parent_element.get_attribute("href")  # Extract the href attribute
        logging.info(f"🌍 Extracted PDP URL: {pdp_url}")
     
        self.driver.get(pdp_url)
        logging.info(f"🌍 Opened PDP URL: {pdp_url}")
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(6)  # Wait for the page to load
        
        self.driver.get(url)
        time.sleep(4)  # Optional: wait for the page to load again

        # Step 5: Call CTAVerifier to verify CTAs
        cta_verifier = CTAVerifier(self.driver)  # Instantiate the CTAVerifier class

        # Define selectors and expected href
        parent_selector = 'div.hp-campaigns__content'
        primary_cta_selector = 'div.hp-campaigns__content a'
        expected_href_value = "/buy/new-car/product.html/"

        # Call the verify_ctas method
        result = cta_verifier.verify_ctas(parent_selector, primary_cta_selector, expected_href_value)

        # Assert the result
        self.assertTrue(result, "Primary CTA verification failed.")

      

        """  
        # Step 2: Verify elements within the shadow DOM
        try:
            parent_element = self.driver.find_element(By.CSS_SELECTOR, 'body > div.root.responsivegrid.owc-content-container > div > div.responsivegrid.ng-content-root.aem-GridColumn.aem-GridColumn--default--12 > div > div:nth-child(8) > div > div > div > div > div:nth-child(1) > article > div > div.hp-campaigns__content')
            logging.info("✅ Parent element located.")
        except Exception as e:
            logging.error(f"❌ Parent element not found: {e}")
            return
        
        time.sleep(3)  # Optional: wait for the elements to load
        
        # Step 3: Locate the Primary CTA child element within the parent element
        try:
            specific_cta = self.driver.find_element(By.CSS_SELECTOR, 'body > div.root.responsivegrid.owc-content-container > div > div.responsivegrid.ng-content-root.aem-GridColumn.aem-GridColumn--default--12 > div > div:nth-child(8) > div > div > div > div > div:nth-child(1) > article > div > div.hp-campaigns__content > div > a')
            logging.info("✅ Primary CTA element located.")
            
            # Verify if the href includes "/buy/new-car/search-results.html/"
            href_value = specific_cta.get_attribute("href")
            if "/buy/new-car/product.html/" in href_value:
                logging.info(f"✅ The href attribute includes '/buy/new-car/product.html/': {href_value}")
            else:
                logging.warning(f"⚠️ The href attribute does not include '/buy/new-car/product.html/': {href_value}")
                
            
            # Optionally, interact with the CTA (e.g., click it)
            specific_cta.click()
            logging.info("✅ Specific CTA element clicked.")
        
        except Exception as e:
            logging.error(f"❌ Primary CTA element not found: {e}")
            return    
        """        
       
    
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()