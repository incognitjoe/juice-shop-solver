# Juice Shop Solver

* [Summary](#Summary)
* [Target Audience](#Target Audience)
* [Requirements](#Requirements)
* [How To Run](#How To Run)

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

- Clone this repo
- `cd` into the directory you created locally
- `pip install -r requirements.txt`(Create a virtualenv first if you'd like)
- Start the Juice Shop application
- `./solutions.py`, then wait a minute

# Why?

I'm a software tester looking to improve my security and automation knowledge, seemed like a 
fun way to kill two birds with one stone. I prefer working with APIs directly when I can, 
so for simplicity the only challenges that require Selenium are ones that _must_ execute 
some Javascript(Python, naturally, does not have a Javascript engine included.)

The actual exploratory effort and techniques used to prepare this repository have been 
written up in my blog [here](https://incognitjoe.github.io/hacking-the-juice-shop.html).