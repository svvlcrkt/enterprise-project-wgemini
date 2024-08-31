from celery import Celery
import requests
import json
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import google.generativeai as genai
import os

logger = logging.getLogger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0')

# Google Gemini API anahtarınızı ayarlayın
genai.configure(api_key="AIzaSyDZEnE3Q6xACtPQEjBxtsy7X_N2BwqTZ4U")

@app.task
def scrape_and_process():
    try:
        logger.info("Starting the scraping and processing task")
        url = "https://ranking.glassdollar.com/graphql"
        
        query = """
        query {
            topRankedCorporates {
                name
                description
                logo_url
                hq_city
                hq_country
                website_url
                linkedin_url
                twitter_url
                startup_partners_count
                startup_partners {
                    company_name
                    logo
                    city
                    website
                    country
                    theme_gd
                }
            }
        }
        """

        response = requests.post(
            url,
            json={'query': query},
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 200:
            data = response.json()

            # Enterprise bilgilerini JSON formatında döndür
            enterprise_data = extract_enterprise_data(data)
            with open('enterprise_data.json', 'w') as f:
                json.dump(enterprise_data, f, indent=4)

            # Kümeleme ve analiz kısmı
            descriptions = [enterprise['description'] for enterprise in enterprise_data]
            vectorizer = TfidfVectorizer(stop_words='english')
            X = vectorizer.fit_transform(descriptions)

            num_clusters = 5
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            kmeans.fit(X)
            clusters = kmeans.labels_.tolist()

            cluster_summaries = []
            for cluster_idx in range(num_clusters):
                cluster_items = [enterprise_data[i] for i in range(len(enterprise_data)) if clusters[i] == cluster_idx]
                cluster_descriptions = " ".join([item['description'] for item in cluster_items])
                
                # Başlık ve açıklama oluşturma
                prompt_title = f"Generate a title for the following cluster of startup companies:\n{cluster_descriptions}\n"
                prompt_summary = f"Generate a summary for the following cluster of startup companies:\n{cluster_descriptions}\n"
                
                try:
                    # Google Gemini API'sini kullanarak başlık ve açıklama oluşturma
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    
                    # Başlık oluşturma
                    title_response = model.generate_content([prompt_title])
                    title_text = title_response.text
                    
                    # Açıklama oluşturma
                    summary_response = model.generate_content([prompt_summary])
                    summary_text = summary_response.text
                    
                    cluster_summary = {
                        'cluster_id': cluster_idx,
                        'title': title_text,
                        'summary': summary_text,
                        'enterprises': cluster_items
                    }

                    cluster_summaries.append(cluster_summary)

                except Exception as e:
                    logger.error(f"Text generation failed for cluster {cluster_idx}: {str(e)}")
                    cluster_summaries.append({
                        'cluster_id': cluster_idx,
                        'title': "Title generation failed",
                        'summary': "Summary generation failed",
                        'enterprises': cluster_items
                    })

            # Analiz sonuçlarını JSON olarak döndür
            with open('clustered_enterprises.json', 'w') as f:
                json.dump(cluster_summaries, f, indent=4)

            return {
                "enterprise_data": enterprise_data,
                "analysis_results": cluster_summaries
            }

        else:
            logger.error(f"Failed to fetch data. Status code: {response.status_code}")
            logger.error(response.text)
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        return {"error": str(e)}

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
        }
        enterprises.append(enterprise)
    return enterprises
