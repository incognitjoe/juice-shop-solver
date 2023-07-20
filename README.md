# Juice Shop Solver

* [Summary](#Summary)
* [Target Audience](#Target_Audience)
* [Requirements](#Requirements)
* [How To Run](#How_To_Run)
* [Why?](#Why?)

# Summary

A collection of Python 2.7 functions for solving the various challenges in the 
[OWASP Juice Shop](https://github.com/bkimminich/juice-shop), using 
[Requests](http://docs.python-requests.org/en/master/) and for two challenges, 
[Selenium 3.0](https://pypi.python.org/pypi/selenium). 100% complete for release 
[2.18](https://github.com/bkimminich/juice-shop/releases/tag/v2.18.0), future versions may
change the method and difficulty of any or all of the challenges.  

# Target Audience

Testers interested in security testing and automation primarily. Assumes some familiarity with 
security concepts and the Python programming language.  

# Requirements

- [OWASP Juice Shop](https://github.com/bkimminich/juice-shop) running on http://localhost:3000
- Python 2.7.12
- Python dependencies in requirements.txt
- [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) available on your system PATH

# How To Run

The test suite defaults to attacking http://localhost:3000. This may not be where you run your JuiceShop, so we've added command line arguments.

- `--protocol`, to specify http or https
- `--hostname`, to indicate an IP address or hostname
- `--port`, to indicate the target port

Since we rely on an older Python version and requirements, it's safest to run this project in Docker.

## Use my Docker container

You can use my pre-built image, if you don't want to build your own.

- `docker pull tsluijter/juice-shop-solver`
- `docker run --rm juice-shop-solver --help` to show how to run the project

For example: 
- `docker run --rm juice-shop-solver --protocol http --hostname 10.0.2.15 --port 3000`

## Build your own Docker container

- Clone this repo
- `cd` into the directory you create locally
- `docker build -t juice-shop-solver .` to create the container image
- `docker run --rm juice-shop-solver --help` to show how to run the project

For example:

- `docker run --rm juice-shop-solver --protocol http --hostname 10.0.2.15 --port 3000`
- `docker run --rm juice-shop-solver --protocol https --hostname juiceshop.azuresites.com --port 443`

Otherwise:

- Clone this repo
- `cd` into the directory you created locally
- `pip install -r requirements.txt`(Create a virtualenv first if you'd like)
- Start the Juice Shop application
- `python ./solutions.py`, then wait a minute
- Or if JuiceShop runs elsewhere: `python ./solutions.py --hostname 10.0.2.15`

# Why?

*This section is not mine, it was written by the original author*:

> I'm a software tester looking to improve my security and automation knowledge, seemed like a fun way to kill two birds with one stone. I prefer working with APIs directly when I can, so for simplicity the only challenges that require Selenium are ones that _must_ execute some Javascript(Python, naturally, does not have a Javascript engine included.)

> The actual exploratory effort and techniques used to prepare this repository have been written up in my blog [here](https://incognitjoe.github.io/hacking-the-juice-shop.html).

