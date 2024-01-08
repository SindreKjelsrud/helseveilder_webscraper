# Webscraper needed for [Helseveileder](https://github.com/haraldnilsen/helseveileder)
> Part of Bachelor-project V2024

## 📝 Info

This webscraper will retrieve questions and answers, as well as the category assigned to the question, from [Studenterspør.no](https://studenterspor.no/). This will be used in our Bachelor project.

## 📋 Prerequisites

- ***Python 3.x***
- ***httpx*** ~ HTTP client
- ***HTMLParser*** (from [`selectolax.parser`](https://github.com/rushter/selectolax/)) ~ a fast HTML5 parser with CSS selectors
- ***re*** ~ regular expression matching operations

## 🛠️ How to run locally

1. Create Python environment: `python -m venv venv`
2. Activate environment: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Run ***main.py*** to get a csv.file: `python main.py`
