# bob
[![Build Status](https://semaphoreci.com/api/v1/ahmad88me/bob/branches/master/badge.svg)](https://semaphoreci.com/ahmad88me/bob)
[![codecov](https://codecov.io/gh/oeg-upm/bob/branch/master/graph/badge.svg)](https://codecov.io/gh/oeg-upm/bob)
[![status](https://img.shields.io/badge/status-under%20development-ff69b4.svg)](https://github.com/oeg-upm/bob)

This application is meant to be an automated experiment and not
an application by it self to annotated numeric columns. Nonetheless, 
we are planning to create an application based on this approach
details will be mentioned here once we start.


# Prerequisits (one time)
1. [pip](https://pip.pypa.io/en/stable/installing/) 
2. [virtualenv](https://virtualenv.pypa.io/en/latest/)
3. create virtualenv: `virtualenv -p /usr/bin/python2.7 .venv`
4. access the virtualenv: `source .venv/bin/activate`
5. install dependencies: `pip install -r requirements.txt`


<!-- 
# Run the web
1.  access the virtualenv: `source .venv/bin/activate`
2.  run the web app: `python app.py`
3.  visit `http://127.0.0.1:5000` in your local browser
-->

# Run the experiments
## Detection

## Labeling
1. Label (may take up to an hour, it needs to be connected to the internet)
```
python experiments/web_commons_v2.py label
```
2. Get the kinds (offline, quick)
```
python experiments/web_commons_v2.py addkinds
 
```
3. Show scores (offline, quick)
```
python experiments/web_commons_v2.py scores
 
```


# Tests
```
python tests/test.py
```
*not that some tests may fail overtime as they depend on dbpedia*
# Coverage: 
```
coverage run --source=. --omit=.venv/*  tests/test.py
coverage report
```

# DATA
## T2Dv2

* [typology](https://drive.google.com/file/d/1VND173tUndx0TTaBVrQQbzY58RQsypS6/view?usp=sharing)
* [csv files](https://github.com/ahmad88me/TADA-NumCol/tree/master/web_commons/data)

# Contribution 
To contribute, please read the below to follow the same convention

## Code structure
* The source code related to detection of data types (e.g. categorical, continuous, ...) is located under `detect`.
* while the files related to the annotation of the semantic types (e.g. height of a person) are located under `label`.

