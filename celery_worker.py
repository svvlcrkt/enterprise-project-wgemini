from celery import Celery
import requests
from bs4 import BeautifulSoup
import json
import logging

logger = logging.getLogger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0')

@app.task
def scrape_and_process():
    try:
        logger.info("This is a log message")
        url = "https://ranking.glassdollar.com/graphql"
        # GraphQL sorgusu
        query = """
        query{topRankedCorporates{
        name
        description
        logo_url
        hq_city
        hq_country
        website_url
        linkedin_url
        twitter_url
        startup_partners_count
        startup_partners{
            company_name
            logo
            city
            website
            country
            theme_gd
        }
        }}
        """


        # Send the GraphQL request
        response = requests.post(
            url,
            json={'query': query},
            headers={'Content-Type': 'application/json'}
        )

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and structure the data
            def extract_enterprise_data(data):

                enterprises = []
                for item in data['data']['topRankedCorporates']:
                    enterprise = {
                        'name': item['name'],
                        'description': item['description'],
                        'logo_url': item['logo_url'],
                        'hq_city': item['hq_city'],
                        'hq_country': item['hq_country'],
                        'website_url': item['website_url'],
                        'linkedin_url': item.get('linkedin_url', ''),
                        'twitter_url': item.get('twitter_url', ''),
                        'startup_partners_count': len(item['startup_partners']),
                        'startup_partners': [
                            {
                                'company_name': sp['company_name'],
                                'logo_url': sp['logo'],
                                'city': sp['city'],
                                'website': sp['website'],
                                'country': sp['country'],
                                'theme_gd': sp['theme_gd']
                            } for sp in item['startup_partners']
                        ],
                        #'startup_themes': item['startup_themes']
                    }
                    enterprises.append(enterprise)
                return json.dumps(enterprises)

            # Extract the data
            enterprise_data = extract_enterprise_data(data)
            print(len(enterprise_data))
            if enterprise_data is not None:
                with open('enterprises.json', 'w') as f:
                    f.write(enterprise_data)
    
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print(response.text)

    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
       

