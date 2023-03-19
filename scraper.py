# Import libraries
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

def scrape_current_page(driver):
    # Find all links with "detail.aspx?" in their href attribute
    links = driver.find_elements_by_css_selector("a[href*='detail.aspx?']")
    pattern = re.compile(r"detail\.aspx\?")
    matching_links = [link.get_attribute("href") for link in links if pattern.search(link.get_attribute("href"))]

    data_rows = []
    for link in matching_links:
        # Visit the link
        driver.get(link)
        # time.sleep(1)

        # Get the page source and create a Beautiful Soup object
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Find the table on the page
        table = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_dvwDetail"})

        # Get all unique values from the table
        unique_values = set([td.text.strip()
                             for td in table.findAll("td", {"class": "detailColumn"})])

        # Store the data in a dictionary
        row = {}
        for tr in table.findAll("tr"):
            tds = tr.findAll("td", {"class": "detailColumn"})
            if len(tds) == 2:
                key = tds[0].text.strip()
                val = tds[1].text.strip()
                row[key] = val

        # Add the row to the data list
        data_rows.append(row)

        # Go back to the search results page
        driver.back()
        # time.sleep(1)

        # Find the links again on the page
        links = driver.find_elements_by_css_selector("a[href*='detail.aspx?']")
        matching_links = [link for link in links if pattern.search(link.get_attribute("href"))]

    return data_rows

# Create a new instance of the Firefox driver
driver = webdriver.Firefox(executable_path='utils/geckodriver')

# Load the web page
driver.get("https://public.govnu.ca/search.aspx")

# Find the drop-down element by its ID
dropdown = driver.find_element_by_id("ctl00_ContentPlaceHolder1_cboDepartment")

# Create a Select object from the drop-down element
select = Select(dropdown)

# Select an option by its value
select.select_by_value("Family Services")

# Finding the submit button element
submit_button = driver.find_element_by_id(
    "ctl00_ContentPlaceHolder1_btnSubmit")

# Click submit button
submit_button.click()

# Create an empty dataframe to store the data
df = pd.DataFrame(columns=['Project Name:', 'Contract Type:', 'Contract Method:', 'Community:', 'Originating Department:', 'Awarded To:', 'Award Date:', 'Award Value:'])

data_rows = []  # Initialize an empty list to store all the rows

for i in range(1, 37):
    # Scrape the data on the current page
    data_rows.extend(scrape_current_page(driver))

    # If we are on page 10 or page 20, click the ellipsis (...) to go to the next set of pages
    if i == 10 or i == 20 or i == 30:
        ellipsis = driver.find_elements_by_xpath("//a[contains(text(), '...')]")[-1]
        ellipsis.click()
        time.sleep(3)
    else:
        # Go to the next page
        next_page = driver.find_element_by_link_text(str(i + 1))
        next_page.click()
        time.sleep(3)

# Create the DataFrame from the collected rows
df = pd.DataFrame(data_rows)
print(df)
df.to_csv('./data/data.csv', index=False)

# Close the browser
driver.quit()