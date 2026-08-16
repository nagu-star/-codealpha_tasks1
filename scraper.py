import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time

base_url = "https://books.toscrape.com/"

data = []

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_page(url):

    for attempt in range(3):

        try:
            response = session.get(
                url,
                headers=headers,
                timeout=15
            )

            response.raise_for_status()

            time.sleep(1)

            return response

        except requests.RequestException as e:

            print(f"Request failed. Retry {attempt + 1}/3")
            time.sleep(3)

    return None


for page in range(1, 51):

    print(f"Scraping page {page}...")

    page_url = f"{base_url}catalogue/page-{page}.html"

    response = get_page(page_url)

    if response is None:
        print(f"Skipping page {page}")
        continue

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    books = soup.find_all(
        "article",
        class_="product_pod"
    )

    for book in books:

        title = book.find(
            "h3"
        ).find("a")["title"]

        price = book.find(
            "p",
            class_="price_color"
        ).text.strip()

        rating = book.find(
            "p",
            class_="star-rating"
        )["class"][1]

        availability = book.find(
            "p",
            class_="instock availability"
        ).text.strip()

        book_link = book.find(
            "h3"
        ).find("a")["href"]

        book_url = urljoin(
            page_url,
            book_link
        )

        book_response = get_page(book_url)

        if book_response is None:
            print(f"Could not get: {title}")
            continue

        book_soup = BeautifulSoup(
            book_response.text,
            "html.parser"
        )

        # Product information
        details = {}

        table = book_soup.find(
            "table",
            class_="table-striped"
        )

        if table:

            rows = table.find_all("tr")

            for row in rows:

                cells = row.find_all("td")

                if len(cells) == 2:

                    key = cells[0].text.strip()
                    value = cells[1].text.strip()

                    details[key] = value

        # Description
        description = ""

        heading = book_soup.find(
            "div",
            id="product_description"
        )

        if heading:

            paragraph = heading.find_next_sibling("p")

            if paragraph:
                description = paragraph.text.strip()

        # Image
        image_url = ""

        image = book_soup.find(
            "div",
            class_="item active"
        )

        if image:

            img = image.find("img")

            if img:

                image_url = urljoin(
                    book_url,
                    img.get("src")
                )

        data.append({

            "Title": title,
            "Price": price,
            "Rating": rating,
            "Availability": availability,
            "Product URL": book_url,
            "UPC": details.get("UPC", ""),
            "Product Type": details.get(
                "Product Type",
                ""
            ),
            "Price (excl. tax)": details.get(
                "Price (excl. tax)",
                ""
            ),
            "Price (incl. tax)": details.get(
                "Price (incl. tax)",
                ""
            ),
            "Tax": details.get(
                "Tax",
                ""
            ),
            "Number of Reviews": details.get(
                "Number of reviews",
                ""
            ),
            "Description": description,
            "Image URL": image_url
        })


df = pd.DataFrame(data)

df.to_csv(
    "books_scraped_data.csv",
    index=False
)

print("\n==============================")
print("SCRAPING COMPLETED")
print("==============================")
print("Total books collected:", len(df))
print("CSV file created successfully.")