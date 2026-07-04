import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def scrape_city_metadata(cities_list, output_path):
    print("[*] Starting Selenium WebDriver for Data Enrichment...")
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=service, options=options)
    
    enriched_data = []
    
    for city in cities_list:
        print(f"\n[*] Scraping enrichment data for: {city.capitalize()}...")
        # Construct the Airbnb search URL for the city
        url = f"https://www.airbnb.com/s/{city}/homes"
        driver.get(url)
        
        # Wait for React and JavaScript to load the dynamic elements
        time.sleep(6) 
        
        try:
            # We will extract the main visible text from the page as a proof-of-concept 
            # for scraping dimensions (like average prices or amenities visible on search)
            # Using a broad XPath to catch listing details (Airbnb DOM changes frequently)
            elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'g1qv1ctd') or contains(@data-testid, 'card-container')]")[:3]
            
            extracted_features = []
            for el in elements:
                if el.text.strip():
                    # Replace newlines with pipes for cleaner CSV storage
                    extracted_features.append(el.text.replace('\n', ' | '))
            
            enriched_data.append({
                'city': city,
                'scraped_sample_data': ' || '.join(extracted_features) if extracted_features else 'Data blocks not found'
            })
            print(f"[+] Successfully scraped data for {city}")
            
        except Exception as e:
            print(f"[!] Failed to extract data for {city}: {e}")
            enriched_data.append({
                'city': city,
                'scraped_sample_data': 'Error'
            })
            
    print("\n[*] Closing browser...")
    driver.quit()
    
    # Save the scraped dimensional data to the Silver layer
    df = pd.DataFrame(enriched_data)
    df.to_csv(output_path, index=False)
    print(f"[+] Enrichment complete! Data saved to: {output_path}")

if __name__ == "__main__":
    # We take a sample of cities that exist in our dataset for this test
    # (In a production pipeline, we would read the unique cities from silver_airbnb_cleaned.csv)
    target_cities = ['amsterdam', 'paris', 'rome']
    
    OUTPUT_FILE = "silver_city_enrichment.csv"
    
    scrape_city_metadata(target_cities, OUTPUT_FILE)