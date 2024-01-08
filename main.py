import httpx
from selectolax.parser import HTMLParser
import re

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

    # Extracting the question "sporsmal"
    sporsmal = html.css_first('div.article-text').text()
    
    # Extracting the answer "svar" and the signature "signature"
    svar = ""
    signature = ""
    specific_div = html.css_first('.article-text.font-serif.text-base.py-10')
    if specific_div:
        p_elements = specific_div.css('p')
        full_text = ' '.join([p.text() for p in p_elements])

        # Separate the signature using a regular expression
        signature_match = re.search(r'(Vennlig hilsen|Med vennlig hilsen|Mvh|Lykke til!)\s*(.*)', full_text, re.IGNORECASE)
        if signature_match:
            signature = signature_match.group(2)  # This is the signature text
            svar = full_text[:signature_match.start()]  # This is the text before the signature
        else:
            svar = full_text  # In case there is no signature

    # Clean up the signature
    cleaned_signature = re.sub(r'(Vennlig hilsen|Med vennlig hilsen|Mvh|Lykke til!)\s*', '', signature, flags=re.IGNORECASE)
    cleaned_signature = re.sub(r'^[\s,]*', '', cleaned_signature).strip()  # Remove leading commas and spaces
    
    # Create array of results
    result = [sporsmal, svar, cleaned_signature]

    return result

studenterspor_url = "https://www.studenterspor.no/ajax_handler.php"
question_urls = fetch_question_url(studenterspor_url)

for url in question_urls:
    print(fetch_all_info(url))