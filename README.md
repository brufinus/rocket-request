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

These steps are tailored to a *Unix shell* or [*Git Bash*](https://gitforwindows.org/), but can be modified for a different CLI.

1. Download the [latest release](https://github.com/brufinus/rocket-request/releases/latest).
    - Click on **Source code** under **Assets**.
2. Extract and open the release.
3. (Optional) [Create and activate a virtual environment](https://docs.python.org/3/library/venv.html): `python -m venv .venv && source .venv/Scripts/activate`
4. Install requirements: `pip install build -r django-distribute/requirements.txt`
5. Build and install the app:

    ```bash
    python -m build django-distribute
    pip install django-distribute/dist/django_distribute*.tar.gz
    ```

6. Run migrations: `python django-rocket-request/manage.py migrate`
7. Run the dev server: `python django-rocket-request/manage.py runserver`
8. Access the web app at <http://localhost:8000/distribute>.

![Rocket Request main page](/.github/static/rocket-request-home.png)

![Rocket Request results page](/.github/static/rocket-request-results.png)

### Development

A bash script `run.sh` is included to build, install, and run the dev server in one step.
