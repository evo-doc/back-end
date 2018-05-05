# EvoDoc / Back End
[![Build Status](https://travis-ci.org/evo-doc/back-end.svg?branch=master)](https://travis-ci.org/evo-doc/back-end)
[![codecov](https://codecov.io/gh/evo-doc/back-end/branch/master/graph/badge.svg)](https://codecov.io/gh/evo-doc/back-end)

This is backend api for Evodoc app.

## Minimal requirements

Our app need database, you can either use sqlite or postgresql, both should do the job, but production will be only on postgresql. Tests are however performed on sqlite by default.

## How to run APP

First you have to setup configuration, in `/conf` you will find example of local configuration.

In development use flask run, after installation everything from `requirements.txt`. After that you have to define, where flask can find evodoc as application using this `export FLASK_APP=relative/path/to/evodoc/folder`, then you should also type `export FLASK_ENV=dev` (this enables dev enviroment). After this you should be able to run app just by typing `flask run`.

## Tests

We are using pytest for our unit and itegration tests, tests can be executed using `python3 -m pytest`.

## Documentation

For code documentation we are using sphinx, for api [link to api doc](https://evodoc.docs.apiary.io/)

