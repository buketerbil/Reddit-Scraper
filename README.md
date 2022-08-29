## Web Scraper for Reddit
A Reddit data collection project.
I have designed this project to obtain mostly unstructured and some structured data from Reddit, an interesting American social news/ content rating platform that is an incredible source of information on countless fields of human knowledge and a website where it is possible to contribute to any discussion one can think of. The aim of this scraper is to analyse the data from some of the hottest topics in the world and find out the current most popular words in each different topic. This could be useful to make predictions about cryptocurrency and stock markets for investors. 
I used Selenium technology to scrape the desired data.

# Summary of the project structure.
Using object oriented programming approach, the scraper contains one module with a class that holds most of the code: class Scraper().
Scraper class allows for navigating, installing and scalably storing the scraped data. The class includes methods to:
- Slowly scroll down the page to enable navigating (__scroll_down_page)
- Click the ‘new’ button of each community to scrape the latest posts and not the most popular
- Determine the advertisements to avoid scraping promoted posts
- Scrape the texts of titles, number of comments, number of votes and image sources and print them out in text
- Store the data of each community in separate JSON files and upload these raw data files in AWS S3 bucket
- Convert the raw data to tabular and upload the tables to AWS RDS through sqlalchemy and psycop2

# Testing
Some of the methods were tested using the unittest module of Python, it is possible to test the methods through the file ‘testscraper.py’. 
- Testing directory has two modules: [testing.py](http://testing.py) and [testscraper.py](http://testscraper.py) (contains TestScraper() and TestIntegrationScraper() which are TestCase classes)
- The test will check that each data entry has only one string data
- It will check that the data has been placed in the JSON file

# Cloud Storage 
I used Amazon Web Services (AWS) software tools to store my objects in an S3 bucket through a web service interface and RDS (Relational Database Service) to set up, operate and scalably store my tabular data in the cloud. 
As the code runs, the types of data are saved locally under the folder 'data'; 
- images under subfolder 'img' 
- text files of post titles, comments, unique ID, image source & body under subfolder 'json' which also contains the test for the JSON file.
Subsequently, the data are saved locally and to Amazon S3 bucket with the same file format.

Data has been converted to tabular data through pandas and SQL alchemy to store in Postgres. The tabular data in Postgres was connected to AWS RDS to be stored in the cloud.

# Deployment of the Scraper: Cloud Computing
AWS EC2 instance was created and the scraper was run on the instance where the scraper is to be deployed. Connection to the EC2 instance was ensured through Terminal. 

# Docker containerisation and GUI image 
To achieve a scalably ditributable scraper, I attempted to first build the Docker image locally however it was time-consuming and complicated to do this due to several complications faced with an M1 chip, e.g.:
- It is not possible to run headless Chrome on Macs with M1 chip
- Multi-architecture builds (AMD64 vs ARM64 instruction set architectures [ISAs])

As it is not possible to run headless Chrome on Macs with M1 chip, the Docker container was built and ran directly on the EC2 instance. Then it was pushed to DockerHub which made the image publicly accessible.
The scraper image can be pulled through the command: docker pull bukete/redditscraper
<img width="1172" alt="Screenshot 2022-08-29 at 15 45 03" src="https://user-images.githubusercontent.com/102605064/187228600-0c7f105c-4924-4b8a-8201-c0a2b8ec1db9.png">

# Monitoring through Prometheus and Grafana
Prometheus was installed and its YAML file was configured to monitor the scraper on Docker container on EC2 instance. Then, Prometheus was used to monitor the container used.

Thereafter, Grafana was used for monitoring metric visualisations.


