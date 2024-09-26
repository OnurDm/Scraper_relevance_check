# -*- coding: utf-8 -*-
"""
Code to scrape data of off gig listings from temper.works
Step 1. Gather all urls
"""
import csv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import time

# Set Firefox options to run headless
options = Options()
options.headless = False

# Specify the path to the geckodriver
driver = webdriver.Firefox(service=Service('F:\\EUR\\Master_Thesis_code\\geckodriver.exe'))

def scrape_gig_listings():

    # Initialize the list to store gig URLs
    gig_urls = []

    # URL of the page containing gig listings
    url = "https://temper.works/werk-zoeken"
    
    # Navigate to the gig listings page
    driver.get(url)

    # Wait for the gig listings to load
    time.sleep(15)

    # Wait for the cookie wall to load and accept the cookies
    try:
        accept_cookies_script = """
            const element = document.querySelector('#usercentrics-root').shadowRoot.querySelector("button[data-testid='uc-accept-all-button']");
            element.click();
        """
        driver.execute_script(accept_cookies_script)
    except Exception:
        pass  
    
    # Wait for the gig listings to load
    time.sleep(10)

    # Get all gig URLs
    gig_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-v-c75b0d42]")    
    for gig_element in gig_elements:
        gig_url = gig_element.get_attribute('href')
        gig_urls.append(gig_url)

    return gig_urls

# Call the function to scrape gig listings and store the result in a variable
scraped_links = scrape_gig_listings()

# Create a list to store the scraped data
scraped_data = []

# Write the scraped links to a CSV file
with open('scraped_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Gig URLs'])
    for link in scraped_links:
        writer.writerow([link])

# Print the scraped links
for link in scraped_links[:25]:
    print(link)
    
# Close the Selenium webdriver session
driver.quit()


#%%
"""
Step 2. Gather gig data
""" 

# Set Firefox options to run headless
options = Options()
options.headless = False
    
driver_path = 'F:\\EUR\\Master_Thesis_code\\geckodriver.exe'
    
# Initial slice of scraped links
start_index = 501
end_index = 581
increment = 80 # Assuming we attempt to scrape n links in each iteration
unsuccessful_attempts = 0  # Track unsuccessful scraping attempts
max_unsuccessful_attempts = 2  # Threshold to adjust increment

def adjust_increment():
    global increment, unsuccessful_attempts
    if unsuccessful_attempts >= max_unsuccessful_attempts:
        increment += 10  # Increase the increment
        unsuccessful_attempts = 0  # Reset unsuccessful attempts counter
        print(f"Adjusting increment. New increment: {increment}")


# Calculate the next run time (30 minutes from now)
next_run_time = datetime.now() + timedelta(minutes=30)
        
    # Navigate to each URL and scrape the desired elements
while True:
        print(f"Starting scraping iteration for links {start_index} to {end_index}.")
        driver = webdriver.Firefox(service=Service(driver_path), options=options)
        links_to_scrape = scraped_links[start_index:end_index]
        scraped_data = []  # Store scraped data for each iteration
        
            
        for link in links_to_scrape:
                try:
                    driver.get(link)
                    time.sleep(5)  # wait for the page to load  
                
                   # Scrape the time elements for checking the date and time
                    shift_time = driver.find_element(By.CSS_SELECTOR, '.mb-px > div:nth-child(1) > label:nth-child(1) > div:nth-child(3) > div:nth-child(2) > p:nth-child(1)').text
                    gig_date = driver.find_element(By.CSS_SELECTOR, '.mb-px > div:nth-child(1) > label:nth-child(1) > div:nth-child(3) > div:nth-child(1) > h4:nth-child(1)').text
        
                   # Parse the gig date and shift time
                    gig_day = int(gig_date.split(' ')[1])  # assuming the format is 'di. 12 mrt.' 
                    gig_hour = int(shift_time.split('-')[0].split(':')[0].strip())  # assuming the format is '16:00 - 21:00'
                    gig_minute = int(shift_time.split('-')[0].split(':')[1].strip())
        
                   # Get the current date and time
                    now = datetime.now()
                   # Create a datetime object for the gig start time on the same day
                    gig_start_time = now.replace(hour=gig_hour, minute=gig_minute, second=0, microsecond=0)
                   # Calculate the difference in minutes
                    diff_minutes = (gig_start_time - now).total_seconds() / 60
                    # Check if the gig starts within the next 60 minutes and in 2 days
                    if 0 <= diff_minutes <= 30 and now.day + 2 == gig_day:
                   
                  
                        # Scrape the desired elements here.
                        applicants = driver.find_element(By.CSS_SELECTOR, '.mb-px > div:nth-child(1) > label:nth-child(1) > div:nth-child(3) > div:nth-child(2) > p:nth-child(2)').text
                        gig_date = driver.find_element(By.CSS_SELECTOR, '.mb-px > div:nth-child(1) > label:nth-child(1) > div:nth-child(3) > div:nth-child(1) > h4:nth-child(1)').text
                        pay = driver.find_element(By.CSS_SELECTOR, 'div.bg-blue-light:nth-child(1) > div:nth-child(1) > label:nth-child(1) > div:nth-child(3) > div:nth-child(1) > h4:nth-child(2)').text
                        quick_payment = driver.find_element(By.CSS_SELECTOR, 'div.agreement:nth-child(1) > p:nth-child(2)').text
                        rating = driver.find_element(By.CSS_SELECTOR, '.mr-4').text
                        rating_quantity = driver.find_element(By.CSS_SELECTOR, '.ml-4').text
                        job_description = driver.find_element(By.CSS_SELECTOR, '.whitespace-pre-line').text
                        category = driver.find_element(By.CSS_SELECTOR, '.pt-16').text 
                        shift_time = driver.find_element(By.CSS_SELECTOR, '.mb-px > div:nth-child(1) > label:nth-child(1) > div:nth-child(3) > div:nth-child(2) > p:nth-child(1)').text
                        # Scroll down the page
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)  # wait for the page to load after scrolling
                        location = driver.find_element(By.CSS_SELECTOR, '.top-0 > div:nth-child(2) > a:nth-child(10) > p:nth-child(2)').text
                        total_compensation = driver.find_element(By.CSS_SELECTOR, '.h-112 > div:nth-child(1) > h5:nth-child(1)').text
                    
                        # Replace newline characters in the job description
                        job_description = job_description.replace('\n', ' ')
                        # Replace ';' characters in the job description
                        job_description = job_description.replace(';', '|')
            
                        # Get the last 7 characters of the URL for the gig ID
                        gig_id = link[-7:]
                        
                        # Get the current timestamp
                        scrape_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
                        # Store the scraped data in a dictionary and append it to the list
                        scraped_data.append({
                            'Gig ID': gig_id,
                            'Applicants': applicants,
                            'Gig Date': gig_date,
                            'Pay': pay,
                            'Total Compensation': total_compensation,
                            'Quick Payment': quick_payment,
                            'Rating': rating,
                            'Rating Quantity': rating_quantity,
                            'Shift Time': shift_time,
                            'Job Description': job_description,
                            'Category': category,
                            'Location': location,
                            'URL': link,
                            'Scraped At': scrape_time  
                            })
                        # Reset unsuccessful attempts if data is successfully scraped
                        unsuccessful_attempts = 0
               
                except NoSuchElementException:
                    continue
                
        if not scraped_data:
            # If no data was scraped, consider it an unsuccessful attempt
            unsuccessful_attempts += 1
            adjust_increment()
        else:
            # Reset unsuccessful attempts counter if successful
            unsuccessful_attempts = 0
            
        # Increment the indices for the next iteration
        start_index += len(scraped_data) if scraped_data else + 20  # Ensure progress if no data was scraped
        end_index = start_index + increment
        
        # Close the Selenium webdriver session
        driver.quit()
        
        # Write the scraped data to a CSV file, appending to it
        with open('scraped_gigs.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Gig ID', 'Applicants', 'Gig Date', 'Pay', 'Total Compensation', 'Quick Payment', 'Rating', 'Rating Quantity', 'Shift Time', 'Job Description', 'Category', 'Location', 'URL', 'Scraped At']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:  # Write header only if file is empty
                writer.writeheader()
            for row in scraped_data:
                writer.writerow(row)
        
        # Close the Selenium webdriver session
        driver.quit()
        print(f"Completed scraping iteration for links {start_index} to {end_index}")
        # Calculate time to loop
        sleep_duration = (next_run_time - datetime.now()).total_seconds()
        if sleep_duration > 0:
            print(f"Sleeping for {sleep_duration} seconds.")
            time.sleep(sleep_duration)
      
        # Update next_run_time for the next iteration
        next_run_time = datetime.now() + timedelta(minutes=30)
        print(f"Completed scraping iteration. Next iteration at {next_run_time}.")
