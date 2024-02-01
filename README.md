# Accessing Web Resources with Python

## How to Run
Put the following in your requirements.txt file
```
requests
beautifulsoup4
```

Open Jupyter Notebook and run the following commands:
```    
!pip install -r requirements.txt
import time
import requests
import csv
import html
```

## Detailed Comment for Every Part
Part 1: Scraping the list page
- Send a GET request to the given page URL
- Define the CSS selector to target the specific elements that contain the event URLs
- Loop through all pages
- Call the function and store the list of URLs

Part 2: Scraping the detail page
- Scrape event URLs from the list pages
- Function to get latitude and longitude from Nominatim
- Function to get weather information
- Function to scrape event details (including location and weather lookup)
- Write data to CSV

## Lessons Learned

- How to scrape information from website

## Questions / Uncertainties

- How to scrape photo from website?
- How to scrape the color of the photo from website?
- How to scrape specific photo? Such as scraping all the wedding dress photo.

## Contact

- Liliana Hsu
# TECHIN510