import requests
from bs4 import BeautifulSoup


headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.232 Whale/2.10.124.26 Safari/537.36"}

def get_last_page(url):
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'lxml')
    try: 
        pages = soup.find("div", {"class": "s-pagination"}).find_all('a')
        last_page = pages[-2].get_text(strip=True)     # get pages except 'next', string 안돼서 get_text
        return int(last_page)
    except: 
        return 1            # prevent None Type error

def extract_job(html, word):
    title = html.find("a", class_=['s-link', 'stretched-link']).get_text()
    company, location = html.find("h3", {"class":"fc-black-700"}).find_all("span",recursive=False) 
                                    # False to Only get the first corresponding values (don't go deep)                                    
    company, location = (company.get_text(strip=True), location.get_text(strip=True)) # .strip('\r') # might use 0 for False, 1 for True
    job_id = html['data-jobid']
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://stackoverflow.com/jobs?id={job_id}&q={word}",
    }

def extract_jobs(last_page, url, word):
    jobs = []
    for page in range(last_page): 
        print(f'Scrapping Stack Overflow page {page+1}...')
        result = requests.get(f"{url}&pg={page}")
        soup = BeautifulSoup(result.text,"html.parser")
        results = soup.find_all("div", {"class":"-job"})

        for result in results:
            job = extract_job(result, word)
            jobs.append(job)

    return jobs

def get_jobs(word):
    url = f'https://stackoverflow.com/jobs?q={word}'
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url, word)
    print (len([dict(t) for t in {tuple(d.items()) for d in jobs}]))
    return [dict(t) for t in {tuple(d.items()) for d in jobs}]
    # return jobs
    # print ([dict(t) for t in {tuple(d.items()) for d in jobs}])

get_jobs("nextJS")