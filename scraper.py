# Import libraries
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

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

# Find all links with "detail.aspx?" in their href attribute
links = driver.find_elements_by_css_selector("a[href*='detail.aspx?']")
pattern = re.compile(r"detail\.aspx\?")
matching_links = [link.get_attribute(
    "href") for link in links if pattern.search(link.get_attribute("href"))]

# Create an empty dataframe to store the data
df = pd.DataFrame(columns=['Project Name:', 'Contract Type:', 'Contract Method:', 'Community:', 'Originating Department:', 'Awarded To:', 'Award Date:', 'Award Value:'])


for link in matching_links:
    # Visit the link
    driver.get(link)
    # time.sleep(3)

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
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    # Go back to the search results page
    driver.back()

    # Find the links again on the page
    links = driver.find_elements_by_css_selector("a[href*='detail.aspx?']")
    matching_links = [link for link in links if pattern.search(
        link.get_attribute("href"))]

# Drop the duplicate columns
df = df.loc[:, ~df.columns.duplicated()]

# Convert the data list to a pandas DataFrame
df = pd.DataFrame(df)
print(df)
