# Rocket Request

Rocket Request is a web app utility for the factory automation game, Factorio.

It shows you how to distribute items across your rocket silos,
aiming to minimize the number of required launches.

A first-fit-decreasing algorithm is used to calculate the distribution of
items into silos such that the sum of each silo's weight does not exceed 1000 kg.

## Usage

### Requirements

- Python>=3.12

### Run Local Server

Optional: [Create and activate a virtual environment](https://docs.python.org/3/library/venv.html)

1. Clone or download the repository.
2. Install requirements: `pip install -r django-distribute/requirements.txt`
3. Run migrations: `python django-rocket-request/manage.py migrate`
4. Build and install django_distribute and run the development server: `./run.sh`
5. Access the web app at http://localhost:8000/distribute.

![Rocket Request main page](/.github/static/rocket-request-home.png)

![Rocket Request results page](/.github/static/rocket-request-results.png)
