import requests
from bs4 import BeautifulSoup
import random
import time


# def find_result_classes(query):
#     target_url = f"https://www.google.co.in/search?q={query}"
    
#     '''
#     Headers are extra pieces of information sent along with HTTP requests and responses. They provide metadata about the request (like browser type, language, authentication, etc.).
#     '''
#     header = {'User-Agent':user_agent}
#     # request the webpage
#     page = requests.get(target_url, headers=header)
#     soup = BeautifulSoup(page.content,'html.parser')

#      # We want all divs and spans with class attributes into a set {}
#     all_classes = set()
#     # Let's search for all <div> and <span> elements in the parsed HTML (soup).
#     for tag in soup.find_all(['div','span']): #find_all returns a list
#         # extracting the class attribute of the selected tags
#         class_found = tag.get("class")
#         if class_found:
#             all_classes.update(class_found)
#     return list(all_classes) # type-conversion to lists

# Different User agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
]
# Generate Google Search URL
def generate_url(query):
    # sanitize the query
    query = query.replace('+', " plus ").replace('-', " minus ")
    return f"https://www.google.com/search?q={query}"

# Mimic human browsing and sending requests
def fetch_html(target_url):
    # create a session
    session = requests.Session()
    '''
    Headers are extra pieces of information sent along with HTTP requests and responses. They provide metadata about the request (like browser type, language, authentication, etc.).
    '''
    header = {'User-Agent':random.choice(USER_AGENTS)}

    try:
        # add human-like delay
        time.sleep(random.uniform(2,5))
        page = requests.get(target_url, headers=header)
        # check the status of the response to the request
        page.raise_for_status()
        return page.content # raw HTML content returned as bytes
    except requests.exceptions.RequestException as e:
        print(f"Error<Flag> : {e}")
        return None


# extract classes from soup
def extract_all_classes(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    # hold all classes in a set
    extracted_classes = set()
    # find_all returns a list
    for tag in soup.find_all(['div','span']):
        class_found = tag.get("class")
        if class_found:
            extracted_classes.update(class_found)
    return list(extracted_classes)


# filter meaningfull classes of snippets / direct answers
def extract_meaningful_result(raw_html, extracted_classes):
    soup = BeautifulSoup(raw_html, 'html.parser')
    meaningful_results = []
    
    for name in extracted_classes:
        # Filters elements that have a specific class name
        elements = soup.find_all(class_ = name)
        for element in elements:
            text = element.get_text(strip = True)
            if text and len(text)>20:
                meaningful_results.append((name, text))
        return meaningful_results

# Select the best result among meaningful results
'Main function that implements all of the above functions'
def get_best_results(raw_html):
    extracted_classes = extract_all_classes(raw_html)
    meaningful_results = extract_meaningful_result(raw_html,extracted_classes)

    if not meaningful_results:
        return "No relevent results to show !"
    
    # There is an understanding that more the text length, better the result
    meaningful_results.sort(key = lambda x: len(x[1]), reverse=True) # Reverse sort by the length of second element in every tuple i.e. content length
    return meaningful_results[0][1] # the best match

# Search function
def search_key(query):
    URL = generate_url(query)
    raw_html = fetch_html(URL)
    # if request fails ...
    if not raw_html:
        return None
    return get_best_results(raw_html)
