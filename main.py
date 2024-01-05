import httpx
from selectolax.parser import HTMLParser

url = "https://www.studenterspor.no/kropp-sex-og-identitet/#/sykdom-og-symptomer"
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"}

response = httpx.get(url, headers=headers)

print(response.status_code)
