# Insurify-Take-home-Assignment

Flask app written to specification. Two endpoints available:

- /expected_population
  Expects POST request with body in the following format:
```
{
    "country": "country_name",
    "year": 2022
}
```
  Returns JSON object in the format:
```
{
    "country": "country_name",
    "year": 2022,
    "population": 1234567890
}
```
  

- /top_countries
  Expects POST request with body in the following format:
```
{
    "year": 2022
}
```
  Returns JSON object in the format:
```
{
    "country_1": 321,
    "country_2": 210,
    "country_3": population,
}
```
