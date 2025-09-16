import requests
from bs4 import BeautifulSoup
import time
import json 
import logging
import pandas as pd

def setup_logging():
    """Config logging settings."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("processing.log", mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
setup_logging()

def crawl_ideas(json_output_path):
    ajax_url = "https://dataforlife.vn/wp-admin/admin-ajax.php"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    'Referer': 'https://dataforlife.vn/idea-bank/',
    'X-Requested-With': 'XMLHttpRequest' 
    }
    payload = {
        'action': 'filter_idea_posts',
        'category_id': '',  
        'search': '',       
        'page': 1           
    }

    current_page = 1
    final_results = []
    max_number_page = 100000

    while current_page <= max_number_page:  
        logging.info(f"--- Crawling page {current_page}... ---")
        
        payload['page'] = current_page
        try:
            response = requests.post(ajax_url, data=payload, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            max_number_page = response_data['data']['max_num_pages']   

            for post in response_data['data']['posts']:
                title = post['title']
                link = post['permalink'] 
                try:
                    response1 = requests.get(link, headers=headers)
                    response1.raise_for_status()

                    soup = BeautifulSoup(response1.content, 'html.parser')
                    category_tag = soup.find('span', class_='category-name')
                    category = category_tag.get_text(strip=True) if category_tag else "Null"

                    #Find title and content
                    content_container = soup.find('div', class_='content-idea-single')
                    detailed_content = {}
                    if content_container:
                        labels = content_container.find_all('h2', class_='label')
                        
                        for label_tag in labels:
                            key = label_tag.get_text(strip=True)
                            value_tag = label_tag.find_next_sibling('p')
                            
                            if value_tag:
                                line = value_tag.get_text(separator='\n', strip=True)
                                value = line.split('\n')
                                detailed_content[key] = value
                            else:
                                detailed_content[key] = "Null."

                    final_idea_data = {
                        'category': category,
                        'title': title,
                        'link': link,
                        'details': detailed_content
                    }
                    final_results.append(final_idea_data)
                    logging.info(f"Finish crawling: {title}")
                    time.sleep(5)  

                except:
                    logging.error(f"Can not access page: {link}")
                    continue

            current_page += 1
            with open(json_output_path, 'w', encoding='utf-8') as f:    
                json.dump(final_results, f, ensure_ascii=False, indent=4)

        
        except requests.RequestException as e:
            logging.error(f"Bug: {e}")
            break

def convert_json_to_csv(json_file_path, csv_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error(f"Bug: Can not find '{json_file_path}'.")
        return
    
    flattened_data = []
    for item in data:
        record = {
            'category': item.get('category', ''),
            'title': item.get('title', ''),
            'link': item.get('link', '')
        }
        
        details = item.get('details', {})
        for key, value in details.items():
            if isinstance(value, list):
                record[key] = ' | '.join(map(str, value))
            else:
                record[key] = value
        
        flattened_data.append(record)

    if not flattened_data:
        logging.info("No data.")
        return
        
    df = pd.DataFrame(flattened_data)
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
    
    logging.info(f"Succesfully converting to '{csv_file_path}'.")
    logging.info(df.columns.tolist()) 

if __name__ == "__main__":
    output_json = '../dataset/JSON_dataset.json'  
    output_csv = '../dataset/CSV_dataset.csv'    
    logging.info("Start crawling...")
    crawl_ideas(output_json)  
    logging.info("Converting JSON to CSV...")
    convert_json_to_csv(output_json, output_csv) 
    logging.info(f"Finish.")
