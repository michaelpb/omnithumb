# WIP

*Nothing to see here, a work in progress!*


# OmniThumb

Mostly stateless microservice for generating on-the-fly thumbs and previews of
a wide variety of file types.


# Getting started

## Without Docker

It's much simpler to run a dev environment without Docker, just using
`virtualenv` as the backend. This will not precisely resemble production
environments, however it is very close.

1. Install Python 3, including `pip` and `venv`:
    * On Debian-based distros:
        * `sudo apt-get install python3 python3-env python3-pip`
    * On macOS, use something like `brew`
2. Create a virtualenv. For example:
    * `mkdir -p ~/.venvs/`
    * `python3 -m venv ~/.venvs/omnithumb`
3. Activate virtualenv:
    * `source ~/.venvs/omnithumb/bin/activate`
    * You will need to do this any time you want to work
4. Install dependencies:
    * `pip install -r requirements/local.txt`
5. Start the server:
    * `python manage.py runserver`

To test it, try visiting:
* http://localhost:8080/thumb/?width=100&height=100&url=unsplash.it/1010/1010

The first time you visit it it will just be a single placeholder pixel.
Subsequent times it should be 100x100 thumbnail

## With Docker

1. TODO: Add in docker compose files for getting this bad boy up and
running


## Thx

* Used Nekroze' cookiecutter to start this package:
* https://github.com/Nekroze/cookiecutter-pypackage
