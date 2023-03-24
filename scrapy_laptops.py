import logging
import requests
from typing import Dict
from bs4 import BeautifulSoup


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="scrapy_laptops.log",
)


def get_laptops_from_page(url: str) -> Dict[str, dict]:
    """Scrapes laptops data from a single page of the website.

    :param url: The URL to scrape laptops data from.
    :return: A dictionary contain laptops data for given page.
    """
    try:
        response = requests.get(url)
        doc = BeautifulSoup(response.text, "html.parser")

        raw_prices_list = doc.find_all("h4", "pull-right price")
        prices = [x.string for x in raw_prices_list]

        raw_title_list = doc.find_all("a", "title")
        titles = [x.string for x in raw_title_list]

        raw_description_list = doc.find_all("p", "description")
        descriptions = [x.string for x in raw_description_list]

        raw_reviews_count = doc.find_all("p", "pull-right")
        reviews = [x.string for x in raw_reviews_count]

        raw_stars_count = doc.find_all("p", {"data-rating": True})
        stars = [x["data-rating"] for x in raw_stars_count]

        current_page_laptops_dict = {
            title: {
                "price": price,
                "description": description,
                "reviews": review,
                "stars": star,
            }
            for title, price, description, review, star in zip(
                titles, prices, descriptions, reviews, stars
            )
        }

        return current_page_laptops_dict

    except Exception as e:
        logging.error(f"Error: {e}")
        return {}


def main():
    """Extracts laptop data from multiple pages of the website."""
    BASE_URL = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"
    PAGE_START = 1
    PAGE_END = 20

    laptops_dict = {}
    with requests.Session() as session:
        for page in range(PAGE_START, PAGE_END + 1):
            url = f"{BASE_URL}?page={page}"
            current_page_laptops_dict = get_laptops_from_page(url=url)
            laptops_dict.update(current_page_laptops_dict)

    logging.info(laptops_dict)


if __name__ == "__main__":
    main()
