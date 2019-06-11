import urllib.request
import requests
from bs4 import BeautifulSoup

main_url = "https://www.indeed.ca/jobs?l=Canada&jt=fulltime&start="

def parse_site(main_url, array=None):
    if(array is None):
        array = []
    
    for page in range(0, 1000, 20):
        array.append(parse_page(main_url + str(page)))
        print(f"Done page {page}")
    
    return array

def parse_page(url):
    page_results = []
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

        if content.find(class_="post_date") is None:
            data["post_date"] = "Not Available"
        else:
            data["post_date"] = content.find(class_="date").string.strip()

        data["url"] = content.find(class_="jobtitle")['href']
        data["country"] = "Canada"
        data["tags"] = get_tags(data["title"])
        page_results.append(data)
    
    return page_results

def get_tags(str):
    tags = str.lower().split(" ")
    
    if len(str) > 1:
        tags.append(str)
    
    return ",".join(tags)

def sendToServer(data):
    for page in data:
        for results in page:
            requests.post(url="http://127.0.0.1:8000/api/jobs/", json=results)

if __name__ == '__main__':
    data = []
    parse_site(main_url, data)
    sendToServer(data)
    print("done")