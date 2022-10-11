# Journal Backend
![Tests](https://github.com/kesler20/test_backend/actions/workflows/python-app.yml/badge.svg)

This repository contains the source code of the backend of the ``Jounral application v0.0``
this can be installed from the root directory as a package ``journal==0.0.0`` by running the following command
## Install journal locally and run using gunicorn
```bash
pip install -e .
```

to run the backend run 
```bash
gunicorn --workers 3 -k uvicorn.workers.UvicornWorker --threads 2 src.journal.main:app
```

## Dev instructions
all contributors should run tests which may ber run automatically on commit by using the following command
```bash
pip install -r requirements_dev.txt
pytest src
coverage html
```

if you get a "pytest" command not found error, you may want to run the command wihtin a conda virtual environment or run

```bash
python -m pytest src
```
where the -m flag is used to run the module, as such this workaround will work with other modules as well i.e. coverage
if the coverage command does not work after using the python environment variable
try

```bash
python -m coverage run -m pytest src
```
>the pytest package looks for all the directories named tests within the src directory and within the tests directory any function with test_ at the start
if you get Module 
the -e flag allows you to install the package from the current directory in editable mode
this will install all the dependencies of the package and put a link from the virtual environment to the actual source code directory, that way if you make a change to the file you don't need to reinstall the package

A linter can be used to perform static analysis before making commits i.e. flake8 
by running the following command
```bash
flake8 src
```
and a type checking is provided by mypy which cn be run from the following command, make sure to include a py.typed file next to the __init__.py file
```bash
mypy src
```
for making sure that the package works in different versions of python we use tox
the tox.ini file specifies a routine which can be run by tox consisting of setting up and installing
the journal package for different virtual environments with different versions of python
if you are on linux run 

if you do not have old versions of python installed run 
```bash
sudo apt-get install python3.6
sudo apt-get install python3.7
sudo apt-get install python3.8
sudo apt-get install python3.9
```
