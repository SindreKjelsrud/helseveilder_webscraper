import httpx
from selectolax.parser import HTMLParser

def fetch_question_url(url):
    # Define headers
    headers = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
    }

    # Define the parameters for the request
    params = {
        "action": "get-faqs",
        "idSource": "2",
        "list": "frequently_asked_questions",
        "idCategory": "8288",  # Id for category
        "from": "0",
        "size": "10",  # Adjust this to get more results
        "gender": "false",
        "age": "false",
        "zone": "default",
        "filter_query": "",
        "skip": "0",
        "load_categories": "false"
    }

    response = httpx.get(url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response
        data = response.json()
        
        # Extracting URLs from each item
        urls = [item['url'] for item in data['items']]
        return urls
    else:
        print(f"Failed to fetch data: {response.status_code}")

def fetch_all_info(url):
    # Define headers
    headers = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
    }

    response = httpx.get(url, headers=headers)
    html = HTMLParser(response.text)

    # Extracting the question and answer
    sporsmal = html.css_first('div.article-text').text()
    
    # Check if the element exists before accessing its text
    signatur_div = html.css_first('div.signatur')
    signatur = ""
    if signatur_div:
        signaturTxt = signatur_div.text()
        # Remove "Med vennlig hilsen" or "Vennlig hilsen"
        signaturTxt = signaturTxt.replace("Med vennlig hilsen", "").replace("Vennlig hilsen", "").strip()
        # Check if the text is empty after removal
        if signaturTxt:
            signatur = signaturTxt
        else:
            signatur = "Null signatur"
    else:
        signatur = "Null signatur"
    
    # Create array of results
    #result = [sporsmal, svar, signatur]

    return signatur

studenterspor_url = "https://www.studenterspor.no/ajax_handler.php"
question_urls = fetch_question_url(studenterspor_url)

for url in question_urls:
    print(fetch_all_info(url))