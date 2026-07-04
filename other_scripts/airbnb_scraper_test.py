from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_selenium_setup(url):
    print("[*] Setting up Selenium WebDriver...")
    
    # 1. Setup Chrome driver automatically using webdriver-manager
    service = Service(ChromeDriverManager().install())
    
    # 2. Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    # Note: We are NOT using headless mode yet, so you can see the browser opening.
    
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"[*] Accessing URL: {url}")
        driver.get(url)
        
        # 3. Wait for the page to load (Airbnb uses a lot of React/JS)
        print("[*] Waiting for 5 seconds to allow JS to load...")
        time.sleep(5) 
        
        # 4. Get page title as a simple test
        title = driver.title
        print(f"[+] Successfully loaded page!")
        print(f"[+] Page Title: {title}")
        
    except Exception as e:
        print(f"[!] An error occurred during scraping: {e}")
    finally:
        print("[*] Closing browser in 3 seconds...")
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    # Testing with the main Airbnb website first
    test_url = "https://www.airbnb.com/"
    test_selenium_setup(test_url)