from flask import Flask, request, jsonify
from selectorlib import Extractor
import requests
import json
from urllib.parse import urlparse
from time import sleep
from nltk.metrics import jaccard_distance

# Define your YAML content, scrape function, and other functions here as in your original script.
yaml_content = """
name:
    css: '#productTitle'
    type: Text
price:
    css: '#price_inside_buybox'
    type: Text
short_description:
    css: '#featurebullets_feature_div'
    type: Text
images:
    css: '.imgTagWrapper img'
    type: Attribute
    attribute: data-a-dynamic-image
rating:
    css: span.arp-rating-out-of-text
    type: Text
number_of_reviews:
    css: 'a.a-link-normal h2'
    type: Text
variants:
    css: 'form.a-section li'
    multiple: true
    type: Text
    children:
        name:
            css: ""
            type: Attribute
            attribute: title
        asin:
            css: ""
            type: Attribute
            attribute: data-defaultasin
product_description:
    css: '#productDescription'
    type: Text
sales_rank:
    css: 'li#SalesRank'
    type: Text
link_to_all_reviews:
    css: 'div.card-padding a.a-link-emphasis'
    type: Link
"""
def scrape(url):
    e = Extractor.from_yaml_string(yaml_content)
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    r = requests.get(url, headers=headers)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    return e.extract(r.text)

def jaccard_similarity(str1, str2):
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())
    similarity = 1 - jaccard_distance(set1, set2)
    return similarity

def result(title):
    data = requests.get("https://script.google.com/macros/s/AKfycbyfy36EPPINEXetgDGdIIA-HqHexrHlBg1ZPwmhssRVWst_ki-cT1wVouHCdv02q0pX/exec")
    if data.status_code == 200:
       product_list = json.loads(data.text)      
    max_similarity = 0
    best_match = None
    amazonTitle = title
    for product in product_list:
        csv_product = product["Product"]
        csv_url = product["Link"]
        similarity = jaccard_similarity(amazonTitle, csv_product)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = csv_product
            url = csv_url

    result_dict = {
        "name": best_match,
        "url": url
    }
    json_result = json.dumps(result_dict)
    print("Amazon Title:", amazonTitle)
    print(f"Product with Highest Jaccard Similarity: {json_result} ")
    return json_result

app = Flask(__name__)

@app.route('/api/scrape', methods=['POST'])
def scrape_and_compare():
    try:
       
        url = request.get_data()
    
        data = scrape(url)
        if data is None:
            return jsonify({'error': 'Failed to scrape data from the provided URL'}), 500
        
        result_data = result(data.get('name'))
        return jsonify(result_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port = 5061)
