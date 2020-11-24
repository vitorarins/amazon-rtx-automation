# Amazon Purchase Script 

Example: script to buy the things on Amazon 

forked from yosh1/amazon-automation & druyang/amazon-PS5-automation

Use at your own risk

Requirements: 
--- 
* Python 3 
* Python modules in `requirements.txt` 
* [WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads) in same directory 

Recommended to be run on Linux or Max. Would be a good script to run on a raspberry pi or server

Notes of caution: 
--- 

Things to check for on Amazon/potential edge cases: 

 * Amazon 2FA (an option is to disable but this will **expose your account to security problems**)
 * Currently uses 1 click buy. Confirm your default address + payments is correct before running this script
 * Captchas for hitting Amazon's server a lot

---

## Copy `.env`

```
$ cp .env.sample .env
```

## Run

```
$ pip install -r requirements.txt 
$ python3 main.py
```

Alternatively use Docker: 

```
$ docker-compose build
$ docker-compose up -d
```

