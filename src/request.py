import requests
from bs4 import BeautifulSoup
import time as tm
from string_processing import split_sentences

def get_linkedin_jobs(search_query, location):
    url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location={location}"  
    config = {
        'headers': {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        },
        'proxies': {}
    }

    for _ in range(3):
        try:
            request = requests.get(url, headers=config['headers'], timeout=5)
            soup = BeautifulSoup(request.content, 'html.parser')
        except requests.exceptions.Timeout:
            print(f"Timeout occurred for URL: {url}, retrying in 1s...")
            tm.sleep(1)
        except Exception as _:
            continue
    if soup is None:
        return []
    
    jobs = []
    job_cards = soup.find_all('div', class_='base-card')

    for job_card in job_cards:
        
        try:
            job_title = job_card.find('h3', class_='base-search-card__title').text.strip()
            if "*" in job_title:
                print("Aborting, LinkedIn is blocking the request.")
                return None
    
            company_name = job_card.find('h4', class_='base-search-card__subtitle').text.strip()
            location = job_card.find('span', class_='job-search-card__location').text.strip()
            listing_date = job_card.find('time', class_='job-search-card__listdate').get('datetime')
            link = job_card.find('a', class_='base-card__full-link').get('href')
            
            job_card = requests.get(link, headers=config['headers'])
            job_card = BeautifulSoup(job_card.content, 'html.parser')
            job_card = job_card.find('div', class_='description__text description__text--rich')
            description = split_sentences(job_card.find('section', class_='show-more-less-html').text.strip())
            
            jobs.append({
                'title': job_title,
                'company': company_name,
                'location': location,
                'listing_date': listing_date,
                'link': link,
                'description': description
            })
      
        except Exception as _:
            continue

    return jobs


#search_query = "Software Engineer"
#location = "Berlin"
#description = get_linkedin_jobs(search_query, location)
