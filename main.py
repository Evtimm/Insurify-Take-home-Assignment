from flask import Flask, jsonify, request
import logging


from expected_population import ExpectedPopulation, TopCountries
from countries import scrape_population_and_growth

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

logger = logging.getLogger(__name__)


def validate_body(request_data):
    try:
        request_json = request_data.json
        assert request_json
        return request_json
    except AssertionError as ae:
        logger.exception(ae)
        return (
            jsonify({"error": "There is an issue with the body of your request"}),
            400,
        )
    except Exception as err:
        logger.exception(err)
        return jsonify({"error": str(err)}), 400


@app.route("/expected_population", methods=["POST"])
def expected_population():
    request_data = validate_body(request)
    if type(request_data) is tuple:
        return request_data
    try:
        country, year, population = ExpectedPopulation(request_data).predict()
        return jsonify({
            "country": country,
            "year": year,
            "population": population
        })
    except Exception as err:
        if len(err.args) == 2:
            return jsonify(err.args[0]), err.args[1]
        logger.exception(err)
        return jsonify({"error": str(err)}), 500


@app.route("/top_countries", methods=["POST"])
def top_countries():
    request_data = validate_body(request)
    if type(request_data) is tuple:
        return request_data
    try:
        return jsonify(TopCountries(request_data).get_top_countries())
    except Exception as err:
        if len(err.args) == 2:
            return jsonify(err.args[0]), err.args[1]
        logger.exception(err)
        return jsonify({"error": str(err)}), 500


if __name__ == "__main__":
    scrape_population_and_growth()
    app.run()
