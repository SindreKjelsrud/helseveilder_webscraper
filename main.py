import httpx
from selectolax.parser import HTMLParser
import re
import csv
import config

def fetch_question_url(url):
    # Define headers
    headers = config.headers
    # Define the parameters for the request
    params = {
        "action": "get-faqs",
        "idSource": "2",
        "list": "frequently_asked_questions",
        "idCategory": "8288",  # Id for category
        "from": "0",
        "size": "100",  # Adjust this to get more results
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
    headers = config.headers

    response = httpx.get(url, headers=headers)
    html = HTMLParser(response.text)

    # Extracting the question
    questions = html.css_first('div.article-text').text()
    
    # Extracting the answer and the signature
    answers = ""
    signature = ""
    specific_div = html.css_first('.article-text.font-serif.text-base.py-10')
    if specific_div:
        p_elements = specific_div.css('p')
        full_text = ' '.join([p.text() for p in p_elements])

        # Separate the signature using a regular expression
        signature_match = re.search(r'(Vennlig hilsen|Med vennlig hilsen|Mvh|Lykke til!)\s*(.*)', full_text, re.IGNORECASE)
        if signature_match:
            signature = signature_match.group(2)  # This is the signature text
            answers = full_text[:signature_match.start()]  # This is the text before the signature
        else:
            answers = full_text  # In case there is no signature

    # Clean up the signature
    cleaned_signature = re.sub(r'(Vennlig hilsen|Med vennlig hilsen|Mvh|Lykke til!)\s*', '', signature, flags=re.IGNORECASE)
    cleaned_signature = re.sub(r'^[\s,]*', '', cleaned_signature).strip()  # Remove leading commas and spaces
    
    # Extracting the additional metadata for gender and date
    metadata_div = html.css_first('div.pt-5.font-serif.text-light')
    if metadata_div:
        metadata_text = metadata_div.text(deep=True).strip()
        # Split the text to isolate gender and date
        parts = metadata_text.split('.')
        # Assuming gender and age are separated by a space and age is always a number
        gender_age = parts[0].split()
        gender = ' '.join([word for word in gender_age if not word.isdigit()]).strip()  # Remove the age part
        date = parts[1].strip() if len(parts) > 1 else "Date not found"
        metadata = gender + ", " + date
    else:
        metadata = "Metadata not found", "Metadata not found"

    # Create array of results
    result = [questions, answers, cleaned_signature, metadata]

    return result

studenterspor_url = "https://www.studenterspor.no/ajax_handler.php"
question_urls = fetch_question_url(studenterspor_url)

with open('studenterspor.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Question', 'Answer', 'Signature', 'Metadata'])

    # Fetch info for each URL and write it to the CSV file
    for url in question_urls:
        info = fetch_all_info(url)
        writer.writerow(info)  # Write the question, answer, signature and metadata as a new row

print("Done! Your data is now in 'studenterspor.csv'")