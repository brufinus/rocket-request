# Rocket Request

Rocket Request is a web app utility for the factory automation game, Factorio.

It shows you how to distribute items across your rocket silos,
aiming to minimize the number of required launches.

A first-fit-decreasing algorithm is used to calculate the distribution of
items into silos such that the sum of each silo's weight does not exceed 1000 kg.

## Usage

### Requirements

- Python>=3.12

### Local Server

Optional: [Create and activate a virtual environment](https://docs.python.org/3/library/venv.html)

1. Clone or download the repository.
2. Access the `django-rocket-request` directory: `cd django-rocket-request`
3. Install requirements: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Run the development server: `python manage.py runserver`
6. Access the web app at http://localhost:8000/distribute.

![Rocket Request main page](/.github/static/rocket-request-home.png)

![Rocket Request results page](/.github/static/rocket-request-results.png)
