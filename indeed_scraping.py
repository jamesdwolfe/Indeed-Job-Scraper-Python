import urllib
import pandas as pd
import requests
from bs4 import BeautifulSoup
import math

# ---------PARAMETERS---------
query = "Software"
loc = "United States"
limit = 50
from_age = 7
file_name = "indeed_jobs.xlsx"


def load_indeed_jobs_div(start):
    variables = {'q': query, 'l': loc, 'sort': 'date', 'fromage': from_age, 'limit': limit, 'explvl': 'entry_level',
                 'start': start}
    url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(variables))
    print("Title:", query, "- Location:", loc, "- Limit:", limit, "- Start:", start)
    print(url)
    page = requests.get(url)
    beautiful_soup = BeautifulSoup(page.content, 'html.parser')
    return beautiful_soup


def extract_title(job_elem):
    title_elem = job_elem.find('h2', class_='title')
    title = title_elem.text.strip()
    return title


def extract_company(job_elem):
    company_elem = job_elem.find('span', class_='company')
    company = company_elem.text.strip()
    return company


def extract_link(job_elem):
    link = job_elem.find('a')['href']
    link = 'https://www.indeed.com' + link
    return link


def extract_date(job_elem):
    date_elem = job_elem.find('span', class_='date')
    date = date_elem.text.strip()
    return date


def extract_location(job_elem):
    location_elem = job_elem.find(class_='location')
    location = location_elem.text.strip()
    return location


def save_excel(saved_jobs_list, saved_file_name):
    jobs = pd.DataFrame(saved_jobs_list)
    jobs.to_excel(saved_file_name)


soup = load_indeed_jobs_div(0)
job_count = soup.find('div', id="searchCountPages").contents[0].split()[3].replace(',', '')
page_count = math.floor(int(job_count) / 50)
print("Job Count:", job_count, "- Page Count: ", page_count)

cols = ['titles', 'companies', 'locations', 'dates', 'links']
titles = []
companies = []
locations = []
links = []
dates = []

for i in range(page_count + 1):
    soup = load_indeed_jobs_div(i * limit)
    job_soup = soup.find(id="resultsCol")
    job_elems = job_soup.find_all('div', class_="jobsearch-SerpJobCard")

    for e in job_elems:
        titles.append(extract_title(e).strip('\nnew'))
        companies.append(extract_company(e))
        locations.append(extract_location(e))
        links.append(extract_link(e))
        dates.append(extract_date(e))

extracted_info = [titles, companies, locations, dates, links]

jobs_list = {}
num_listings = len(extracted_info[0])
for i in range(len(cols)):
    jobs_list[cols[i]] = extracted_info[i]

save_excel(jobs_list, file_name)
