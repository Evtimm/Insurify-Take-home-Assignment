from copy import deepcopy
from countries import Country


class ExpectedPopulation:
    def __init__(self, request_data):
        self.country, self.year = self.validate_request_data(request_data)

    @staticmethod
    def validate_request_data(request_data):
        if not bool(request_data.get("country", False)) or not bool(
            request_data.get("year", False)
        ):
            raise Exception(
                {
                    "error": "Fields 'country' and 'year' must be present in the request body"
                },
                400,
            )

        if not isinstance(request_data["country"], str) or not isinstance(
            request_data["year"], int
        ):
            raise Exception(
                {"error": "'country' must be a string, 'year' must be an int"}, 400
            )

        if request_data["year"] < 2022:
            raise Exception({"error": "'year' must be in the future."}, 400)

        return request_data["country"], request_data["year"]

    def predict(self):
        country = Country(name=self.country)
        future_population = country.get_current_population()
        growth_rate = country.get_growth_rate()

        for i in range(self.year - 2022):
            # growth rate is a % so I divide by 100
            future_population += future_population * growth_rate / 100

        return country.name, self.year, int(future_population)


class TopCountries:
    def __init__(self, request_data):
        self.year = self.validate_request_data(request_data)

    @staticmethod
    def validate_request_data(request_data):
        # I realise there is some code repetition here with the other class, would consider this
        # for a possible optimisation
        if not bool(request_data.get("year", False)):
            raise Exception(
                {"error": "Field 'year' must be present in the request body"}, 400
            )
        if not isinstance(request_data["year"], int):
            raise Exception({"error": "'year' must be an int"}, 400)
        if request_data["year"] < 2022:
            raise Exception({"error": "'year' must be in the future."}, 400)

        return request_data["year"]

    def get_top_countries(self):
        # A number of implementations come to mind
        # I could multithread the calculations
        # I could get the top countries now + the fastest growing countries and only consider those
        # I could store the calculation results and use that as a checkpoint for calculating dates further in the future
        # This is by far the easiest and most processor intensive solution since there are no
        #   time or processing constraints
        population_and_growth = deepcopy(Country(name=None).get_population_and_growth())

        # population number scraped is as of 2020
        for y in range(self.year - 2020):
            for country in population_and_growth:
                growth, population = population_and_growth[country]
                population += population * growth / 100
                population_and_growth[country] = (growth, int(population))

        sorted_countries = {
            k: v[1]
            for k, v in sorted(
                population_and_growth.items(), key=lambda item: item[1][1], reverse=True
            )
        }
        return dict(list(sorted_countries.items())[:20])
