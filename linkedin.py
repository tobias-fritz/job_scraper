import requests
from bs4 import BeautifulSoup
import time as tm

def get_linkedin_jobs(search_query, location):
    url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location={location}"  
    config = {
        'headers': {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        },
        'proxies': {}
    }
    print(url)

    for _ in range(10):
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
    
    print("start")
    jobs = []
    job_cards = soup.find_all('div', class_='base-card')

    for job_card in job_cards:
        try:
            job_title = job_card.find('h3', class_='base-search-card__title').text.strip()
            company_name = job_card.find('h4', class_='base-search-card__subtitle').text.strip()
            location = job_card.find('span', class_='job-search-card__location').text.strip()
            listing_date = job_card.find('time', class_='job-search-card__listdate').get('datetime')
            link = job_card.find('a', class_='base-card__full-link').get('href')
            # access the link to get the full job description
            job_card = requests.get(link, headers=config['headers'])
            job_card = BeautifulSoup(job_card.content, 'html.parser')
            job_card = job_card.find('div', class_='description__text description__text--rich')
            description = job_card.find('section', class_='show-more-less-html').text.strip().replace('\n', ' ')
            
            print(description)
            return description
            break
            
            """<div class="description__text description__text--rich">
            <section class="show-more-less-html" data-max-lines="5">
            <div class="show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden">
            <strong>About us:<br/><br/></strong>We are a dynamic start up of talented individuals united by our passion for crafting cutting-edge solutions using modern technologies. Our team is young and agile, thriving on a fast-paced work culture where we're encouraged to move quickly and innovate, even if it means breaking things along the way sometimes.<br/><br/><strong>About PlanD:<br/><br/></strong>At PlanD we are pioneering the digital transformation of the commercial cleaning industry with our comprehensive cloud-based software. We are providing essential tools for shift planning, time tracking, payroll, and invoicing, tailored to enhance the efficiency of our customers. Our mission is to empower these companies to focus more on growth and customer satisfaction by streamlining administrative tasks.<br/><br/>Tasks<br/><br/><ul><li>Full stack implementation of new features.</li><li>Take responsibility from implementation to release.</li><li>Contribute your own ideas to help shape our product.</li><li>Conduct bug-fixing activities to enhance software performance and reliability.</li><li>Collaborating with designers and other developers.<br/><br/><br/></li></ul><strong>Requirements<br/><br/></strong><ul><li>Passion for programming and a drive for self-improvement in new technologies.</li><li>Completed Bachelor's degree in Computer Science or a related field.</li><li>Fluent in either german or english</li><li>At least one year experience in web development (preferably Angular)</li><li>At least one year experience in backend development (preferably PHP)</li><li>Experience in Mobile Development (Flutter) is a plus<br/><br/><br/></li></ul><strong>Benefits<br/><br/></strong><ul><li>Full involvement in the development process from concept to deployment.</li><li>Significant freedom and input in project executions.</li><li>Competitive salary and flexible working conditions.</li><li>Additional company benefits (Hello Fresh, Swapfiets, Urban Sports Club, ...)<br/><br/><br/></li></ul>If you are eager to contribute to a cutting-edge company and take on the freedom and challenges of a young start up, we might be the perfect fit for you.<br/><br/>We are looking forward to your application and to innovate together. 🚀
                    </div>
            <button aria-expanded="false" aria-label="i18n_show_more" class="show-more-less-html__button show-more-less-button show-more-less-html__button--more ml-0.5" data-tracking-control-name="public_jobs_show-more-html-btn">
            <!-- -->
                    
                        Show more
                    

                    <icon class="show-more-less-html__button-icon show-more-less-button-icon" data-delayed-url="https://static.licdn.com/aero-v1/sc/h/cyolgscd0imw2ldqppkrb84vo"></icon>
            </button>
            <button aria-expanded="true" aria-label="i18n_show_less" class="show-more-less-html__button show-more-less-button show-more-less-html__button--less ml-0.5" data-tracking-control-name="public_jobs_show-less-html-btn">
            <!-- -->
                    
                        Show less
                    

                    <icon class="show-more-less-html__button-icon show-more-less-button-icon" data-delayed-url="https://static.licdn.com/aero-v1/sc/h/4chtt12k98xwnba1nimld2oyg"></icon>
            </button>
            <!-- --> </section>
            </div>"""
            jobs.append({
                'title': job_title,
                'company': company_name,
                'location': location,
                'listing_date': listing_date,
                'link': link,
            })
      
        except Exception as err:
            print(err)
            continue
    # div = soup.find('div', class_='description__text description__text--rich')


    return jobs


search_query = "Software Engineer"
location = "Berlin"
description = get_linkedin_jobs(search_query, location)
