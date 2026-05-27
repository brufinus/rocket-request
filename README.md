# Rocket Request

Rocket Request is a web app utility for the factory automation game, Factorio.

It shows you how to distribute items across your rocket silos,
aiming to minimize the number of required launches.

A first-fit-decreasing algorithm is used to calculate the distribution of
items into silos such that the sum of each silo's weight does not exceed 1000 kg.

## Usage

### Requirements

- Python>=3.12

### Run Local Webapp

These steps are tailored to a *Unix shell* or [*Git Bash*](https://gitforwindows.org/), but can be modified for a different CLI.

1. Clone the repository or download and extract the [latest release](https://github.com/brufinus/rocket-request/releases/latest).
    - Click on **Source code** under **Assets**.
2. Open a terminal to the base project directory.
3. (Optional) [Create and activate a virtual environment](https://docs.python.org/3/library/venv.html): `python -m venv .venv && source .venv/Scripts/activate`
4. Install requirements: `pip install django`
5. Run migrations: `python migrate.py`
6. Run the dev server: `python runapp.py`
7. Access the web app at <http://localhost:8000/distribute>.

![Rocket Request main page](/.github/static/rocket-request-home.png)

![Rocket Request results page](/.github/static/rocket-request-results.png)
