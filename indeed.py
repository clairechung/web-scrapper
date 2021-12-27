import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://www.indeed.com/jobs?q=python&from=googlesl&limit={LIMIT}'
headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.232 Whale/2.10.124.26 Safari/537.36"}

def get_last_page():
    page = 0    # shorter version using page number
    result = requests.get(URL, headers=headers)

    while True:
        soup = BeautifulSoup(result.text, 'lxml')
        pagination = soup.find("div", {"class": "pagination"})
        links = pagination.find_all('a')
        if links[-1]['aria-label'] == "Next":
            pass
        else:
            break
        page += 1
        result = requests.get(f'{URL}&start={page*LIMIT}')
    return page

def extract_job(html): 
    title = html.select_one('.jobTitle>span').string
    company = html.find("span", {"class" : "companyName"})
    if company.a is not None:       # if company_anchor is not None:
        # company_link = 'https://www.indeed.com'+company.a['href']
        company = company.find("a").string
    else:
        company = company.string
        # company_link = None
    
    location = html.select_one("pre > div").text
    job_id = html.parent['data-jk']

    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://www.indeed.com/viewjob?jk={job_id}&from=web&vjs=3"
        # 'company_link': company_link
    }

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'Scrapping Indeed page {page+1}...')
        result = requests.get(f'{URL}&start={page*LIMIT}')
        soup = BeautifulSoup(result.text, 'html.parser')    
        results = soup.find_all("div", {"class": "slider_container"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
