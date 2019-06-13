import urllib.request
import requests
import json
import re
from bs4 import BeautifulSoup

main_url = "https://www.indeed.ca/jobs?l=Canada&jt=fulltime&start="

def parse_site(main_url, data):
    for page in range(0, 1000, 20):
        parse_page(main_url + str(page), data)
        print(f"Done page {page}")

def parse_page(url, data_array):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all("div", class_="result")
    for content in results:
        data = {}
        data["title"] = content.find(class_="jobtitle").string.strip()
        location = content.find(class_="location").string.strip().split(", ")
        data["city"] = location[0]

        if len(location) > 1:
            data["state"] = location[1]
        else:
            data["state"] = "Not Available"
        
        data["description"] = content.find(class_="summary").string.strip()

        if content.find(class_="company").string is None:
            data["company"] = "Not Available"
        else:
            data["company"] = content.find(class_="company").string.strip()

        if content.find(class_="date") is None:
            data["post_date"] = "Not Available"
        else:
            data["post_date"] = content.find(class_="date").string.strip()
        linkSlug = content.find(class_="jobtitle")['href']
        data["url"] = f"https://www.indeed.com{linkSlug}"
        data["country"] = "Canada"
        data["tags"] = get_tags(data["title"])
        data_array.append(data)
    
    return data_array

def get_tags(str):
    cleaned_str = re.sub(r"\s*[^A-Za-z]+\s*", ' ', str).lower()
    tags = cleaned_str.split(" ")
    return tags

def sendToServer(data):
    for results in data:
        requests.post(url="http://127.0.0.1:8000/api/jobs/", json=results)


if __name__ == '__main__':
    data = []
    parse_site(main_url, data)
    sendToServer(data)
    print("done")