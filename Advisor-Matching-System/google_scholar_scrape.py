import requests
import re
from bs4 import BeautifulSoup
import urllib3
from collections import defaultdict
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import unquote, urlparse, parse_qs
import pandas as pd
import json

def get_research_interests(author_name,university_name):
    proxies = {
    "http": "http://scraperapi:apikey@proxy-server.scraperapi.com:8001",
    "https": "http://scraperapi:apikey@proxy-server.scraperapi.com:8001"
    }
    query = author_name + ' ' + university_name + ' ' + 'google scholar'
    url = 'https://www.google.com/search?q=' + query.replace(' ', '+').replace('–', '')
    response = requests.get(url, proxies=proxies, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    author_id = 0
    search_results = soup.find_all('div', {'class':'g'})
    if search_results:
        first_result = search_results[0]
        url_tag = first_result.find('a')
        if url_tag:
            url = url_tag['href']
    response = requests.get(url, proxies = proxies, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    interests = soup.find_all('a',{'class':'gsc_prf_inta gs_ibl'})
    ri = []
    for interest in interests:
        ri.append(interest.text)
    return ri

file_path = 'faculty_names_titles.xlsx'  
column_index = 0  
df = pd.read_excel(file_path, header=None, skiprows=2)
names = df.iloc[:, column_index].tolist()
dict_research={}

with open("RI.json", 'a') as file:
    for i in range(0,len(names)): 
        publications = get_research_interests(names[i], "UIUC")
        dict_research[names[i]] = publications
        entry = {names[i]: publications}
        json_string = json.dumps(entry)
        file.write(json_string + '\n')

with open('RI.json', 'r') as file:
    professors_data = [json.loads(line) for line in file]


with open('results.json', 'r') as file:
    publications_data = json.load(file)

combined_data = {}
for professor_entry in professors_data:
    professor_name = list(professor_entry.keys())[0]
    interests = professor_entry[professor_name]

    combined_data[professor_name] = {"interests": interests, "publications": []}

for publication_entry in publications_data:
    professor_name = publication_entry.get("query", "")
    if professor_name in combined_data:
        for publication in publication_entry.get("results", []):
            combined_data[professor_name]["publications"].append({
                "title": publication.get("title", ""),
                "snippet": publication.get("snippet", "")
            })

with open("/server/FinalProfessorsData.json", 'w') as output_file:
    json.dump(combined_data, output_file, indent=2)