# TTLA

[![Build Status](https://ahmad88me.semaphoreci.com/badges/ttla/branches/master.svg?key=7b050606-3d80-4698-a022-a3d6d1464203)](https://ahmad88me.semaphoreci.com/projects/ttla)
[![codecov](https://codecov.io/gh/oeg-upm/ttla/branch/master/graph/badge.svg)](https://codecov.io/gh/oeg-upm/ttla)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2619306.svg)](https://doi.org/10.5281/zenodo.2619306)


This application is meant to be an automated experiment and not
an application by it self to annotated numeric columns. Nonetheless, 
we are planning to create an application based on this approach
details will be mentioned here once we start.

# Install via pip
```
pip install ttla
```

[//]: # (# Prerequisits &#40;one time&#41;)

[//]: # (1. [pip]&#40;https://pip.pypa.io/en/stable/installing/&#41; )

[//]: # (2. [virtualenv]&#40;https://virtualenv.pypa.io/en/latest/&#41;)

[//]: # (3. create virtualenv: `virtualenv -p /usr/bin/python2.7 .venv`)

[//]: # (4. access the virtualenv: `source .venv/bin/activate`)

[//]: # (5. install dependencies: `pip install -r requirements.txt`)


<!-- 
# Run the web
1.  access the virtualenv: `source .venv/bin/activate`
2.  run the web app: `python app.py`
3.  visit `http://127.0.0.1:5000` in your local browser
-->

# Run the experiments

## To download the data of T2Dv2 automatically
```
python data/preprocessing.py
```
## Detection
```
python experiments/web_commons_v2.py detect
```
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
## Quick tests (test the algorithms, but does not include the t2d experiment)
```
sh run_tests.sh
```
## run tests with the T2Dv2 experiment (may take up to an hour)
```
sh run_t2dv2_tests.sh
```
*not that some tests may fail overtime as they depend on dbpedia*

# Coverage: 
## Coverage of the quick tests
```
sh run_cov.sh
```
## Coverage of T2Dv2 tests
```
sh run_t2dv2_cov.sh
```

# To publish
```
python setup.py sdist bdist_wheel
twine upload dist/*
```

# Contribution 
To contribute, please read the below to follow the same convention

## Code structure
* The source code related to detection of data types (e.g. categorical, continuous, ...) is located under `detect`.
* while the files related to the annotation of the semantic types (e.g. height of a person) are located under `label`.

