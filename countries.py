import requests
import urllib.parse
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

population_and_growth = {}


def scrape_population_and_growth():
    logger.info("Scraping population and growth...")

    global population_and_growth

    # A better approach would be to scrape and update the data independently
    # of the app. This way if the website is down the application will still
    # work with the last available data.
    growth_rates_page = requests.get(url="https://worldpopulationreview.com/")
    soup = BeautifulSoup(growth_rates_page.content, "html.parser")

    table_body = soup.find("tbody", {"class": "jsx-2006211681"})

    for row in table_body.find_all("tr"):
        name = row.find_all_next("td")[1].text
        growth = row.find_all_next("td")[6].text
        # population as of 2020
        population = row.find_all_next("td")[3].text.replace(",", "")
        population_and_growth[name.lower()] = (float(growth[:-1]), int(population))

    logger.info("Scraping complete")


class Country:
    def __init__(self, name):
        self.name = name

    def get_current_population(self) -> int:
        # The population data is already scraped but this is just to showcase an
        # alternative API integration
        rest_country = requests.get(
            url="https://restcountries.com/v3/name/" + urllib.parse.quote(self.name)
        )

        if rest_country.status_code != 200:
            raise Exception({"error": "Unable to fetch country"}, 409)
        if len(rest_country.json()) != 1:
            raise Exception({"error": "Too many countries match this name"}, 409)
        if not rest_country.json()[0].get("population", False):
            raise Exception({"error": "Current population not found in data set"}, 409)

        return rest_country.json()[0].get("population")

    def get_growth_rate(self) -> float:
        global population_and_growth

        try:
            return population_and_growth[self.name.lower()][0]
        except KeyError:
            raise Exception(
                {"error": "Growth rate not found for country: " + self.name}, 409
            )

    @staticmethod
    def get_population_and_growth():
        global population_and_growth
        return population_and_growth
