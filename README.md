# WIP

*Nothing to see here, a work in progress!*


# OmniConverter

![Travis CI](https://travis-ci.org/michaelpb/omnithumb.svg?branch=master)

Mostly stateless microservice for generating on-the-fly thumbs and previews of
a wide variety of file types.

Fully extendable to create any arbitrary conversion pipelines.


# Getting started

## Without Docker

It's much simpler to run a dev environment without Docker, just using
`virtualenv`, and using asyncio's task queueing. This might not precisely
resemble production environments, however it is very close.

1. Install Python 3, including `pip` and `venv`:
    * On Debian-based distros:
        * `sudo apt-get install python3 python3-env python3-pip`
    * On macOS, use something like `brew`
2. Create a virtualenv. For example:
    * `mkdir -p ~/.venvs/`
    * `python3 -m venv ~/.venvs/omnic`
3. Activate virtualenv:
    * `source ~/.venvs/omnic/bin/activate`
    * You will need to do this any time you want to work
4. Install dependencies:
    * `pip install -r requirements/local.txt`
5. (Optional) Run test suite:
    * `py.test`
6. Start the server:
    * `./bin/omnic runserver`


## Test routes

To test it, try visiting something like:
* http://localhost:8080/media/thumb.png:200x200/?url=unsplash.it/450/450

The first time you visit it it will just be a single placeholder pixel.
Subsequent times it should be 200x200 thumbnail

You might also be able to run this, if you have `unoconv` and ImageMagick
(providing the `convert` command) installed:
* `http://localhost:8080/media/thumb.jpg:200x200/?url=idee.org/Georgia_opposition_NATO-Eng-F.doc`

This will convert the `.doc` into a PDF, then into a JPG thumbnail

If you have `jsc3d` installed (a Node JavaScript based 3D model renderer), then
the following should render a delightful trumpet:
* `http://localhost:8080/media/thumb.jpg:200x200/?url=people.sc.fsu.edu/~jburkardt/data/obj/trumpet.obj`

The built-in converters interface with a variety of system binaries in order to
provide rendering and conversion of many document, image, mesh. Adding new
converters and rasterizers is simple, with relatively minimal code!


## With Docker

1. TODO: Add in docker compose files for getting this bad boy up and
running


## Thx

* Used Nekroze' cookiecutter to start this package:
* https://github.com/Nekroze/cookiecutter-pypackage
