# -codealpha_tasks1
**Overview**
Scraped and cleaned book data from books.toscrape.com using Python (Requests +
BeautifulSoup) to generate an analysis-ready dataset.

**Files**
scraper.py : Scrapes all pages to collect basic details (title, price, rating, availability, UPC,
product type, description).
url.py : Enriches records with detailed product page info.
cleaning.py : Cleans data and outputs final datasets.

**Output**
books_scraped_data_complete.csv (Full raw dataset)
books_custom_analysis_dataset.csv (Cleaned: Title, Price, Rating, Availability, Product
Type)

**How to Run**
pip install requests beautifulsoup4 pandas
python scraper.py
python url.py
python cleaning.py

**Author: S. Nageswari | Data Analytics Intern, CodeAlpha**
