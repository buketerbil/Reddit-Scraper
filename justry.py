import time
import uuid
import json
import boto3
import sys
from psutil import LINUX
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from postgres import write_to_db
from downloadimage import download_image



topics = {
    'gaming': ['gaming', 'gamingnews'],
    'politics': [],
    'cryptocurrency': [],
    'anime': []
}

class Scraper: 

    def __init__(self):
        chrome_options=webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument('--disable-gpu')
        prefs = {
            "profile.default_content_setting_values.notifications" : 2, 
            "profile.default_content_settings": {"images": 2}
            }
        chrome_options.add_experimental_option("prefs", prefs)

        if sys.platform == 'linux':
            chrome_path = "/usr/local/bin/chromedriver"
        else:
            chrome_path = r"/Users/macbook/Downloads/chromedriver-2" 

        self.driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

    #TODO: Scrolls down the page.
    def __scroll_down_page(self, speed=7):
        current_scroll_position, new_height= 0, 4000
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            self.driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            # new_height = driver.execute_script("return document.body.scrollHeight")

    #The main method that looks inside the post containers and gets the desired elements from each community.
    def fetch_community(self, community_name):

        self.driver.get(f'https://www.reddit.com/r/{community_name}')

        new_button = self.driver.find_element(By.CSS_SELECTOR, f"a[href='/r/{community_name}/new/']")
        self.driver.execute_script("arguments[0].click();", new_button)
        time.sleep(2)

 
        self.__scroll_down_page(5)
                

        promoteds = WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.promotedlink'))
        )
        print('all promoteds =', len(promoteds))


        containers = WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="post-container"]'))
        )

        all_post_details = {}

        # table_of_posts = []
    

        #Iterate in the containers to extract the desired data from within the post containers.
        for container in containers:
            is_promoted = 'promotedlink' in container.get_attribute("class") 
            print(is_promoted)
            if is_promoted:
                continue
            
            unique_id = str(uuid.uuid4())

            title = WebDriverWait(container, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, '_eYtD2XCVieq6emjKBH3m'))
            ).text
            print(title)

            comment = WebDriverWait(container, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="FHCV02u6Cp2zYL0fhQPsO"]'))
            ).text
            print(comment)
        
            vote = WebDriverWait(container, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, '_1rZYMD_4xY3gRcSS3p8ODO'))
            ).text
            print(vote)

            body = WebDriverWait(container, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'STit0dLageRsa2yR4te_b'))
            ).text
            print(body)

            ''' for_urls = WebDriverWait(container, 15).until(
                EC.presence_of_element_located((By.XPATH, '//a[@data-testid="outbound-link"]'))
            )
            
            print(for_urls.get_attribute('href'))'''
            

            try:
                img_src = EC.presence_of_element_located((By.CLASS_NAME, '_1XWObl-3b9tPy64oaG6fax'))(container).get_attribute("src")
            except NoSuchElementException as e:
                img_src = ''
      
            post_details_dict = {
                'Title': title, 
                'Comment': comment,
                'Vote': vote,
                'ID': unique_id,
                'ImageSource': str(img_src),
                'Body': body
            }

            # table_of_posts.append([title, comment, vote, body, unique_id])

            all_post_details[str(uuid.uuid5(uuid.NAMESPACE_URL, title))] = post_details_dict

        
        write_to_db(all_post_details, community_name)

        json_file_name = f'{community_name}.json'
        self.create_json(all_post_details, json_file_name)
        self.upload_to_s3(all_post_details, json_file_name)

        


    #Transferring your dictionary of post details to a JSON file.
    def create_json(self, all_post_details, file_name='raw_data.json'):
        with open(f'data/json/{file_name}', 'w') as f:
            json_str = json.dumps(all_post_details, indent=4)
            f.write(json_str)

        
    def upload_to_s3(self, all_post_details, file_name):

        s3 = boto3.client("s3")

        for index, post_details_dict in all_post_details.items():
            src = post_details_dict.get('ImageSource')
            if src:
                download_image(src, index)
                s3.upload_file(f'data/img/{index}.png', 'buketsbucket', f'data/img/{index}.png', ExtraArgs={'ContentType': "image/png"})

        #Uploading the JSON file to S3.             
        s3.upload_file(f'./data/json/{file_name}', 'buketsbucket', f'data/json/{file_name}')
        




if __name__ == "__main__":
    
    scrape_reddit = Scraper()
    for topic, communities in topics.items():
        for community in communities:
            
            scrape_reddit.fetch_community(community) 
     


# driver.quit()