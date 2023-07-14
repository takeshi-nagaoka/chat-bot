import requests
from bs4 import BeautifulSoup

def fetch_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_data(data):
    soup = BeautifulSoup(data, "html.parser")
    return soup

def generate_response(parsed_data, user_input):
    question_tags = parsed_data.find_all("h4")
    for tag in question_tags:
        if user_input in tag.text:
            answer_tag = tag.find_next_sibling("p")
            if answer_tag:
                return f"{tag.text}\n\n{answer_tag.text.strip()}"
    return None
